
import argparse

from randomBackgroundChanger.fileHandler.fileHandler import startFileHandlerServer, PORT
from randomBackgroundChanger.fileHandler.fileHanlderClient import FileHandlerClient
from randomBackgroundChanger.imgur.imgur import ImgurController


def startFileHandler():
    parser = argparse.ArgumentParser(description="Start File Handler")
    parser.add_argument(
        "-A", "--accessToken", required=True,
        help="Authorisation token that should be generated using https://api.imgur.com/oauth2#authorization"
    )

    args = parser.parse_args()
    imgurController = ImgurController(args.accessToken)
    startFileHandlerServer(imgurController)


def updateBackgroundImage():
    client = FileHandlerClient(PORT)
    client.nextBackgroundImage()
