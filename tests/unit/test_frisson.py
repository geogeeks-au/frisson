from tests import *
from os import remove, path

from frisson.frisson import convert_to_tiff, add_overviews 

class TestPrintPoint(unittest.TestCase):

    def test_input_exists(self):
        self.assertTrue(path.isfile("tests/cons 1636 item 3706.tif"), "Test File doesn't exist")

    #@pytest.mark.xfail
    def test_convert_to_tiff(self):
        self.assertEquals(convert_to_tiff("tests/cons 1636 item 3706.tif",
                                          "tests/test_output.tif"),
                          0,
                          "Couldn't convert tiff")

    def test_outtif_exists(self):
        self.assertTrue(path.isfile("tests/test_output.tif"),
                        "Output tiff File doesn't exist")

    def test_convert_overview(self):
        self.assertEquals(add_overviews("tests/test_output.tif"), 0,
                          "Couldn't create overview")


    def tearDown(self):
        if path.isfile("tests/test_output.tif"):
            pass
            #remove("tests/test_output.tif")

