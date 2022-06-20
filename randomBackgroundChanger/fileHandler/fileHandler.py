
import json
import os
import subprocess
import shutil
import requests
from flask import Flask, Response
from abc import ABC, abstractmethod

PORT = 5000


class FileHandler:

    def __init__(self, imgurController, *args, **kwargs):
        self._imageFilePaths = []
        self._currentImagePath = None
        self._imageController = imgurController
        self._addExistingImagesToList()

    def cycleBackgroundImage(self):
        """ Change the background to the next image in the queue
        """
        if not self._imageFilePaths:
            self.getImages()

        nextImagePath = self._imageFilePaths.pop(0)
        self._deleteLastImage()
        self._currentImagePath = nextImagePath

    def getImages(self):
        """ Request new image URLs from the image controller
        """
        imgurImages = self._imageController.requestNewImages()
        for imgurImage in imgurImages:
            self._downloadImage(imgurImage)

    def _downloadImage(self, imgurImage):
        response = requests.get(imgurImage.imageURL, stream=True)
        fileName = self.getFilePath(imgurImage.imageTitle)
        with open(fileName, "wb") as imageFile:
            shutil.copyfileobj(response.raw, imageFile)
        self._imageFilePaths.append(fileName)

    def _deleteLastImage(self):
        if not self._currentImagePath:
            return

        try:
            os.remove(self._currentImagePath)
        except Exception as e:
            print("Could not delete file")
            print(str(e))

    def getFilePath(self, fileName):
        return os.path.join(self.directoryPath, fileName)

    def _checkCurrentImageNotInFilePaths(self):
        if self._currentImagePath in self._imageFilePaths:
            self._imageFilePaths.remove(self._currentImagePath)
        else:
            # We don't want to delete a file the user has added only the random ones
            self._currentImagePath = None

    def _addExistingImagesToList(self):
        """ Add any images to the path that already exist
        """
        imageFilePaths = list(map(self.getFilePath, os.listdir(self.directoryPath)))
        self._imageFilePaths = list(filter(lambda filePath: "gitkeep" not in filePath, imageFilePaths))

    @property
    def directoryPath(self):
        return os.path.join(os.getcwd(), "backgroundImages")


class HTTPFileHandler(FileHandler, Flask):

    def __init__(self, imgurController, *args, **kwargs):
        FileHandler.__init__(self, imgurController, *args, **kwargs)
        Flask.__init__(self, __name__, *args, **kwargs)

        self.add_url_rule("/", view_func=self.homePage, methods=["GET"])
        self.add_url_rule("/change-background", view_func=self.changeBackground, methods=["POST", "GET"])
        self.add_url_rule("/current-image", view_func=self.currentImage, methods=["GET"])

    def homePage(self):
        return Response(status=200)

    def changeBackground(self):
        self.cycleBackgroundImage()
        response = Response(status=200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    def currentImage(self):
        response = Response(json.dumps(self._currentImagePath), mimetype="json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class BackgroundChangerBase(ABC, HTTPFileHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCurrentBackgroundImagePath()
        self._checkCurrentImageNotInFilePaths()

    def cycleBackgroundImage(self):
        super().cycleBackgroundImage()
        self.changeBackgroundImage()

    @abstractmethod
    def setCurrentBackgroundImagePath(self):
        pass

    @abstractmethod
    def changeBackgroundImage(self):
        pass


class GSettingsHTTPBackgroundChanger(BackgroundChangerBase):

    def setCurrentBackgroundImagePath(self):
        backgroundPathProcess = subprocess.run(
            ["/usr/bin/gsettings", "get", "org.gnome.desktop.background", "picture-uri"],
            capture_output=True
        )
        self._currentImagePath = backgroundPathProcess.stdout.decode().split("'")[1]

    def changeBackgroundImage(self):
        subprocess.run(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", self._currentImagePath]
        )
        subprocess.run(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-options", "scaled"]
        )


def startFileHandlerServer(imageController):
    fileHandler = GSettingsHTTPBackgroundChanger(imageController)
    fileHandler.run(port=PORT)
