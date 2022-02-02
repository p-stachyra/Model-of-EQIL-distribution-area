# Project created by
# Jan Androsiuk
# Jaimy Lai
# Marius Lupulescu
# Piotr Stachyra 

import numpy as np

# local modules imports
from unifyResolutions import *
from cropToDEM import *
from translateToMap import *
from extractZone import *
from morphologicalStatistics import *


def main():

	# Program's driver
	# This routine manages the modules' procedures.

	# make the resolution of the rasters smallest as possible. 
	# This leads to unifying the rasters resolution to the
	# most detailed value. All the rasters in "data" folder are unified.
	unifyResolutions()

	# PGA raster has a big extent, thus it must be adjusted
	# to the size of DEM map.
	cropToDEM("adjusted_resolution_rasters/dem.tif",
			   "adjusted_resolution_rasters/pga_contour_raster.tif",
			   "adjusted_resolution_rasters/pga_contour_raster_cropped.tif")

	# crop the Ground Failure raster as well as its extent is bigger than of the DEM map
	cropToDEM("adjusted_resolution_rasters/dem.tif",
			  "adjusted_resolution_rasters/ground_failure_estimate.tif",
			  "adjusted_resolution_rasters/ground_failure_estimate_cropped.tif")

	# translate TIF rasters to .map binary maps
	# this format is understood by PCRaster
	translateAllRasters("adjusted_resolution_rasters", ["ground_failure_estimate.tif", "pga_contour_raster.tif"])

	# this function allows to save binary maps 
	# representing the extent of the area within
	# the specified PGA threshold conture
	# The maps are saved to PGA_zone directory
	extractZone("binary_maps", "pga_contour_raster_cropped.map", "PGA_zone", 0.12, np.nan)

	# this function allows to save binary maps
	# representing the extent of the area within
	# the specified ground failure probability threshold: more than 1% chance
	# The maps are saved to ground_failure_zone
	extractZone("binary_maps", "ground_failure_estimate_cropped.map", "ground_failure_zone", 0.01, np.nan)

	# create a CSV files containing values
	# of inputs for the mLS parameter
	morphologicalStatistics(["PGA_zone", "ground_failure_zone", "binary_maps"], "area_morphology")

	return 0

if __name__ == "__main__":
	main()







