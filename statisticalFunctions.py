import numba as nb
import numpy as np

@nb.njit(cache=True)
def computeMean(raster_array, skip_value=np.nan):
	"""Calculates average value for a two-dimensional array which represents a raster map.
	The function expects an array or other iterable, numeric data structure.
	The function returns mean."""

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
def measureDispersion(raster_array, skip_value=np.nan):
	"""Calculates standard deviation value for a two-dimensional array which represents a raster map.
	The function expects an array or other iterable, numeric data structure.
	The function returns biased variation, unbiased variation, biased standard deviation, unbiased standard deviation."""

	mean_value = computeMean(raster_array)

	sq_differences = 0.0
	elements = 0
	for i in range(raster_array.shape[0]):
			if raster_array[i] == skip_value:
				continue
			else:
				sq_differences += (raster_array[i] - mean_value) ** 2
				elements += 1

	variance_biased = sq_differences / elements
	variance_unbiased = sq_differences / (elements - 1)
	standard_deviation_biased = np.sqrt(variance_biased)
	standard_deviation_unbiased = np.sqrt(variance_unbiased)

	return variance_biased, variance_unbiased, standard_deviation_biased, standard_deviation_unbiased

