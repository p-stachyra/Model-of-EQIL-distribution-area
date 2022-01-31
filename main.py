# Project created by
# Jan Androsiuk
# Jaimy Lai
# Marius Lupulescu
# Piotr Stachyra 

from unifyResolutions import *
from cropRasterPGA import *
from translateToMap import *
from extractPGAZone import *
from extractSimulationParameters import *


def main():

	# Program's driver
	# This routine manages the modules' procedures.

	# make the resolution of the rasters smallest as possible. 
	# This leads to unifying the rasters resolution to the
	# most detailed value
	unifyResolutions()

	# PGA raster has a big extent, thus it must be adjusted
	# to the size of DEM map
	cropRasterPGA()

	# translate TIF rasters to .map binary maps
	# this format is understood by PCRaster
	translateAllRasters("adjusted_resolution_rasters")

	# this function allows to save binary maps 
	# representing the extent of the area within
	# the specified PGA threshold conture
	# The maps are saved to maps_above_PGA_threshold directory
	saveZoneMaps("binary_maps")

	# create a CSV files containing values
	# of inputs for the mLS parameter
	extractSimulationParameters()

	return 0

if __name__ == "__main__":
	main()







