
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

import requests

from randomBackgroundChanger.imgur.imgur import ImgurController

MODULE_PATH = "randomBackgroundChanger.imgur.imgur."


class Test_ImgurController__parseImageUrls(TestCase):

    def test_singular_images(self):
        responseData = {
            "data": [
                {
                    "title": "imageTitle1",
                    "type": "image/jpeg",
                    "link": "https://www.imgur.com/imageTitle1",
                },
                {
                    "title": "imageTitle2",
                    "type": "image/png",
                    "link": "https://www.imgur.com/imageTitle2",
                }
            ]
        }

        parsedImages = ImgurController._parseImageUrls(responseData)

        counter = 0
        for image in parsedImages:
            self.assertEqual(responseData["data"][counter]["title"], image.imageTitle)
            self.assertEqual(responseData["data"][counter]["type"], image.imageFileType)
            self.assertEqual(responseData["data"][counter]["link"], image.imageURL)
            counter += 1
        self.assertEqual(2, len(parsedImages))

    def test_multiple_images(self):
        responseData = {
            "data": [
                {
                    "title": "imageTitle1",
                    "type": "image/jpeg",
                    "link": "https://www.imgur.com/imageTitle1",
                    "images": [
                        {
                            "title": "imageSubTitle1",
                            "type": "image/png",
                            "link": "https://www.imgur.com/imageSubTitle1"
                        }
                    ]
                },
                {
                    "title": "imageTitle2",
                    "type": "image/png",
                    "link": "https://www.imgur.com/imageTitle2",
                    "images": [
                        {
                            "title": "imageSubTitle2",
                            "type": "image/gif",
                            "link": "https://www.imgur.com/imageSubTitle2"
                        },
                        {
                            "title": "imageSubTitle3",
                            "type": "image/png",
                            "link": "https://www.imgur.com/imageSubTitle1"
                        }
                    ]
                }
            ]
        }

        parsedImages = ImgurController._parseImageUrls(responseData)

        counter = 0
        for image in parsedImages:
            self.assertEqual(responseData["data"][counter]["title"], image.imageTitle)
            self.assertEqual(responseData["data"][counter]["images"][0]["type"], image.imageFileType)
            self.assertEqual(responseData["data"][counter]["images"][0]["link"], image.imageURL)
            counter += 1
        self.assertEqual(2, len(parsedImages))

    def test_ignore_videos(self):
        responseData = {
            "data": [
                {
                    "title": "imageTitle1",
                    "type": "video/jpeg",
                    "link": "https://www.imgur.com/imageTitle1",
                },
                {
                    "title": "imageTitle2",
                    "type": "image/png",
                    "link": "https://www.imgur.com/imageTitle2",
                }
            ]
        }

        parsedImages = ImgurController._parseImageUrls(responseData)

        counter = 0
        for image in parsedImages:
            if counter == 0:
                continue
            self.assertEqual(responseData["data"][counter]["title"], image.imageTitle)
            self.assertEqual(responseData["data"][counter]["type"], image.imageFileType)
            self.assertEqual(responseData["data"][counter]["link"], image.imageURL)
            counter += 1
        self.assertEqual(1, len(parsedImages))


@patch(f"{MODULE_PATH}requests")
class Test_ImgurController__makeRequest(TestCase):

    def test_ok(self, mockRequests):
        mockRequests.HTTPError = requests.HTTPError
        data = {"testData": "testData1"}
        expectedHeaders = {"Authorization": f"Bearer accessToken123"}
        imgurAuthenticator = MagicMock(accessToken="accessToken123")
        imgurController = ImgurController(imgurAuthenticator)

        imgurController._makeRequest("http://api.imgur/endpoint", data=data)

        mockRequests.get.assert_called_once_with(
            "http://api.imgur/endpoint", data, headers=expectedHeaders
        )
        imgurAuthenticator.refreshToken.assert_not_called()

    def test_refresh_success(self, mockRequests):
        mockRequests.HTTPError = requests.HTTPError
        data = {"testData": "testData1"}
        expectedHeaders = {"Authorization": f"Bearer accessToken123"}
        imgurAuthenticator = MagicMock(accessToken="accessToken123")
        imgurController = ImgurController(imgurAuthenticator)
        mockRequests.get.return_value.raise_for_status.side_effect = [requests.HTTPError, None]

        imgurController._makeRequest("http://api.imgur/endpoint", data=data)

        mockRequests.get.assert_has_calls(
            [
                call("http://api.imgur/endpoint", data, headers=expectedHeaders),
                call().raise_for_status(),
                call("http://api.imgur/endpoint", data, headers=expectedHeaders),
                call().raise_for_status()
            ]
        )
        imgurAuthenticator.refreshToken.assert_called_once_with()

    def test_refresh_failure(self, mockRequests):
        mockRequests.HTTPError = requests.HTTPError
        data = {"testData": "testData1"}
        expectedHeaders = {"Authorization": f"Bearer accessToken123"}
        imgurAuthenticator = MagicMock(accessToken="accessToken123")
        imgurController = ImgurController(imgurAuthenticator)
        mockRequests.get.return_value.raise_for_status.side_effect = requests.HTTPError

        with self.assertRaises(requests.HTTPError):
            imgurController._makeRequest("http://api.imgur/endpoint", data=data)

        mockRequests.get.assert_has_calls(
            [
                call("http://api.imgur/endpoint", data, headers=expectedHeaders),
                call().raise_for_status(),
                call("http://api.imgur/endpoint", data, headers=expectedHeaders),
                call().raise_for_status()
            ]
        )
        imgurAuthenticator.refreshToken.assert_called_once_with()
