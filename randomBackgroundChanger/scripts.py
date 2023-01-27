
import argparse
import sys
from abc import ABC, abstractmethod

from randomBackgroundChanger.fileHandler.fileHandler import (
    GSettingsHTTPBackgroundChanger, PORT, WebFileHandler
)
from randomBackgroundChanger.fileHandler.WSGIFileHandler import WSGIFileHandler
from randomBackgroundChanger.fileHandler.fileHandlerClient import FileHandlerClient
from randomBackgroundChanger.imgur.imgur import ImgurController
from randomBackgroundChanger.imgur.imgurAuthenticator import PinImgurAuthenticator


class BasicArgsParser(ABC):

    def __init__(self):
        self._args = None

    @property
    @abstractmethod
    def Parser(self):
        pass

    @abstractmethod
    def createInstance(self):
        pass

    def parseArguments(self, *args):
        self.Parser.add_argument(
            "--clientId", required=True,
            help="The client ID that can be found in the settings of your Imgur account"
        )
        self.Parser.add_argument(
            "--clientSecret", required=True,
            help="The client secret that can be found in the settings of your Imgur account"
        )
        self._args = self.Parser.parse_args(*args)
        self.createInstance()


class StartFilerServer(BasicArgsParser, ABC):

    def __init__(self):
        super().__init__()
        self._server = None
        self._imgurController = None
        self._imgurAuthenticator = None
        self._parser = argparse.ArgumentParser(description="Start File Handler")

    @property
    def Parser(self):
        return self._parser

    @abstractmethod
    def startFileHandler(self):
        pass

    @abstractmethod
    def getArgs(self, parser, *args):
        pass


class HTTPFileHandlerServer(StartFilerServer):

    def createInstance(self):
        self._imgurAuthenticator = PinImgurAuthenticator(self._args.clientId, self._args.clientSecret)
        self._imgurController = ImgurController(self._imgurAuthenticator)
        fileHandler = GSettingsHTTPBackgroundChanger(self._imgurController)
        self._server = WebFileHandler(fileHandler, self._args.clientId, self._args.clientSecret)


class FileServerStarter(HTTPFileHandlerServer):

    def startFileHandler(self):
        self.parseArguments(sys.argv[1:])
        wsgiSever = WSGIFileHandler(self._server)
        wsgiSever.run()

    def getArgs(self, parser, *args):
        return parser.parse_args(args)


def startFileHandler():
    productionServer = FileServerStarter()
    return productionServer.startFileHandler()


class FileHandlerClientParser(BasicArgsParser, ABC):

    def __init__(self):
        super().__init__()
        self.client = None

    def startClient(self, *args):
        self.parseArguments(*args)
        self.createInstance()

    def createInstance(self):
        self.client = FileHandlerClient(
            PORT, self._args.clientId, self._args.clientSecret
        )


class FileHandlerClientChangeBackgroundParser(FileHandlerClientParser):

    def __init__(self):
        super().__init__()
        self._parser = argparse.ArgumentParser(description="Update Background Image")

    @property
    def Parser(self):
        return self._parser


class FileHandlerClientAddPinParser(FileHandlerClientParser):

    def __init__(self):
        super().__init__()
        self.pin = None
        self._parser = argparse.ArgumentParser(description="Set Imgur Auth Pin")

    def createInstance(self):
        super().createInstance()
        self.pin = self._args.pin

    @property
    def Parser(self):
        return self._parser

    def parseArguments(self, *args):
        self.Parser.add_argument(
            "--pin", required=True,
            help="The pin used to authorise the Imgur account"
        )
        super().parseArguments(*args)


def updateBackgroundImage():
    parser = FileHandlerClientChangeBackgroundParser()
    parser.startClient(sys.argv[1:])
    parser.client.nextBackgroundImage()


def addImgurPin():
    parser = FileHandlerClientAddPinParser()
    parser.startClient(sys.argv[1:])
    parser.client.addPin(parser.pin)
