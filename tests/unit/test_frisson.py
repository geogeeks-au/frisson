from tests import *

from frisson.frisson import canonise_map, add_overviews 

class TestPrintPoint(unittest.TestCase):

    @pytest.mark.xfail
    def test_canonise_map(self):
        canonise_map()

    @pytest.mark.xfail
    def test_make_point(self):
        point = add_overviews()

