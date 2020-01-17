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
