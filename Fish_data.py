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
        input_name = download.download_fish_file()
        #build the fish data parsar
        dataframe = pd.read_excel(input_name)
        
        self.dataframes["fish_data"] = dataframe


        #get the water data
        #build the water parsar

        # import pdb; pdb.set_trace()


    def get_fish_data(self):
        return self.dataframes["fish_data"]

    def get_water_data(self):
        pass
