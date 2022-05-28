
import requests


class FileHandlerClient:

    def __init__(self, port):
        self.port = port

    def nextBackgroundImage(self):
        changeBackgroundRequest = requests.post(f"http://localhost:{self.port}/change-background")
        changeBackgroundRequest.raise_for_status()
