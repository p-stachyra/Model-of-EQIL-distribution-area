import numpy as np
import pandas as pd

from pcraster import *


def createZoneMap(map_object, pga_map_object, pga_threshold, repalce_with=0):
	"""This function performs simple map algebra operations to determine the
	extent in the map where the PGA values exceed the specified threshold.
	Such a map is the output of this function.
	The function expects the current map, 
	the map containing PGA values, 
	the PGA threshold to limit the extent 
	and the replace value for the cells which are located in an irrelevant area"""

	above_threshold = pga_map_object > pga_threshold
	output_map = ifthenelse(above_threshold, map_object, repalce_with)
	return output_map

def saveZoneMaps(binary_maps_directory):
	"""This function allows to save the binary maps generated using createZoneMap function.
	Expects a directory name where the binary maps are stored. 
	The function saves the maps to a new directory: maps_above_PGA_threshold"""
	
	# prepare a new folder to save newly created maps
	new_folder = "maps_above_PGA_threshold"
	if not os.path.isdir(new_folder):
		os.mkdir(new_folder)

	try:
		# load PGA, DEM, TWI, Profile Curvature maps
		pga_map = readmap(f"{binary_maps_directory}/pga_contour_raster_cropped.map")
		dem_map = readmap(f"{binary_maps_directory}/dem.map")
		twi_map = readmap(f"{binary_maps_directory}/TWI_raster.map")
		prof_c_map = readmap(f"{binary_maps_directory}/profile_curvature.map")

		###############
		# Saving maps #
		###############
		# the value indicating that an area should be excluded for digital elevation model
		# is set to 0
		dem_above_012 = createZoneMap(dem_map, pga_map, 0.12, 0)
		report(dem_above_012, "maps_above_PGA_threshold/dem_above_012.map")
		# in case of TWI, the index value can differ, so by default this is also zero
		# but previous checks evaluate the maximal value for the TWI index.
		# in case of this study, the maximal value was -4.9608107 and 0 was selected.
		twi_above_012 = createZoneMap(twi_map, pga_map, 0.12, 0)
		report(twi_above_012, "maps_above_PGA_threshold/twi_above_012.map")
		# Profile curvature is morphometric variable in terms of modules in GRASS GIS
		prof_c_above_012 = createZoneMap(prof_c_map, pga_map, 0.12, 0)
		report(prof_c_above_012, "maps_above_PGA_threshold/prof_c_above_012.map")

	except Exception as e:
		print("[ ! ] Could not save the maps.")
		print("[ ! ] Error message: %s" % e)
		sys.exit(-1)

	return 0


if __name__ == "__main__":
	saveZoneMaps("binary_maps")
