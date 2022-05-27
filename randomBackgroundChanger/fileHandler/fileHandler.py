
import json
from mimetypes import MimeTypes
import mimetypes
import os
import subprocess
import shutil
import requests
from flask import Flask, Response

PORT = 5000


class FileHandler(Flask):

    def __init__(self, imgurController, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)
        self._imageFilePaths = []
        self._currentImagePath = None
        self._imageController = imgurController
        self.addExistingImagesToList()

        self.add_url_rule("/", view_func=self.homePage, methods=["GET"])

        self.add_url_rule("/change-background", view_func=self.changeBackground, methods=["POST", "GET"])

        self.add_url_rule("/background-images", view_func=self.backgroundImages, methods=["GET"])

        self.add_url_rule("/current-image", view_func=self.currentImage, methods=["GET"])

    def homePage(self):
        return Response(status=200)

    def changeBackground(self):
        if not self._imageFilePaths:
            self._getImages()

        # TODO: make this available for other operating systems
        nextImagePath = self._imageFilePaths.pop(0)
        subprocess.run(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", nextImagePath]
        )
        subprocess.run(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-options", "scaled"]
        )
        # TODO: check security considerations for the running this command
        self._deleteLastImage()
        self._currentImagePath = nextImagePath
        return Response(status=200)

    def backgroundImages(self):
        response = Response(json.dumps(self._imageFilePaths), mimetype="json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    def currentImage(self):
        response = Response(json.dumps(self._currentImagePath), mimetype="json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    def _getImages(self):
        imgurImages = self._imageController.requestNewImages()
        for imgurImage in imgurImages:
            self._downloadImage(imgurImage)

    def _downloadImage(self, imgurImage):
        response = requests.get(imgurImage.imageURL, stream=True)
        fileName = self.getFilePath(imgurImage.imageTitle)
        with open(self.getFilePath(fileName), "wb") as imageFile:
            shutil.copyfileobj(response.raw, imageFile)
            self._imageFilePaths.append(fileName)

    def _deleteLastImage(self):
        if not self._currentImagePath:
            return

        try:
            os.remove(self._currentImagePath)
        except Exception:
            print("Could not delete file")

    def getFilePath(self, fileName):
        return os.path.join(self.directoryPath, fileName)

    def addExistingImagesToList(self):
        """ Add any images to the path that already exist
        """
        imageFilePaths = list(map(self.getFilePath, os.listdir(self.directoryPath)))
        self._imageFilePaths = list(filter(lambda filePath: "gitkeep" not in filePath, imageFilePaths))

    @property
    def directoryPath(self):
        return "/home/jack/Documents/Python/autoDesktopChanger/backgroundImages"


def startFileHandlerServer(imageController):
    fileHandler = FileHandler(imageController)
    fileHandler.run(port=PORT)
