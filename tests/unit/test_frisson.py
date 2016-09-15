from tests import *
from os import remove

from frisson.frisson import convert_to_tiff, add_overviews 

class TestPrintPoint(unittest.TestCase):

    #@pytest.mark.xfail
    def test_convert_to_tiff(self):
        assert 0 == convert_to_tiff("tests/cons 1636 item 3706.tif", "tests/test_output.tif")
        remove("tests/test_output.tif")

    @pytest.mark.xfail
    def test_make_point(self):
        point = add_overviews()

