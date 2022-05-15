
import os
import subprocess
import shutil
import requests
from flask import Flask, Response


class FileHandler(Flask):

    def __init__(self, imgurController, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)
        self._imageFilePaths = []
        self._currentImagePath = None
        self._imageController = imgurController

        self.add_url_rule("/change-background", view_func=self.changeBackground, methods=["POST", "GET"])

    def changeBackground(self):
        if not self._imageFilePaths:
            self._getImages()

        # TODO: make this available for other operating systems
        nextImagePath = self._imageFilePaths.pop(0)
        subprocess.run(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", nextImagePath],
        )
        # TODO: check security considerations for the running this command
        self._deleteLastImage()
        self._currentImagePath = nextImagePath
        return Response(status=200)

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
            os.remove(self.getFilePath(self._currentImagePath))
        except Exception:
            print("Could not delete file")

    def getFilePath(self, fileName):
        return os.path.join(self.directoryPath, fileName)

    @property
    def directoryPath(self):
        return "/home/jack/Documents/Python/autoDesktopChanger/backgroundImages"


def startFileHandlerServer(imageController):
    fileHandler = FileHandler(imageController)
    fileHandler.run()
