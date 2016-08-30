from osgeo import gdal
from osgeo import ogr

def canonise_map(filename): 
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(1198054.34, 648493.09)
    print point.ExportToWkt()

def add_overviews(filename): 
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(1198054.34, 648493.09)
    return point

def add_mask(filename, mask_vectors): 
    pass

def virtual_georeference(filename, control_points): 
    pass

def georeference(filename, control_points, opts): 
    pass

def get_map_bbbox(filename): 
    pass

