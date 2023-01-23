
import json
import os
import secrets
import subprocess
import shutil
import hashlib
from abc import abstractmethod, ABC

import requests
from multiprocessing import Process, Lock
from flask import Flask, Response, request, send_file
from flask_cors import cross_origin
from werkzeug.exceptions import Unauthorized, TooManyRequests, BadRequest
from functools import wraps

from randomBackgroundChanger.DAL import queries
from randomBackgroundChanger.imgur.imgurAuthenticator import InvalidPin

PORT = 5000


class CrossOriginExceptionMixin(ABC):

    def get_headers(self, environ=None, scope=None):
        headers = super().get_headers(environ=environ, scope=scope)
        headers.append(("Access-Control-Allow-Origin", "*"))
        return headers


class CrossOriginUnauthorised(CrossOriginExceptionMixin, Unauthorized):
    pass


class CrossOriginBadRequest(CrossOriginExceptionMixin, BadRequest):
    pass


class AlreadyDownloadingImagesException(Exception):
    pass


class FileHandler:

    def __init__(self, imgurController):
        self._imageController = imgurController
        self._downloadingImages = Lock()
        self._listingImages = Lock()

    @property
    def imageFilePaths(self):
        with self._listingImages:
            return sorted([
                self.getFilePath(filePath) for filePath
                in os.listdir(self.directoryPath)
                if ".gitkeep" not in filePath
            ])

    @property
    def currentImagePath(self):
        if self.imageFilePaths:
            return self.imageFilePaths[0]

    @property
    def currentBackgroundImage(self):
        if self.imageFilePaths:
            return self.imageFilePaths[0]

    def cycleBackgroundImage(self):
        """ Change the background to the next image in the queue
        """
        if len(self.imageFilePaths) <= 1:
            if self._downloadingImages.acquire(block=False):
                try:
                    self.getImages()
                finally:
                    self._downloadingImages.release()
            else:
                raise AlreadyDownloadingImagesException

        self._deleteLastImage()

    def getImages(self):
        """ Request new image URLs from the image controller
        """
        imgurImages = self._imageController.requestNewImages()
        runningProcesses = []
        for imgurImage in imgurImages:
            imageDownloadProcess = Process(target=self._downloadImage, args=(imgurImage, ))
            imageDownloadProcess.start()
            runningProcesses.append(imageDownloadProcess)

        # ensure all images have downloaded before continuing
        for runningProcess in runningProcesses:
            runningProcess.join()

    def _downloadImage(self, imgurImage):
        response = requests.get(imgurImage.imageURL, stream=True)
        fileName = self.getFilePath(imgurImage.imageTitle)
        with open(fileName, "wb") as imageFile:
            shutil.copyfileobj(response.raw, imageFile)

    def _deleteLastImage(self):
        if self.currentBackgroundImage not in self.imageFilePaths:
            # Don't delete images that haven't been downloaded by the image controller
            return

        try:
            os.remove(self.currentBackgroundImage)
        except Exception as e:
            print("Could not delete file")
            print(str(e))

    def getFilePath(self, fileName):
        return os.path.join(self.directoryPath, fileName)

    def addPin(self, pin):
        self._imageController.imgurAuthenticator.addPin(pin)

    @property
    def directoryPath(self):
        return os.path.join(os.getcwd(), "backgroundImages")


class HTTPAuthenticator(Flask):

    def __init__(self, clientId, clientSecret, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)

        self._clientId = clientId
        self._clientSecret = clientSecret

        self.add_url_rule("/token", view_func=self.addToken, methods=["POST"])
        self.add_url_rule("/token", view_func=self.revokeToken, methods=["DELETE"])

    @staticmethod
    def tokenResponse(token):
        return Response(
            response=json.dumps({'token': token}), mimetype="application/json", status=200
        )

    @cross_origin(automatic_options=True)
    def addToken(self):
        self.checkValidSecretAndId()
        token = secrets.token_urlsafe(64)
        validDays = min(request.json.get("validDays", 30), 120)
        queries.addNewToken(token, validDays)
        return self.tokenResponse(token)

    @cross_origin(automatic_options=True)
    def revokeToken(self):
        self.checkValidSecretAndId()
        token = request.json.get("token")
        queries.revokeToken(token)
        return self.tokenResponse(token)

    def checkValidSecretAndId(self):
        clientId = request.json.get("clientId")
        clientSecret = request.json.get("clientSecret")
        if clientId != self._clientId or clientSecret != self._clientSecret:
            raise Unauthorized

    @staticmethod
    def checkTokenExists(func):
        @wraps(func)
        def _innerFunc(self):
            authorisationHeader = request.headers.get("Authorization")
            if not authorisationHeader or len(authorisationHeader.split(" ")) == 1:
                raise CrossOriginUnauthorised

            authorisationToken = authorisationHeader.split(" ")[1]
            if not queries.validToken(authorisationToken):
                raise CrossOriginUnauthorised
            return func(self)
        return _innerFunc


class HTTPFileHandler(FileHandler, HTTPAuthenticator):

    def __init__(self, imgurController, clientId, clientSecret, *args, **kwargs):
        FileHandler.__init__(self, imgurController)
        HTTPAuthenticator.__init__(self, clientId, clientSecret, *args, **kwargs)

        self.add_url_rule("/", view_func=self.homePage, methods=["GET"])
        self.add_url_rule("/change-background", view_func=self.changeBackground, methods=["POST", "GET"])
        self.add_url_rule("/current-image", view_func=self.currentImage, methods=["GET"])
        self.add_url_rule("/imgur-pin", view_func=self.imgurPin, methods=["POST"])
        self.add_url_rule("/current-image-hash", view_func=self.currentImageHash, methods=["GET"])

    @cross_origin(automatic_options=True)
    def homePage(self):
        return Response(status=200)

    @cross_origin(automatic_options=True)
    @HTTPAuthenticator.checkTokenExists
    def imgurPin(self):
        pin = request.json.get("pin")
        if not pin:
            raise CrossOriginBadRequest("Pin json key not passed")

        try:
            self.addPin(pin)
        except InvalidPin as e:
            raise CrossOriginBadRequest(str(e))
        return Response(status=200)

    @cross_origin(automatic_options=True)
    @HTTPAuthenticator.checkTokenExists
    def changeBackground(self):
        try:
            self.cycleBackgroundImage()
        except AlreadyDownloadingImagesException:
            raise TooManyRequests()
        return Response(status=200)

    @cross_origin(automatic_options=True)
    @HTTPAuthenticator.checkTokenExists
    def currentImageHash(self):
        """ Get the current image hash to check for difference without sending the full image
        """
        responseBody = {
            "hash": self._getCurrentImageHash()
        }
        return Response(json.dumps(responseBody), mimetype="json")

    def _getCurrentImageHash(self):
        currentImagePath = self.currentBackgroundImage
        bufferSize = 65536
        sha1 = hashlib.sha1()

        with open(currentImagePath, "rb") as currentImage:
            imageData = currentImage.read(bufferSize)
            while imageData:
                sha1.update(imageData)
                imageData = currentImage.read(bufferSize)

        return sha1.hexdigest()

    @cross_origin(automatic_options=True)
    @HTTPAuthenticator.checkTokenExists
    def currentImage(self):
        return send_file(self.currentImagePath, mimetype="image/gif")


class BackgroundChanger(HTTPFileHandler, ABC):

    @property
    def currentBackgroundImage(self):
        return self._getCurrentImage()

    @abstractmethod
    def cycleBackgroundImage(self):
        # You must call super when overriding this function
        # it must also be overridden by the child
        super().cycleBackgroundImage()

    @abstractmethod
    def _getCurrentImage(self):
        pass


class GSettingsHTTPBackgroundChanger(BackgroundChanger):

    def cycleBackgroundImage(self):
        super().cycleBackgroundImage()
        subprocess.run(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", self.currentImagePath]
        )
        subprocess.run(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-options", "scaled"]
        )

    def _getCurrentImage(self):
        currentBackground = subprocess.run(
            ["/usr/bin/gsettings", "get", "org.gnome.desktop.background", "picture-uri"], stdout=subprocess.PIPE
        ).stdout
        # remove fat from response
        return currentBackground.decode().split("'")[1]
