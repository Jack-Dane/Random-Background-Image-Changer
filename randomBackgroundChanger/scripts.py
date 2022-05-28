
import argparse

from randomBackgroundChanger.fileHandler.fileHandler import startFileHandlerServer, PORT
from randomBackgroundChanger.fileHandler.fileHandlerClient import FileHandlerClient
from randomBackgroundChanger.imgur.imgur import ImgurController
from randomBackgroundChanger.imgur.imgurAuthenticator import ImgurAuthenticator


def startFileHandler():
    parser = argparse.ArgumentParser(description="Start File Handler")
    parser.add_argument(
        "--clientId", required=True,
        help="The client ID that can be found in the settings of your Imgur account"
    )
    parser.add_argument(
        "--clientSecret", required=True,
        help="The client secret that can be found in the settings of your Imgur account"
    )
    args = parser.parse_args()
    imgurAuthenticator = ImgurAuthenticator(args.clientId, args.clientSecret)
    imgurController = ImgurController(imgurAuthenticator)
    startFileHandlerServer(imgurController)


def updateBackgroundImage():
    client = FileHandlerClient(PORT)
    client.nextBackgroundImage()
