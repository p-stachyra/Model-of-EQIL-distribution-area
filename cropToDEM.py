import os
from osgeo import gdal

def cropToDEM(input_raster_path, target_raster_path, output_raster_path):
	original_raster = gdal.Open(input_raster_path, gdal.GA_ReadOnly)
	geoTransform = original_raster.GetGeoTransform()
	minx = geoTransform[0]
	maxy = geoTransform[3]
	maxx = minx + geoTransform[1] * original_raster.RasterXSize
	miny = maxy + geoTransform[5] * original_raster.RasterYSize
	os.system(f"gdal_translate -projwin {minx} {maxy} {maxx} {miny} -of GTiff {target_raster_path} {output_raster_path}")

	return 0

