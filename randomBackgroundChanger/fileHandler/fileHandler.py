
import subprocess
from flask import Flask, Response


class FileHandler(Flask):

    def __init__(self, imgurController, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)
        self._imageFilePaths = []
        self._imageController = imgurController

        self.add_url_rule("/change-background", view_func=self.changeBackground, methods=["POST"])

    def changeBackground(self):
        if not self._imageFilePaths:
            self._getImages()

        print(self._imageFilePaths)

        # TODO: make this available for other operating systems
        nextImagePath = self._imageFilePaths.pop(0)
        subprocess.Popen(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", nextImagePath]
        )
        return Response(status=200)

    def _getImages(self):
        self._imageFilePaths = self._imageController.requestNewImages()
