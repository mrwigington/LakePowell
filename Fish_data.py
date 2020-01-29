# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:21:03 2020

@author: aquag
"""

#class fish_data(dataset):
### this is how to defien a class

import pandas as pd
import download


class Fish():
    def __init__(self):
        #initialize a dictionary or somthing to hold dataframes
        self.dataframes = {}
        #get the fish data
        fish_data_path = download.download_fish_file()
        #build the fish data parsar
        fish_df = pd.read_excel(fish_data_path)
        column_headers = ["FishID","Date", "TREND","Gear", "Species", "Gender", "Length",
                          "Mass", "Ktl", "Relative weight", "Maturity", "Age structure",
                          "stomach", "gonads", "fat_index", "parasite", "misc 1 text",
                          "misc 2 num", "misc 3 text", "misc 4 num", "Site", "KFL"]

        fish_df.columns = column_headers
        self.dataframes["fish_data"] = fish_df


        #get the water data
        water_data_path =  download.download_water_data()
        #build the water parsar
        water_df = pd.read_csv(water_data_path)
        self.dataframes['water_data'] = water_df


    def get_fish_data(self):
        return self.dataframes["fish_data"]

    def get_water_data(self):
        return self.dataframes["water_data"]
