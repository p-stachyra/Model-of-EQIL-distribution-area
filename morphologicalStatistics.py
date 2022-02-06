# standard data analysis functions
import numpy as np
import os
import pandas as pd

# time performance measure
from time import perf_counter
# spatial operations
from pcraster import *

# local modules imports
from statisticalFunctions import *

def prepareData(binary_map_path):
	"""A function which loads binary rasters, translates them into multidimensional arrays,
	 flattens them and removes missing values
	 Returns a pre-processed data structure."""
	map_data = readmap(binary_map_path)
	# convert to array format
	data_array = numpy_operations.pcr2numpy(map_data, np.nan)
	# discard all missing values and return array
	return data_array[~np.isnan(data_array)]

def morphologicalStatistics(directories_to_crawl, directory_flatten_rasters):
	"""This function allows to compute descriptive statistics for the terrain of interest.
	Seperate CSV files are created for the values for each variable - such as TWI, profile curvature, etc
	And a single CSV file containing the descriptive statistics output is created.
	The function expects the directory in which all the files for computing statistical measures are located
	and a directory to which the separate CSV files for each phenomenon measures are going to be saved."""

	# create a directory for storing the flattened rasters
	if not os.path.isdir(directory_flatten_rasters):
		os.mkdir(directory_flatten_rasters)
	# for each directory and for each raster in directory, append the descriptive statistics values
	descriptive_statistics = []
	# prepare a list of all the names for each row
	descriptive_statistics.append(["directory",
					   "terrain_variable",
					   "mean_value",
					   "variance_biased",
					   "variance_unbiased",
					   "standard_deviation_biased",
					   "standard_deviation_unbiased",
					   "max_value",
					   "min_value",
					   "median_value"])

	# iterate through all the specified directories
	for directory in directories_to_crawl:
		# in each directory, iterate over each file
		for raster in os.listdir(directory):
			phenomenon_statistics = []
			# select only PCRaster .map files
			if raster[-3:] == "map":
				# extract the terrain variable from the raster name
				phenomenon_name = raster[:-4]
				# extrat the values from the raster in a 1-D array
				flattened_raster = prepareData(f"{directory}/{raster}")

				# save the array to CSV
				flattened_raster_df = pd.DataFrame(flattened_raster)
				flattened_raster_df.columns = [f"{phenomenon_name}"]
				flattened_raster_df.to_csv(f"{directory_flatten_rasters}/{directory}__{phenomenon_name}.csv")

				# descriptive statistics
				# extract mean, standard deviation, variance, minimal value, maximal value, median
				mean_value = computeMean(flattened_raster)
				variance_biased, variance_unbiased, standard_deviation_biased, standard_deviation_unbiased = measureDispersion(flattened_raster)
				max_value = flattened_raster.max()
				min_value = flattened_raster.min()
				median_value = np.median(flattened_raster)
				# prepare a list of descriptive statistics values
				measures_values = [mean_value,
								   variance_biased,
								   variance_unbiased,
								   standard_deviation_biased,
								   standard_deviation_unbiased,
								   max_value,
								   min_value,
								   median_value]
				# for keeping track of what is measured, append the directory name (context) and phenomenon name (what exatly is measured)
				phenomenon_statistics.append(directory)
				# append the values for each descriptive, another row is created
				phenomenon_statistics.append(phenomenon_name)
				for p in measures_values:
					phenomenon_statistics.append(p)
			# gather all rows
			descriptive_statistics.append(phenomenon_statistics)
	# create a dataframe for descriptive statistics and export it into CSV file format
	descriptive_statistics_df = pd.DataFrame(descriptive_statistics)
	descriptive_statistics_df.to_csv("parameters/area_terrain_statistics.csv")

	return 0
