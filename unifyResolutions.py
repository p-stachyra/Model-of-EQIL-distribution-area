import numpy as np
import os
import pandas as pd
import sys

from osgeo import gdal
from time import perf_counter

def findAllRasters(directory):
	"""Identifies files with .tif extension.
	Expects an argument for the directory name in which the rasters are located"""
	
	# get all files in the relative directory
	all_files = os.listdir(directory)
	# declare and initialize an empty array to store .tif files
	tif_rasters = []
	# check all files and add to the list those files with TIF extension
	for file in all_files:
		if (file[-3:] == "tif") | (file[-3:] == "TIF"):
			tif_rasters.append(file)

	return tif_rasters

def computeRasterResolution(raster_file, relative_directory="data"):
	"""Determines what is the resolution of the provided raster. 
	Expects the raster file's name or an absolute path to the raster.
	The default argument for the directory containing rasters is set to data"""
	
	raster_path = f"{relative_directory}/{raster_file}"

	xcell = 0
	ycell = 0
	
	try:
		# obtain the resolutions of cell's width and height
		source = gdal.Open(raster_path)
		xcell = abs(source.GetGeoTransform()[1])
		ycell = abs(source.GetGeoTransform()[-1])

	except Exception as e:
		print("[ ! ] Determining the raster's resolution failed.")
		print("[ ! ] ERROR MESSAGE: %s" % e)
		sys.exit(-1)

	return (xcell, ycell)

def getResolutionsDataFrame(directory, raster_files):
	"""Creates a dataframe containing raster resolutions and their names.
	Expects a relative directory where the rasters are stores and raster files names (an array)"""
	
	# declare and initialize array variables for storing pixel's width, height and raster's name
	resolutions_x = []
	resolutions_y = []
	raster_names = []

	try:
		for filename in raster_files:
			xcell, ycell = computeRasterResolution(filename, relative_directory=directory)
			resolutions_x.append(xcell)
			resolutions_y.append(ycell)
			raster_names.append(filename)

	except Exception as e:
		print("[ ! ] Failed to create a resolutions dataframe.")
		print("[ ! ] ERROR MESSAGE: %s" % e)
		sys.exit(-1)

	resolutions_df = pd.DataFrame([resolutions_x, resolutions_y, raster_names]).T
	resolutions_df.columns = ["pixel_x", "pixel_y", "file_name"]
	return resolutions_df

def changeResolution(min_resolution, rasters_directory, raster):
	"""Changes the resolution of a raster to the provided resolution.
	Expects the required resolution, the relative directory name and raster file's name."""
	
	if not os.path.isdir("adjusted_resolution_rasters"):
		os.mkdir("adjusted_resolution_rasters")

	# if function fails, it returns an exitcode of a value -1
	exitcode = -1

	try:
		# Use GDAL WARP to change the resolutions of the provided raster
		gdal.Warp(f"adjusted_resolution_rasters/{raster}", f"{rasters_directory}/{raster}", xRes=min_resolution, yRes=min_resolution)
		# Upon sucessful transformation, return 0 value indicating successful execution
		exitcode = 0
	except Exception as e:
		print("[ ! ] Error changing the raster's resolution.")
		print("[ ! ] Error message: %s" % e)
	
	return exitcode

def main():

	start = perf_counter()

	# compare raster resolutions
	resolutions_df = getResolutionsDataFrame("data", findAllRasters("data"))
	print(resolutions_df)
	
	# Determine the smallest resolution which will be set as the default resolution for all rasters
	smallest_resolutions = resolutions_df[["pixel_x", "pixel_y"]].min()
	#################################
	# TODO: resolution inconsistency #
	#################################
	smallest_size = round(smallest_resolutions.tolist()[0], 5)

	# change rasters' resolution to adjust them to the smallest one
	success_codes = []
	for raster in findAllRasters("data"):
		changeResolution(smallest_size, "data", raster)

	# study the coherence of this operation
	adjusted_rasters = findAllRasters("adjusted_resolution_rasters")
	print(adjusted_rasters)
	print(getResolutionsDataFrame("adjusted_resolution_rasters", adjusted_rasters))
	# Save the dataframe as a CSV file to access the length of pixels later, more easily
	getResolutionsDataFrame("adjusted_resolution_rasters", adjusted_rasters).to_csv("rasters_unified_resolutions.csv")

	finish = perf_counter()
	time_delta = finish - start
	print("\nProgram finished. Total execution time: %f seconds" % time_delta)

	return 0

if __name__ == "__main__":
	main()