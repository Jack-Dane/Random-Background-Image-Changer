
import json
import os
import secrets
import subprocess
import shutil
from abc import abstractmethod, ABC

import requests
from multiprocessing import Process, Lock
from flask import Flask, Response, request
from flask_cors import cross_origin
from werkzeug.exceptions import Unauthorized, TooManyRequests
from functools import wraps

from randomBackgroundChanger.DAL import queries

PORT = 5000


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
        try:
            os.remove(self.currentImagePath)
        except Exception as e:
            print("Could not delete file")
            print(str(e))

    def getFilePath(self, fileName):
        return os.path.join(self.directoryPath, fileName)

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
            if not authorisationHeader:
                raise Unauthorized

            authorisationToken = authorisationHeader.split(" ")[1]
            if not queries.validToken(authorisationToken):
                raise Unauthorized
            return func(self)
        return _innerFunc


class HTTPFileHandler(FileHandler, HTTPAuthenticator):

    def __init__(self, imgurController, clientId, clientSecret, *args, **kwargs):
        FileHandler.__init__(self, imgurController)
        HTTPAuthenticator.__init__(self, clientId, clientSecret, *args, **kwargs)

        self.add_url_rule("/", view_func=self.homePage, methods=["GET"])
        self.add_url_rule("/change-background", view_func=self.changeBackground, methods=["POST", "GET"])
        self.add_url_rule("/current-image", view_func=self.currentImage, methods=["GET"])

    @cross_origin(automatic_options=True)
    def homePage(self):
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
    def currentImage(self):
        return Response(json.dumps(self.currentImagePath), mimetype="json")


class BackgroundChanger(HTTPFileHandler, ABC):

    @property
    def currentImagePath(self):
        currentImagePath = super().currentImagePath
        if currentImagePath:
            return currentImagePath
        return self._getCurrentImage()

    @abstractmethod
    def cycleBackgroundImage(self):
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
