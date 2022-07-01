
import argparse
import sys
from abc import ABC, abstractmethod

from randomBackgroundChanger.fileHandler.fileHandler import (
    GSettingsHTTPBackgroundChanger, PORT
)
from randomBackgroundChanger.fileHandler.fileHandlerClient import FileHandlerClient
from randomBackgroundChanger.imgur.imgur import ImgurController
from randomBackgroundChanger.imgur.imgurAuthenticator import ImgurAuthenticator


class StartFilerServer(ABC):

    def __init__(self):
        self._server = None
        self._imgurController = None
        self._imgurAuthenticator = None

    @abstractmethod
    def startFileHandler(self):
        pass

    def parseArguments(self, *args):
        parser = argparse.ArgumentParser(description="Start File Handler")
        parser.add_argument(
            "--clientId", required=True,
            help="The client ID that can be found in the settings of your Imgur account"
        )
        parser.add_argument(
            "--clientSecret", required=True,
            help="The client secret that can be found in the settings of your Imgur account"
        )
        print(args)
        args = parser.parse_args(args)
        self._imgurAuthenticator = ImgurAuthenticator(args.clientId, args.clientSecret)
        self._imgurController = ImgurController(self._imgurAuthenticator)
        self._server = GSettingsHTTPBackgroundChanger(
            self._imgurController, args.clientId, args.clientSecret
        )


class ProductionStartFileServer(StartFilerServer):

    def startFileHandler(self, *args):
        self.parseArguments(*args)
        return self._server


class DevelopmentStartFileServer(StartFilerServer):

    def startFileHandler(self):
        self.parseArguments(sys.argv[1:])
        self._server.run()


def startProductionServer(*args):
    productionServer = ProductionStartFileServer()
    return productionServer.startFileHandler(*args)


def startDevelopmentServer():
    developmentServer = DevelopmentStartFileServer()
    developmentServer.startFileHandler()


def updateBackgroundImage():
    client = FileHandlerClient(PORT)
    client.nextBackgroundImage()
