
import argparse

from randomBackgroundChanger.fileHandler.fileHandler import FileHandler
from randomBackgroundChanger.imgur.imgur import ImgurController


def startFileHandler():
    parser = argparse.ArgumentParser(description="Start File Handler")
    parser.add_argument(
        "-A", "--accessToken", required=True,
        help="Authorisation token that should be generated using https://api.imgur.com/oauth2#authorization"
    )

    args = parser.parse_args()
    imgurController = ImgurController(args.accessToken)
    fileHandler = FileHandler(imgurController)
    fileHandler.run()


def updateBackgroundImage():
    print("Update background image")
