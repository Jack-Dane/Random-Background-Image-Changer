
import requests


class ImgurController:

    def __init__(self, authorisationToken):
        self.authorisationToken = authorisationToken

    def _makeRequest(self, url, data=None):
        headers = {"Authorization": f"Bearer {self.authorisationToken}"}
        response = requests.get(url, data, headers=headers)
        response.raise_for_status()
        return response

    def requestNewImages(self):
        requestURL = "https://api.imgur.com/3/gallery/random/random/0"
        response = self._makeRequest(requestURL)
        imagesURLs = ImgurController._parseImageUrls(response.json())
        return imagesURLs

    @staticmethod
    def _parseImageUrls(responseData):
        imageURLs = []
        for imageResponse in responseData["data"]:
            imageURLs.append(imageResponse["link"])
        return imageURLs

    def refreshToken(self):
        pass
