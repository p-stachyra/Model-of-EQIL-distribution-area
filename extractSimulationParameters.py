import numba as nb
import numpy as np

from time import perf_counter

from pcraster import *

	
@nb.njit(nopython=True, cache=True)
def computeMean(raster_array, skip_value=0):
	"""Calculates average value for a two-dimensional array which represents a raster map.
	The function expects a two-dimensional array"""

	parameter_sum = 0.0
	elements = 0
	for i in range(raster_array.shape[0]):
		for j in range(raster_array.shape[1]):
			if raster_array[i][j] == skip_value:
				continue
			else:
				parameter_sum += raster_array[i][j]
				elements += 1

	return parameter_sum / elements

@nb.njit(nopython=True, cache=True)
def computeStandardDeviation(raster_array, skip_value=0):
	"""Calculates standard deviation value for a two-dimensional array which represents a raster map.
	The function expects a two-dimensional array"""

	mean_value = computeMean(raster_array)

	sq_differences = 0.0
	elements = 0
	for i in range(raster_array.shape[0]):
		for j in range(raster_array.shape[1]):
			if raster_array[i][j] == skip_value:
				continue
			else:
				sq_differences += (raster_array[i][j] - mean_value) ** 2
				elements += 1

	standard_deviation_biased = np.sqrt(sq_differences / elements)
	standard_deviation_unbiased = np.sqrt(sq_differences / elements - 1)

	return standard_deviation_biased, standard_deviation_unbiased


def profileCurvature(datafolder, raster_name):
	raster_file = readmap(f"{datafolder}/{raster_name}")
	profile_curvature_raster = profcurv(raster_file)
	profile_curvature_array = numpy_operations.pcr2numpy(profile_curvature_raster, np.nan)
	return profile_curvature_array

def extractSimulationParameters():

	start = perf_counter()

	data_folder = "maps_above_PGA_threshold"


	# Profile curvature: mean value and standard devation
	profile_curvature = profileCurvature(data_folder, "dem_above_012.map")
	profile_curvature_mean = computeMean(profile_curvature)
	profile_curvature_biased_std, profile_curvature_unbiased_std = computeStandardDeviation(profile_curvature)

	
	# Topographic wetness index (TWI): mean
	twi_map = readmap(f"{data_folder}/dem_above_012.map")
	twi_array = numpy_operations.pcr2numpy(twi_map, np.nan)
	twi_mean = computeMean(twi_array)

	# save parameters to a file
	with open("area_paramaters.csv", "w") as fh:
		fh.write(f"Profile Curvature Mean,Profile Curvature Biased Standard Deviation,Profile Curvature Unbiased Standard Deviation,Mean TWI\n{profile_curvature_mean},{profile_curvature_biased_std},{profile_curvature_unbiased_std},{twi_mean}")




	finish = perf_counter()
	time_delta = finish - start
	print("\nProgram extractSimulationParameters finished. Total execution time: %f seconds" % time_delta)

	return 0

if __name__ == "__main__":
	extractSimulationParameters()