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
        # fish_data_path = download.download_fish_file()
        fish_data_path = "data/fishdata"
        #build the fish data parsar
        fish_df = pd.read_excel(fish_data_path)
        column_headers = ["FishID","Date", "TREND","Gear", "Species", "Sex", "Length",
                          "Mass", "Ktl", "Weight", "Maturity", "Age structure",
                          "stomach", "gonads", "fat_index", "parasite", "misc 1 text",
                          "misc 2 num", "misc 3 text", "misc 4 num", "Site", "KFL"]

        fish_df.columns = column_headers

        #FishID with errors in dates
        fish_df = fish_df[fish_df.FishID != 20040355] #year 6468
        fish_df = fish_df[fish_df.FishID != 20040484] #year 0204
        fish_df = fish_df[fish_df.FishID != 20100667] #year 0210
        fish_df = fish_df[fish_df.FishID != 20110269] #year 0211

        #split fish data date into Day, Month, Year columns
        fish_df['Day'] = pd.DatetimeIndex(fish_df['Date']).day
        fish_df['Month'] = pd.DatetimeIndex(fish_df['Date']).month
        fish_df['Year'] = pd.DatetimeIndex(fish_df['Date']).year

        self.dataframes["fish_data"] = fish_df

        #get the water data
        water_data_path =  "data/water_data"
        water_df = pd.read_csv(water_data_path)

        new = water_df["DATE MEASURED"].str.split(r",\s|\s", n = 3, expand = True)
        #------------------- convert month to digit -------------------
        months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
                    'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        df_months = new[1]
        for i in range(0, len(df_months)):
            df_months[i] = months.get(df_months[i])
        #--------------------------------------------------------------

        water_df["MONTH"]= df_months
        water_df["DAY"]= new[2]
        water_df["YEAR"]= new[3]

        self.dataframes['water_data'] = water_df

    def get_fish_data(self):
        return self.dataframes["fish_data"]

    def get_water_data(self):
        return self.dataframes["water_data"]
