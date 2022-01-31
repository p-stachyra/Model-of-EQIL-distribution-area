import numba as nb
import numpy as np

from time import perf_counter

from pcraster import *

	
@nb.njit(cache=True)
def computeMean(raster_array, skip_value=0):
	"""Calculates average value for a two-dimensional array which represents a raster map.
	The function expects a two-dimensional array"""

	parameter_sum = 0.0
	elements = 0
	for i in range(raster_array.shape[0]):
			if raster_array[i] == skip_value:
				continue
			else:
				parameter_sum += raster_array[i]
				elements += 1

	return parameter_sum / elements

@nb.njit(cache=True)
def computeStandardDeviation(raster_array, skip_value=0):
	"""Calculates standard deviation value for a two-dimensional array which represents a raster map.
	The function expects a two-dimensional array"""

	mean_value = computeMean(raster_array)

	sq_differences = 0.0
	elements = 0
	for i in range(raster_array.shape[0]):
			if raster_array[i] == skip_value:
				continue
			else:
				sq_differences += (raster_array[i] - mean_value) ** 2
				elements += 1

	standard_deviation_biased = np.sqrt(sq_differences / elements)
	standard_deviation_unbiased = np.sqrt(sq_differences / (elements - 1))

	return standard_deviation_biased, standard_deviation_unbiased

def prepareData(binary_map_path):
	map_data = readmap(binary_map_path)
	# convert to array format
	data_array = numpy_operations.pcr2numpy(map_data, np.nan)
	# discard all missing values and return array
	return data_array[~np.isnan(data_array)]

def extractSimulationParameters():

	start = perf_counter()


	# Profile curvature: mean value and standard devation
	# Inside 0.12 PGA contour
	prof_c_array = prepareData("maps_above_PGA_threshold/prof_c_above_012.map")
	prof_c_mean = computeMean(prof_c_array)
	profile_curvature_biased_std, profile_curvature_unbiased_std = computeStandardDeviation(prof_c_array)
	# The entire DEM map area
	prof_c_array_entire = prepareData("binary_maps/profile_curvature.map")
	prof_c_mean_entire = computeMean(prof_c_array_entire)
	profile_curvature_biased_std_entire, profile_curvature_unbiased_std_entire = computeStandardDeviation(prof_c_array_entire)


	# Topographic wetness index (TWI): mean
	# Inside 0.12 PGA contour
	twi_array = prepareData("maps_above_PGA_threshold/twi_above_012.map")
	twi_mean = computeMean(twi_array)
	# The entire DEM map area
	twi_array_entire = prepareData("binary_maps/TWI_raster.map")
	twi_mean_entire = computeMean(twi_array_entire)

	# save parameters to a file
	with open("parameters/area_paramaters.csv", "w") as fh:
		fh.write(f"Area Extent, Profile Curvature Mean,Profile Curvature Biased Standard Deviation,Profile Curvature Unbiased Standard Deviation,Mean TWI\nInside 0.12 PGA Contour, {prof_c_mean},{profile_curvature_biased_std},{profile_curvature_unbiased_std},{twi_mean}\nDEM Map Extent, {prof_c_mean_entire},{profile_curvature_biased_std_entire},{profile_curvature_unbiased_std_entire},{twi_mean_entire}")




	finish = perf_counter()
	time_delta = finish - start
	print("\nProgram extractSimulationParameters finished. Total execution time: %f seconds" % time_delta)

	return 0

if __name__ == "__main__":
	extractSimulationParameters()