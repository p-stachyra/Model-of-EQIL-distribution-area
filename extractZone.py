import numpy as np
import pandas as pd

from pcraster import *


def createZoneMap(map_object, reference_map_object, threshold, repalce_with_value):
	"""This function performs simple map algebra operations to determine the
	extent in the map where the PGA values exceed the specified threshold.
	Such a map is the output of this function.
	The function expects the current map, 
	the map containing PGA values, 
	the PGA threshold to limit the extent 
	and the replace value for the cells which are located in an irrelevant area"""

	above_threshold = reference_map_object > threshold
	output_map = ifthenelse(above_threshold, map_object, repalce_with_value)
	return output_map

def extractZone(binary_maps_directory, narrow_to_area, save_to_directory, threshold_value, replace_with):
	"""This function allows to save the binary maps generated using createZoneMap function.
	Expects a directory name where the binary maps are stored. 
	The function saves the maps to a new directory: maps_above_PGA_threshold"""
	
	# prepare a new folder to save newly created maps
	if not os.path.isdir(save_to_directory):
		os.mkdir(save_to_directory)

	narrow_to_map = readmap(f"{binary_maps_directory}/{narrow_to_area}")

	try:
		# load all rasters in binary_maps_directory
		for raster_map in os.listdir(binary_maps_directory):
			if (raster_map != narrow_to_area) & (raster_map[-3:] == "map") & (raster_map != "ground_failure_estimate.map"):
				# read the raster from which the parameters are to be read
				parameter_map = readmap(f"{binary_maps_directory}/{raster_map}")
				# save the map containing the data within the specified zone
				# the data in other zones will be replaced by repalce_with value
				report(createZoneMap(parameter_map,
									 narrow_to_map,
									 threshold_value,
									 replace_with),
					   f"{save_to_directory}/{raster_map}")

	except Exception as e:
		print("[ ! ] Could not save the maps.")
		print("[ ! ] Error message: %s" % e)
		sys.exit(-1)

	return 0
