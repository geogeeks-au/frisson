from tests import *
from os import remove, path

from frisson.frisson import (
    convert_to_tiff,
    add_overviews,
    create_mask_vectors,
    virtual_georeference,
    _points_to_string,
    georeference,
    get_map_bbbox
)


class TestPrintPoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gcp_points = [
            [12895157.1042, -3756156.6509, 1989.1230, -2999.8393],
            [12898106.0028, -3756364.7068, 4083.4782, -3103.3251],
            [12898161.6258, -3754995.9836, 4108.2269, -2151.3432]
        ]
        cls.gcp_string = [
            ["-gcp", "12895157.1042",
             "-3756156.6509",
             "1989.123", "-2999.8393"],
            ["-gcp", "12898106.0028", "-3756364.7068",
             "4083.4782", "-3103.3251"],
            ["-gcp", "12898161.6258", "-3754995.9836",
             "4108.2269", "-2151.3432"]
        ]

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

    def test_virtual_georeference(self):
        self.assertEquals(virtual_georeference("tests/test_output.tif",
                                   "tests/test_output.vrt",
                                   self.gcp_points), 0,
                          "Couldn't add mask")

    def test_gcp_string(self):
        self.assertEquals(_points_to_string(self.gcp_points),
                          self.gcp_string
                          )

    def test_georeference(self):
        opts = {"MASK_OPTIONS":["17", "17", "17"],
                "RESAMPLE_OPTION":"near"}
        self.assertEquals(
            georeference("tests/test_output.vrt",
                         "tests/test_output_referenced.tif",
                         self.gcp_string,
                         opts)
        )

    def test_map_bbox(self):
        self.assertEquals(get_map_bbbox("tests/test_output_referenced.tif"),
                          0)

    @classmethod
    def tearDownClass(self):
        test_files = [
            "tests/test_output.tif",
            "tests/test_output.dbf",
            "tests/test_output.shp",
            "tests/test_output.shx",
            "tests/test_output.vrt",
        ]
        for tf in test_files:
            if path.isfile(tf):
                pass
                #remove(tf)
