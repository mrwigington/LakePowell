# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:21:03 2020

@author: aquag
"""

#class fish_data(dataset):
### this is how to defien a class

import pandas as pd


input_name = "BIO365-FishData.xlsx"


data_frame = pd.read_excel(input_name)

column_headers = ["FishID","Date", "TREND","Gear", "Species", "Gender", "Length", 
                  "Mass", "Ktl", "Relative weight", "Maturity", "Age structure",
                  "stomach", "gonads", "fat_index", "parasite", "misc 1 text",
                  "misc 2 num", "misc 3 text", "misc 4 num", "Site", "KFL"]

data_frame.columns = column_headers

#anything to prvent combinations
#tag in list of fish ID's that we will ignore
#want to tag things that don't fit correctly

Bad_data_IDs = []
