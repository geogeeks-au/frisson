from tests import *
from os import remove, path

from frisson.frisson import (
    convert_to_tiff,
    add_overviews,
    create_mask_vectors
)


class TestPrintPoint(unittest.TestCase):
    def test_input_exists(self):
        self.assertTrue(path.isfile("tests/cons 1636 item 3706.tif"), "Test File doesn't exist")

    # @pytest.mark.xfail
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

    def test_shapefile_index(self):
        # TODO: Not 100% on this one
        self.assertEquals(create_mask_vectors("tests/test_output.shp", "tests/test_output.tif"), 0,
                          "Couldn't create shapefile index")

    def tearDown(self):
        if path.isfile("tests/test_output.tif"):
            pass
            # remove("tests/test_output.tif")
