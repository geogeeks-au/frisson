# from osgeo import gdal
# from osgeo import ogr
from subprocess import call
from os import environ, path


# https://docs.python.org/2/library/subprocess.html
# subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False)

# $GDAL_PATH/gdal_translate $INPUTFILE -outsize $DEST_WIDTH $DESTHEIGHT \ 
# -co COMPRESS=DEFLATE -co PHOTOMETRIC=RGB -co PROFILE=BASELINE $OUTPUT_TIF

def convert_to_tiff(filename, output_filename):
    args = [path.join(environ["GDAL_HOME"], "gdal_translate"),
            filename,
            "-outsize",
            "1000", "1000",
            "-co", "COMPRESS=DEFLATE",
            "-co", "PHOTOMETRIC=RGB",
            "-co", "PROFILE=BASELINE",
            output_filename]
    return call(args)


def add_overviews(filename):
    args = [path.join(environ["GDAL_HOME"], "gdaladdo"),
            "-r",
            "average",
            filename,
            "2",
            "4",
            "8",
            "16",
            "32",
            "64"]
    return call(args)


def create_mask_vectors(output_filename, input_filename):
    """
    $GDAL_PATH / gdaltindex - write_absolute_path $OUTPUT_INDEX_SHAPEFILE $INPUT_FOLDER / *.$EXT
    :return:
    """
    args = [path.join(environ["GDAL_HOME"], "gdaltindex"),
            "-write_absolute_path",
            output_filename,
            input_filename
            ]
    return call(args)


def _points_to_string(gcp_points):
    """
    Converts a list of GCP points to a gdal_translate gcp argument string
    :param gcp_points: A list of GCP tuples
    :return: A list of formatted strings
    """
    gcp_s = []
    for gcp in gcp_points:
        assert type(gcp) in [list, tuple]
        assert len(gcp) == 4
        gcp_s.append(["-gcp"])
        coords = []
        for coord in gcp:
            if type(coord) == float:
                coord = str(coord)
            coords.append(coord)

        gcp_s[-1].append(" ".join(coords))
    return gcp_s


def add_mask(input_filename, output_filename, mask_vectors):
    """
    gdal_translate -of GTiff -gcp 1989.12 2999.84 1.28952e+07 -3.75616e+06 -gcp 4083.48 3103.33 1.28981e+07 -3.75636e+06 -gcp 4108.23 2151.34 1.28982e+07 -3.755e+06 "/Users/Drogon/Repos/frisson/tests/cons 1636 item 3706.tif" "/var/folders/nd/k10412g92s1bk7rll01d59y40000gn/T/cons 1636 item 3706.tif"
    gdalwarp -r near -order 1 -co COMPRESS=NONE  "/var/folders/nd/k10412g92s1bk7rll01d59y40000gn/T/cons 1636 item 3706.tif" "/Users/Drogon/Repos/frisson/tests/cons 1636 item 3706_testref.tif"
    $GDAL_PATH/gdal_translate -a_srs '+init=epsg:4326' -of VRT \
$CONVERTED_TIF $VIRTUAL_WARPED.vrt $MAGIC_GCP_STRING
    mask_vectors should be a list of tuples (x,y,long,lat)
    """
    args = [path.join(environ["GDAL_HOME"], "gdal_translate"),
            "-a_srs",
            "+init=epsg:4326",
            "-of",
            "VRT"] + [x for y in _points_to_string2(mask_vectors) for x in y] + [
            input_filename,
            output_filename,
            ]
    print(args)
    return call(args)


def virtual_georeference(filename, control_points):
    pass


def georeference(filename, control_points, opts):
    pass


def get_map_bbbox(filename):
    pass
