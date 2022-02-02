from osgeo import gdal
import math

def calculate_radius(magnitude, in_pixels=True, pixel_res=208.34):
    """
    Calculate the area radius based on Keefer, D. K. (2002)
    The original formula: Log_10(A_d) = magnitude - 3.46, where A_d is the hazard area estimation in km2
    Each pixel size is equal to approximately 208.34 meters, as all of the layers' resolutions are
    normalized to DEM map resolution
    """
    if in_pixels: A_d = 10**(-173/50 + magnitude)*10**3/pixel_res
    else: A_d = 10**(-173/50 + magnitude)*10**3
    print(A_d)
    return math.sqrt(A_d/math.pi)

def create_proximity_map(source_path='data/rupture_point_raster.tif', output_path='data/EQIL_area.tif', magnitude=5.3):
    """
    Following the method from: https://gis.stackexchange.com/a/304413
    The radius is calculated using calculate_radius() function,
    and its length is rounded to the closest integer with int() function
    """
    radius = int(calculate_radius(magnitude))
    src_ds = gdal.Open(source_path)
    srcband = src_ds.GetRasterBand(1)
    dst_filename = output_path
    drv = gdal.GetDriverByName('GTiff')
    dst_ds = drv.Create(
        dst_filename, src_ds.RasterXSize, src_ds.RasterYSize,
        1, gdal.GetDataTypeByName('Float32')
    )
    dst_ds.SetGeoTransform(src_ds.GetGeoTransform())
    dst_ds.SetProjection(src_ds.GetProjectionRef())
    dstband = dst_ds.GetRasterBand(1)
    gdal.ComputeProximity(
        srcband, dstband,
        ["DISTUNITS=PIXEL", f"MAXDIST={radius}", "NODATA=0.0", "OT=Float32", "OF=GTiff"]
    )
    srcband = None
    dstband = None
    src_ds = None
    dst_ds = None