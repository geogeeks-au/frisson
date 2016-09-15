from tests import *
from os import remove, path

from frisson.frisson import convert_to_tiff, add_overviews 

class TestPrintPoint(unittest.TestCase):

    #@pytest.mark.xfail
    def test_convert_to_tiff(self):
        self.assertEquals(convert_to_tiff("tests/cons 1636 item 3706.tif", "tests/test_output.tif"), 0)


    def test_convert_overview(self):
        self.assertEquals(add_overviews("tests/test_output.tif"), 0)

    @pytest.mark.xfail
    def test_make_point(self):
        point = add_overviews()

    def tearDown(self):
        if path.isfile("tests/test_output.tif"):
            remove("tests/test_output.tif")

