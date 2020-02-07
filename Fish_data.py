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

        # data_frame.columns = column_headers

        self.dataframes["fish_data"] = fish_df


        #get the water data
        water_data_path =  download.download_water_data()
        #build the water parsar
        water_df = pd.read_csv(water_data_path)
        self.dataframes['water_data'] = water_df


    def clean_fish_data(self):
        self.clean_fish_data = {}
        self.dirty_fish_data = {}
        clean = self.dataframes["fish_data"]
        dirty = {}

        current_year = datetime.datetime.now().year()
        clean = clean[((clean['Year'] >= 1962) & (clean['Year'] <= current_year))]
        bad_year = clean[(clean['Year'] < 1962) | (clean['Year'] > current_year)]
        dirty = vertical_stack = pd.concat([dirty, bad_year], axis=0)

        species_list = ["FMS", "LMB", "GSF", "BGL", "BLC", "YBH", "CCF", "BFL", "RSH", "BBH", "STB", "BM,", "OTH", "RLC",
                        "WAE", "SMB", "CRP", "BCL", "TFS", "RDS", "BLG", "FLM", "CC", "BC", "YGH", "WTC", "GZD", "cct",
                        "tfs'", "snb", "sj", "sgf", "gh", "gssf", "bgl", "el", "gdf", "gsf", "cat", "amb", "gnf", "wal",
                        "gsh", "rzb", "gbl", "cpm", "gaf", "gaz", "GLB", "GZDL", "GSDF", "GZC", "RBS"]
        clean = clean[(clean['Species'].isin(species_list()))]
        bad_species = clean[~(clean['Species'].isin(species_list()))]
        dirty = vertical_stack = pd.concat([dirty, bad_species], axis=0)

        clean = clean[(clean['Length'].isdigit())]
        bad_length = clean[~(clean['Length'].isdigit())]
        dirty = vertical_stack = pd.concat([dirty, bad_length], axis=0)

        clean = clean[(clean['Mass'].isdigit())]
        bad_mass = clean[(clean['Mass'].isdigit())]
        dirty = vertical_stack = pd.concat([dirty, bad_mass], axis=0)

        site_list = ["PB", "RN", "BF", "HA", "KC", "NW", "HC", "CC", "FC", "QC", "GH", "SJ", "WW", "PB", "RP", "SC", "WC",
                     "AI", "NC", "RC", "PF", "GC", "ES", " s", "U", "EL", "SA"]
        clean = clean[(clean['Species'].isin(site_list()))]
        bad_site = clean[~(clean['Species'].isin(site_list()))]
        dirty = vertical_stack = pd.concat([dirty, bad_site], axis=0)
        self.clean_fish_data = clean
        self.dirty_fish_data = dirty

    def get_fish_data(self):
        return self.dataframes["fish_data"]

    def get_water_data(self):
        return self.dataframes["water_data"]
