import pandas as pd
import re
import requests
import argparse

from Data_Crawler import Crawler

ap = argparse.ArgumentParser()

ap.add_argument("-b", "--basic_data_filename", required=True,
	help="Name of the basic data's file")
ap.add_argument("-d", "--detailed_data_filename", required=True,
	help="Name of the detailed data's file")
ap.add_argument("-f", "--full_data_filename", required=True,
	help="Name of the full data's file")

args = vars(ap.parse_args())

basic_data_filename =  args["basic_data_filename"]
detailed_data_filename =  args["detailed_data_filename"]
full_data_filename =  args["full_data_filename"]

Soccer_Crawler = Crawler()

Soccer_Crawler.Update_Data(basic_data_filename, detailed_data_filename, full_data_filename)
