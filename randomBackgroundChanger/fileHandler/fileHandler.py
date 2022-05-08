
import subprocess
from flask import Flask, Response


class FileHandler(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)
        self.imageFilePaths = []

        self.add_url_rule("/change-background", view_func=self.changeBackground, methods=["POST"])

    def changeBackground(self):
        if not self.imageFilePaths:
            self._getImages()

        # TODO: make this available for other operating systems
        nextImagePath = self.imageFilePaths.pop(0)
        subprocess.Popen(
            ["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", nextImagePath]
        )
        return Response(status=200)

    def _getImages(self):
        # TODO: make a request to get the images + store the images and link to array
        ...
