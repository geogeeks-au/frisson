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
        for coord in gcp:
            if type(coord) == float:
                coord = str(coord)
            gcp_s[-1].append(coord)
    return gcp_s


def add_mask(input_filename, output_filename, mask_vectors):
    """
    $GDAL_PATH/gdal_translate -a_srs '+init=epsg:4326' -of VRT \
    $CONVERTED_TIF $VIRTUAL_WARPED.vrt $MAGIC_GCP_STRING
    """
    pass


def virtual_georeference(input_filename, output_filename, control_points):
    """
    Performs the virtual georeferencing using gdal translate
    :param input_filename:
    :param output_filename:
    :param control_points: should be a list of tuples (x,y,long,lat)
    :return: 0 return code for success
    """
    args = [path.join(environ["GDAL_HOME"], "gdal_translate"),
            "-a_srs",
            "+init=epsg:4326",
            "-of",
            "VRT"] + [x for y in _points_to_string(control_points) for x in y] + [
               input_filename,
               output_filename,
           ]
    return call(args)


def georeference(filename, control_points, opts):
    """
    $GDAL_PATH/gdalwarp $MEMORY_LIMIT $TRANSFORM_OPTION $RESAMPLE_OPTION \
    -dstalpha $MASK_OPTIONS -s_srs 'EPSG:4326' $VIRTUAL_WARPED.vrt \
    $REAL_WARPED_TIF -co TILED=YES -co COMPRESS=LZW
    :param filename:
    :param control_points:
    :param opts:
    :return:
    """
    pass


def get_map_bbbox(filename):
    pass
