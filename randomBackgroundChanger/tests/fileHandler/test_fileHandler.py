
from unittest import TestCase
from unittest.mock import call, patch, MagicMock, PropertyMock

from randomBackgroundChanger.fileHandler.fileHandler import (
    FileHandler, AlreadyDownloadingImagesException, HTTPFileHandler,
    HTTPAuthenticator
)
from randomBackgroundChanger.imgur.imgur import ImgurImage

MODULE_PATH = "randomBackgroundChanger.fileHandler.fileHandler."


@patch.object(FileHandler, "_deleteLastImage")
@patch.object(FileHandler, "getImages")
class Test_FileHandler_cycleBackgroundImage(TestCase):

    def setUp(self):
        self.fileHandler = FileHandler(MagicMock())

    def test_ok(self, FileHandler_getImages, FileHandler_deleteLastImage):
        type(self.fileHandler).imageFilePaths = PropertyMock(return_value=["/foo/bar", "/bar/foo"])

        self.fileHandler.cycleBackgroundImage()

        FileHandler_getImages.assert_not_called()
        FileHandler_deleteLastImage.assert_called_once_with()
        FileHandler_deleteLastImage.assert_called_once_with()

    def test_locked(self, FileHandler_getImages, FileHandler_deleteLastImage):
        self.fileHandler._downloadingImages.acquire()
        type(self.fileHandler).imageFilePaths = PropertyMock(return_value=["/foo/bar"])

        with self.assertRaises(AlreadyDownloadingImagesException):
            self.fileHandler.cycleBackgroundImage()

    def test_no_image_files(self, FileHandler_getImages, FileHandler_deleteLastImage):
        type(self.fileHandler).imageFilePaths = PropertyMock(return_value=[])

        self.fileHandler.cycleBackgroundImage()

        FileHandler_getImages.assert_called_once_with()
        FileHandler_deleteLastImage.assert_called_once_with()


@patch(f"{MODULE_PATH}Process")
@patch.object(FileHandler, "getFilePath")
class Test_FileHandler_getImages(TestCase):

    def test_ok(self, FileHandler_getFilePath, Process):
        imgurController = MagicMock()
        imgurController.requestNewImages.return_value = [
            ImgurImage("ImageTitle1", "https://imgur/123", "image/png"),
            ImgurImage("ImageTitle2", "https://imgur/234", "image/jpeg")
        ]
        FileHandler_getFilePath.side_effect = lambda title: f"/foo/bar/{title}"
        fileHandler = FileHandler(imgurController)

        fileHandler.getImages()

        Process.assert_has_calls(
            [
                call(target=fileHandler._downloadImage, args=(imgurController.requestNewImages.return_value[0],)),
                call().start(),
                call(target=fileHandler._downloadImage, args=(imgurController.requestNewImages.return_value[1],)),
                call().start(),
                call().join(),
                call().join(),
            ]
        )


@patch(f"{MODULE_PATH}FileHandler.directoryPath", return_value="/foo/bar/directory")
@patch(f"{MODULE_PATH}requests")
@patch(f"{MODULE_PATH}shutil")
@patch(f"{MODULE_PATH}open")
class Test_FileHandler__downloadImage(TestCase):

    def test_ok(self, open, shutil, requests, FileHandler_directoryPath):
        fileHandler = FileHandler(MagicMock)
        open.return_value.__enter__.return_value = "File"
        requests.get.return_value = MagicMock(raw="Image Data")

        fileHandler._downloadImage(
            MagicMock(imageURL="imageURL", imageTitle="imageTitle")
        )

        requests.get.assert_called_once_with("imageURL", stream=True)
        shutil.copyfileobj.assert_called_once_with("Image Data", "File")


@patch(f"{MODULE_PATH}os")
class Test_FileHandler__deleteLastImage(TestCase):

    def setUp(self):
        self.fileHandler = FileHandler(MagicMock())

    def test_ok(self, os):
        type(self.fileHandler).imageFilePaths = PropertyMock(return_value=["/foo/bar", "/bar/foo"])
        type(self.fileHandler).currentBackgroundImage = PropertyMock(return_value="/foo/bar")

        self.fileHandler._deleteLastImage()

        print(os.remove.mock_calls)
        os.remove.assert_called_once_with("/foo/bar")

    def test_no_current_image(self, os):
        type(self.fileHandler).imageFilePaths = PropertyMock(return_value=[])

        # assert doesn't raise an exception
        self.fileHandler._deleteLastImage()

    @patch(f"{MODULE_PATH}print")
    def test_exception(self, print, os):
        type(self.fileHandler).imageFilePaths = PropertyMock(return_value=["/foo/bar", "/bar/foo"])
        os.remove.side_effect = FileNotFoundError("File Not Found")

        self.fileHandler._deleteLastImage()

        print.assert_has_calls(
            [
                call("Could not delete file"),
                call("File Not Found")
            ]
        )

    def test_image_not_downloaded_by_imgur(self, os):
        type(self.fileHandler).imageFilePaths = PropertyMock(return_value=["/foo/bar", "/bar/foo"])
        type(self.fileHandler).currentBackgroundImage = PropertyMock(return_value=["/foo/baz"])

        self.fileHandler._deleteLastImage()

        os.remove.assert_not_called()


@patch.object(FileHandler, "__init__")
@patch.object(HTTPAuthenticator, "__init__")
@patch.object(HTTPFileHandler, "add_url_rule")
@patch.object(HTTPFileHandler, "currentBackgroundImage", new_callable=PropertyMock(return_value="file_path"))
@patch("builtins.open", new_callable=MagicMock(), read_data="data")
@patch(MODULE_PATH + "hashlib")
class Test_HTTPFileHandler__getCurrentImageHash(TestCase):

    def test_ok(
            self, hashlib_, open_, currentBackgroundImage, HTTPFileHandler_add_url_rule,
            HTTPAuthenticator__init__, FileHandler__init__
    ):
        readMock = MagicMock(side_effect=["a", "b", "c", None])
        open_.return_value.__enter__.return_value.read = readMock
        httpFileHandler = HTTPFileHandler(
            MagicMock(), "clientId", "clientSecret"
        )

        hash_ = httpFileHandler._getCurrentImageHash()

        self.assertEqual(4, readMock.call_count)
        self.assertEqual(
            [call("a"), call("b"), call("c")],
            hashlib_.sha1.return_value.update.mock_calls
        )
        self.assertEqual(
            hash_, hashlib_.sha1.return_value.hexdigest.return_value
        )
