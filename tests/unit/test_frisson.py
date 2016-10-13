from tests import *
from os import remove, path

from frisson.frisson import (
    convert_to_tiff,
    add_overviews,
    create_tile_index,
    virtual_georeference,
    _points_to_string,
    georeference,
    get_map_bbbox,
    add_mask
)


class TestPrintPoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gcp_points = [
            [1991.5184954376359201,3000.20271501503793843, 115.83883775684209638,-31.94554601339920907],
            [3211.51960671375672973, 3078.3775435045758968, 115.85439400036874247, -31.94675219309830183],
            [2542.09731250744516728, -1049.31538631206467471, 115.84633294756488908, -31.92436589497924615],
        ]
        cls.gcp_string = [
            ['-gcp', '1991.51849544', '3000.20271502', '115.838837757', '-31.9455460134'],
            ['-gcp', '3211.51960671', '3078.3775435', '115.854394', '-31.9467521931'],
            ['-gcp', '2542.09731251', '-1049.31538631', '115.846332948', '-31.924365895']
        ]

    def test_input_exists(self):
        self.assertTrue(path.isfile("tests/test_1636.tif"), "Test File doesn't exist")

    # @pytest.mark.xfail
    def test_convert_to_tiff(self):
        self.assertEquals(convert_to_tiff("tests/test_1636.tif",
                                          "tests/test_output.tif"),
                          0,
                          "Couldn't convert tiff")

    def test_outtif_exists(self):
        self.assertTrue(path.isfile("tests/test_output.tif"),
                        "Output tiff File doesn't exist")

    def test_convert_overview(self):
        self.assertEquals(add_overviews("tests/test_output.tif"), 0,
                          "Couldn't create overview")

    def test_add_mask(self):
        # TODO: Or this one
        if path.exists("tests/test_mask.gml"):
            self.assertEquals(add_mask("tests/test_mask.gml", "features", "tests/test_output_clipped.tif"), 0,
                          "Couldn't add mask index")
        return True

    def test_virtual_georeference(self):
        self.assertEquals(virtual_georeference("tests/test_output.tif",
                                   "tests/test_output.vrt",
                                   self.gcp_points), 0,
                          "Couldn't add mask")

    #TODO: Create georeference with masking

    def test_gcp_string(self):
        self.assertEquals(_points_to_string(self.gcp_points),
                          self.gcp_string
                          )

    def test_georeference(self):
        output = "tests/test_output_referenced.tif"
        if path.exists(output):
            remove(output)
        opts = {"RESAMPLE_OPTION": "average"}
        self.assertEquals(
            georeference("tests/test_output.vrt",
                         output,
                         self.gcp_string,
                         opts), 0
        )

    def test_tile_index(self):
        # TODO: Not 100% on this one
        if path.exists("tests/test_output_referenced.tif"):
            self.assertEquals(create_tile_index("tests/test_output.shp", "tests/test_output_referenced.tif"), 0,
                          "Couldn't create shapefile index")
        return True

    def test_map_bbox(self):
        self.assertEquals(get_map_bbbox("tests/test_output_referenced.tif"),
                          ['Lower Left  ( 115.8136615, -31.9342700) (115d48\'49.18"E, 31d56\' 3.37"S)',
                           'Upper Right ( 115.8265317, -31.9282996) (115d49\'35.51"E, 31d55\'41.88"S)'])

    @classmethod
    def tearDownClass(self):
        test_files = [
            "tests/test_output.tif",
            "tests/test_output.dbf",
            "tests/test_output.shp",
            "tests/test_output.shx",
            "tests/test_output.vrt",
            "tests/test_output_masked.tif",
            "test_output_referenced.tif",
            "test_output_referenced.tif.aux.xml"
        ]
        for tf in test_files:
            if path.isfile(tf):
                #remove(tf)
                pass