from contextlib import contextmanager

import requests


class FileHandlerClient:

    def __init__(self, port, clientId, clientSecret):
        self._port = port
        self._clientId = clientId
        self._clientSecret = clientSecret
        self._token = None

    @contextmanager
    def _withAuth(self):
        """ Create temporary token
        """
        try:
            tokenRequest = requests.post(
                f"http://localhost:{self._port}/token",
                json={
                    "clientId": self._clientId,
                    "clientSecret": self._clientSecret
                }
            )
            self._token = tokenRequest.json().get("token")
            yield
        finally:
            requests.delete(
                f"http://localhost:{self._port}/token",
                json={
                    "clientId": self._clientId,
                    "clientSecret": self._clientSecret,
                    "token": self._token
                }
            )

    def _sendRequest(self, url, json=None):
        json = json if json else {}
        with self._withAuth():
            response = requests.post(
                url=url, json=json, headers={"Authorization": f"Bearer: {self._token}"}
            )
            response.raise_for_status()

    def nextBackgroundImage(self):
        self._sendRequest(
            f"http://localhost:{self._port}/change-background"
        )

    def addPin(self, pin):
        self._sendRequest(
            f"http://localhost:{self._port}/imgur-pin", json={"pin": pin}
        )
