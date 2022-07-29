
import requests


class FileHandlerClient:

    def __init__(self, port):
        self.port = port

    def nextBackgroundImage(self):
        changeBackgroundRequest = requests.post(
            f"http://localhost:{self.port}/change-background"
        )
        changeBackgroundRequest.raise_for_status()

    def addPin(self, pin):
        pinRequest = requests.post(
            f"http://localhost:{self.port}/imgur-pin",
            json={"pin": pin}
        )
        pinRequest.raise_for_status()
