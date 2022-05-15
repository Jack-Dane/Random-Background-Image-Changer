
import requests
from dataclasses import dataclass


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
            title = imageResponse["title"]
            if imageResponse.get("images"):
                # Just use the first image
                imageFileFormat = imageResponse["images"][0]["type"]
                imageLink = imageResponse["images"][0]["link"]
                imageType = imageResponse["images"][0]["type"]
            else:
                imageFileFormat = imageResponse["type"]
                imageLink = imageResponse["link"]
                imageType = imageResponse["type"]
            if not ImgurController._imageIsVideo(imageFileFormat):
                # only add images, not videos
                imageURLs.append(ImgurImage(title, imageLink, imageType))
        return imageURLs

    @staticmethod
    def _imageIsVideo(imageFileFormat):
        return "video" in imageFileFormat

    def refreshToken(self):
        pass


@dataclass
class ImgurImage:

    imageTitle: str
    imageURL: str
    imageFileType: str

    def __post_init__(self):
        invalidFileChars = ["&", "/", "<", ">", "\\", " ", "\"", "'", "."]
        for char in invalidFileChars:
            self.imageTitle = self.imageTitle.replace(char, "_")
