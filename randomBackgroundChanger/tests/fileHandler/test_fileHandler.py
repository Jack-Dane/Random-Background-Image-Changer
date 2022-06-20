
from unittest import TestCase
from unittest.mock import call, patch, MagicMock

from randomBackgroundChanger.fileHandler.fileHandler import FileHandler
from randomBackgroundChanger.imgur.imgur import ImgurImage

MODULE_PATH = "randomBackgroundChanger.fileHandler.fileHandler."


@patch(f"{MODULE_PATH}os")
@patch.object(FileHandler, "_addExistingImagesToList")
class Test_FileHandler_cycleBackgroundImage(TestCase):

    def test_existing_files_no_current_image(self, FileHandler_addExistingImagesToList, os):
        fileHandler = FileHandler(MagicMock())
        fileHandler._imageFilePaths = ["foo/bar", "bar/foo"]

        fileHandler.cycleBackgroundImage()

        os.remove.assert_not_called()
        fileHandler._currentImagePath = "foo/bar"

    def test_existing_files_current_image(self, FileHandler_addExistingImagesToList, os):
        fileHandler = FileHandler(MagicMock())
        fileHandler._imageFilePaths = ["foo/bar", "bar/foo"]
        fileHandler._currentImagePath = "foo/foo"

        fileHandler.cycleBackgroundImage()

        os.remove.assert_called_once_with("foo/foo")
        fileHandler._currentImagePath = "foo/bar"

    @patch.object(FileHandler, "getImages")
    def test_no_existing_files(self, FileHandler_getImages, FileHandler_addExistingImageToList, os):
        fileHandler = FileHandler(MagicMock())
        def changeListItems(*args, **kwargs):
            # simulate the items being added to the imageFilePaths
            fileHandler._imageFilePaths = ["foo/foo", "bar/foo"]
        FileHandler_getImages.side_effect = changeListItems

        fileHandler.cycleBackgroundImage()

        FileHandler_getImages.assert_called_once_with()
        os.remove.assert_not_called()
        fileHandler._currentImagePath = "foo/foo"


@patch(f"{MODULE_PATH}requests")
@patch(f"{MODULE_PATH}shutil")
@patch(f"{MODULE_PATH}open")
@patch.object(FileHandler, "getFilePath")
@patch.object(FileHandler, "_addExistingImagesToList")
class Test_FileHandler_getImages(TestCase):

    def test_ok(
            self, FileHandler_addExistingImagesToList, FileHandler_getFilePath, open, shutil, requests
    ):
        mockManaged = MagicMock()
        mockManaged.attach_mock(shutil, "shutil")
        mockManaged.attach_mock(requests, "requests")
        imgurController = MagicMock()
        imgurController.requestNewImages.return_value = [
            ImgurImage("ImageTitle1", "https://imgur/123", "image/png"),
            ImgurImage("ImageTitle2", "https://imgur/234", "image/jpeg")
        ]
        requests.get.side_effect = [
            MagicMock(raw="abc"),
            MagicMock(raw="def")
        ]
        FileHandler_getFilePath.side_effect = lambda title: f"/foo/bar/{title}"
        open.return_value.__enter__.return_value = "MagicMockFile"
        fileHandler = FileHandler(imgurController)

        fileHandler.getImages()

        self.assertEqual(
            ["/foo/bar/ImageTitle1", "/foo/bar/ImageTitle2"],
            fileHandler._imageFilePaths
        )
        mockManaged.assert_has_calls(
            [
                call.requests.get("https://imgur/123", stream=True),
                call.shutil.copyfileobj("abc", "MagicMockFile"),
                call.requests.get("https://imgur/234", stream=True),
                call.shutil.copyfileobj("def", "MagicMockFile")
            ]
        )


@patch(f"{MODULE_PATH}os")
class Test_FileHandler__deleteLastImage(TestCase):

    def setUp(self):
        self.addExistingImagesToListPatch = patch.object(FileHandler, "_addExistingImagesToList")
        self.addExistingImagesToListPatch.start()
        self.fileHandler = FileHandler(MagicMock())

    def tearDown(self):
        self.addExistingImagesToListPatch.stop()

    def test_ok(self, os):
        self.fileHandler._currentImagePath = "/foo/bar"

        self.fileHandler._deleteLastImage()

        os.remove.assert_called_once_with("/foo/bar")

    def test_no_current_image(self, os):
        self.fileHandler._deleteLastImage()

        os.remove.assert_not_called()

    @patch(f"{MODULE_PATH}print")
    def test_exception(self, print, os):
        self.fileHandler._currentImagePath = "/foo/bar"
        os.remove.side_effect = FileNotFoundError("File Not Found")

        self.fileHandler._deleteLastImage()

        print.assert_has_calls(
            [
                call("Could not delete file"),
                call("File Not Found")
            ]
        )


@patch.object(FileHandler, "_addExistingImagesToList")
class Test_FileHandler__checkCurrentImageNotInFilePaths(TestCase):

    def test_file_in_image_file_paths(self, FileHandler_addExistingImagesToList):
        fileHandler = FileHandler(MagicMock())
        fileHandler._currentImagePath = "/foo/bar"
        fileHandler._imageFilePaths = ["/bar/foo", "/foo/bar"]

        fileHandler._checkCurrentImageNotInFilePaths()

        self.assertEqual(
            ["/bar/foo"],
            fileHandler._imageFilePaths
        )
        self.assertEqual("/foo/bar", fileHandler._currentImagePath)

    def test_file_not_in_image_file_paths(self, FileHandler_addExistingImagesToList):
        fileHandler = FileHandler(MagicMock())
        fileHandler._currentImagePath = "/foo/foo"
        fileHandler._imageFilePaths = ["/bar/foo", "/foo/bar"]

        fileHandler._checkCurrentImageNotInFilePaths()

        self.assertEqual(
            ["/bar/foo", "/foo/bar"],
            fileHandler._imageFilePaths
        )
        self.assertIsNone(fileHandler._currentImagePath)


@patch(f"{MODULE_PATH}os")
@patch.object(FileHandler, "getFilePath")
class Test_FileHandler__addExistingImagesToList(TestCase):

    def test_ok(self, FileHander_getFilePath, os):
        FileHander_getFilePath.side_effect = lambda filePath: filePath
        os.listdir.return_value = ["/foo/bar", "/bar/foo", ".gitkeep", "/bar/bar", "/foo/foo"]
        fileHandler = FileHandler(MagicMock())

        fileHandler._addExistingImagesToList()

        self.assertEqual(
            ["/foo/bar", "/bar/foo", "/bar/bar", "/foo/foo"],
            fileHandler._imageFilePaths
        )
