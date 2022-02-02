import os
import sys

def translateToMap(input_name, output_name, datatype):

	if not os.path.isdir("binary_maps"):
		os.mkdir("binary_maps")

	try:
		os.system(f"gdal_translate -ot {datatype} -of PCRaster adjusted_resolution_rasters/{input_name} binary_maps/{output_name}")
	except Exception as e:
		print("[ ! ] Failed to convert to .map format!")
		sys.exit(-1)
	return 0


def translateAllRasters(rasters_directory, rasters_to_skip):
	for raster in os.listdir(rasters_directory):
		if raster in rasters_to_skip:
			continue
		else:
			name = raster.split(".")[0]
			new_name = f"{name}.map"
			translateToMap(raster, new_name, "Float64")

