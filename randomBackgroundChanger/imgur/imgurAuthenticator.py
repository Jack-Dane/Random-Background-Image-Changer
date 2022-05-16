
import requests
import webbrowser


class ImgurAuthenticator:

    def __init__(self, clientId, clientSecret):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.accessToken = None
        self.refreshToken = None
        self.pin = None

    @property
    def accessTokenURL(self):
        return "https://api.imgur.com/oauth2/token"

    @property
    def pinAuthenticationURL(self):
        return f"https://api.imgur.com/oauth2/authorize?client_id={self.clientId}&response_type=pin"

    def startAuthentication(self):
        webbrowser.open(self.pinAuthenticationURL)
        self.pin = input("Enter Pin: ")
        self.getAccessToken()

    def getAccessToken(self):
        postData = {
            "client_id": self.clientId,
            "client_secret": self.clientSecret,
            "grant_type": "pin",
            "pin": self.pin
        }
        response = requests.post(self.accessTokenURL, data=postData)
        response.raise_for_status()
        response = response.json()
        self.accessToken = response["access_token"]
        self.refreshToken = response["refresh_token"]
