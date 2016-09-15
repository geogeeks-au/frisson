#from osgeo import gdal
#from osgeo import ogr
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

def add_mask(filename, mask_vectors): 
    pass

def virtual_georeference(filename, control_points): 
    pass

def georeference(filename, control_points, opts): 
    pass

def get_map_bbbox(filename): 
    pass

