# from osgeo import gdal
# from osgeo import ogr
from subprocess import call, check_output
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


def add_mask(input_filename, output_filename, mask_vectors):
    """
    $GDAL_PATH/gdal_rasterize -i  -burn 17 -b 1 -b 2 -b 3 \
    $VECTOR_FILE -l $NAME_OF_VECTOR_FILE_LAYER $TARGET_TIF

    """
    args = [path.join(environ["GDAL_HOME"], "gdal_rasterize"),
            "-i",
            "-burn",
            "17",
            "-b",
            "1",
            "-b",
            "2",
            "-b",
            "3",
            "-of",
            "-l",
            mask_vectors,
            input_filename,
            output_filename,
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


def virtual_georeference(input_filename, output_filename, control_points):
    """
    Performs the virtual georeferencing using gdal translate
    $GDAL_PATH/gdal_translate -a_srs '+init=epsg:4326' -of VRT \
    $CONVERTED_TIF $VIRTUAL_WARPED.vrt $MAGIC_GCP_STRING
    :param input_filename:
    :param output_filename:
    :param control_points: should be a list of tuples (x,y,long,lat)
    :return: A call function os code (0 for success)
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

# NOTE need to check resample option is either
# near: nearest neighbour resampling (default, fastest algorithm, worst interpolation quality).
# bilinear: bilinear resampling.
# cubic: cubic resampling.
# cubicspline: cubic spline resampling.
# lanczos: Lanczos windowed sinc resampling.
# average: average resampling, computes the average of all non-NODATA contributing pixels. (GDAL >= 1.10.0)
# mode: mode resampling, selects the value which appears most often of all the sampled points. (GDAL >= 1.10.0)
# max: maximum resampling, selects the maximum value from all non-NODATA contributing pixels. (GDAL >= 2.0.0)
# min: minimum resampling, selects the minimum value from all non-NODATA contributing pixels. (GDAL >= 2.0.0)
# med: median resampling, selects the median value of all non-NODATA contributing pixels. (GDAL >= 2.0.0)
# q1: first quartile resampling, selects the first quartile value of all non-NODATA contributing pixels. (GDAL >= 2.0.0)
# q3: third quartile resampling, selects the third quartile value of all non-NODATA contributing pixels. (GDAL >= 2.0.0)
def georeference(input_filename, output_filename, control_points, opts):
    """
    $GDAL_PATH/gdalwarp $MEMORY_LIMIT $TRANSFORM_OPTION $RESAMPLE_OPTION \
    -dstalpha $MASK_OPTIONS -s_srs 'EPSG:4326' $VIRTUAL_WARPED.vrt \
    $REAL_WARPED_TIF -co TILED=YES -co COMPRESS=LZW
    :param filename: Input vrt
    :param control_points: list of control points each control point should be a tuple/list of (x,y,long,lat)
    :param opts: dictionary containing either "TRANSFORM_OPTIONS", "RESAMPLE_OPTIONS", "MASK_OPTIONS"
                with options in a list
    :return:
    """
    assert "RESAMPLE_OPTION" in opts
    assert "MASK_OPTIONS" in opts
    args = [
        path.join(environ["GDAL_HOME"], "gdalwarp"),
        "-r",
        opts["RESAMPLE_OPTION"],
        "-dstalpha",
        "-srcnodata"] + opts["MASK_OPTIONS"] + [
        "-s_srs",
        "EPSG:4326",
        "-co",
        "TILED=YES",
        "-co",
        "COMPRESS=LZW",
        input_filename,
        output_filename
    ]
    print(" ".join(args))
    return call(args)


def get_map_bbbox(filename):
    """
    $GDAL_PATH/gdalinfo $INPUT_WARPED_TIF
    $DO_STUFF_TO_PARSE "Lower Left" "Upper Right"
    This is such a shitty hack but I think it's best to replace a lot of the functions with ogr.
    So for consistancy I will keep it as is till we discuss further.
    :param filename:
    :return:
    """
    args = [
        path.join(environ["GDAL_HOME"], "gdalinfo"),
        filename,
    ]
    bbox = []
    output = check_output(args)
    for line in output.split("\n"):
        if "Upper Right" in line or "Lower Left" in line:
            bbox.append(line)
    return bbox