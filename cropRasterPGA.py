import os
from osgeo import gdal

def cropRasterPGA():
	original_raster = gdal.Open('adjusted_resolution_rasters/dem.tif', gdal.GA_ReadOnly)
	geoTransform = original_raster.GetGeoTransform()
	minx = geoTransform[0]
	maxy = geoTransform[3]
	maxx = minx + geoTransform[1] * original_raster.RasterXSize
	miny = maxy + geoTransform[5] * original_raster.RasterYSize
	os.system(f"gdal_translate -projwin {minx} {maxy} {maxx} {miny} -of GTiff adjusted_resolution_rasters/pga_contour_raster.tif adjusted_resolution_rasters/pga_contour_raster_cropped.tif")

	return 0


if __name__ == "__main__":
	cropRasterPGA()