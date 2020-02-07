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
        column_headers = ["FishID","Date", "TREND","Gear", "Species", "Sex", "Length",
                          "Mass", "Ktl", "Relative weight", "Maturity", "Age structure",
                          "stomach", "gonads", "fat_index", "parasite", "misc 1 text",
                          "misc 2 num", "misc 3 text", "misc 4 num", "Site", "KFL"]

        fish_df.columns = column_headers

        #FishID with errors in dates
        fish_df = fish_df[fish_df.FishID != 20040355] #year 6468
        fish_df = fish_df[fish_df.FishID != 20040484] #year 0204
        fish_df = fish_df[fish_df.FishID != 20100667] #year 0210
        fish_df = fish_df[fish_df.FishID != 20110269] #year 0211

        #split date into Day, Month, Year columns
        fish_df['Day'] = pd.DatetimeIndex(fish_df['Date']).day
        fish_df['Month'] = pd.DatetimeIndex(fish_df['Date']).month
        fish_df['Year'] = pd.DatetimeIndex(fish_df['Date']).year

<<<<<<< HEAD
data_frame.columns = column_headers

#anything to prvent combinations
#tag in list of fish ID's that we will ignore
#want to tag things that don't fit correctly

Bad_data_IDs = []
=======
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
>>>>>>> 62284a0363309fad3361d81508333f8b7a77a653
