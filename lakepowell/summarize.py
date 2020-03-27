import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import lakepowell

# summarizes fish or lake data based on given criteria over a specified numerical variable.
# @Param layers: An ordered list of column header names (strings). First layer in the list
# is the largest group and the last is the smallest subgrouping.
# @Param feature: is the name of the numerical variable column that should have a summary calculation performed over it.
# @Param calcs: are the different calculations to be made over the feature.
def table_summary(df, layers, feature, calcs, titles):
    if feature is None: #if the feature is None, assume they want to count the lowest subgrouping
        feature = layers[-1]
        calcs = ['count']
    if calcs is None: #if there is no calculation assum they want to count the feature
        calcs = ['count']
    if len(calcs) != len(titles): #catch errors in length of given title and replace with numbered list
        titles = map(str, range(len(calcs) + 1))

    grouped_multiple = df.groupby(layers).agg({feature: calcs})
    grouped_multiple.columns = titles
    grouped_multiple = grouped_multiple.reset_index()

    return grouped_multiple

# Combines the fish and lake condition data tables based on date. It will join off of the
# most specific date in both dataframes.
# @Param fish_df: the fish data pandas dataframe
# @Param water_df: the lake conditions pandas dataframe
def join_fish_and_water(fish_df, water_df):
    year = False
    month = False
    day = False
    new_df = None

    fish_df.columns = ["Fish_" + s for s in fish_df.columns] #add "Fish_" to the start of every string
    water_df.columns = ["Lake_" + s for s in water_df.columns] #add "Lake_" to the start of every string

    if "Fish_Year" in fish_df.columns and "Lake_YEAR" in water_df.columns:
        year = True
    if "Lake_Month" in fish_df.columns and "Lake_MONTH" in water_df.columns:
        month = True
    if "Lake_Day" in fish_df.columns and "Lake_DAY" in water_df.columns:
        day = True

    #join based on most specific date in the given dataframes
    if year and month and day:
        new_df = pd.merge(fish_df, water_df,  how='left', left_on=["Fish_Year","Fish_Month","Fish_Day"],
                            right_on = ["Lake_YEAR", "Lake_MONTH", "Lake_DAY"])
        new_df = new_df.drop(["Lake_YEAR", "Lake_MONTH", "Lake_DAY"], axis = 1)
    elif year and month and not day:
        new_df = pd.merge(fish_df, water_df,  how='left', left_on=["Fish_Year", "Fish_Month"],
                            right_on = ["Lake_YEAR", "Lake_MONTH"])
        new_df = new_df.drop(["Lake_YEAR", "Lake_MONTH"], axis = 1)
    elif year and not month and not day:
        new_df = pd.merge(fish_df, water_df,  how='left', left_on=["Fish_Year"],
                            right_on = ["Lake_YEAR"])
        new_df = new_df.drop(["Lake_YEAR"], axis = 1)

    return new_df
# calculates the CPUE by determining the CPUE for each trip and then scales EL to GN to
# give a more accurate representation of CPUE.
# @Param fish_df: the fish dataframe subset to calculate CPUE across
# @Param full_fish_df: the entire fish dataframe to use as a reference in determining EL to GN ratio
def cpue_scale(fish_df, full_fish_df):
    titles = ['CPUE']
    layers = ['Species', 'Year', 'Location', 'Month', 'Site', 'Gear']
    feature = 'Length'
    calcs = ['count']
    ratio = get_el_ratio(full_fish_df)

    gear_count = table_summary(fish_df, layers, feature, calcs, ['count'])
    gear_count['CPUE'] = gear_count['count'].divide(8) #4 nets for two nights for each trip for CPUE
    gear_count.loc[gear_count.Gear == 'EL', 'CPUE'] = gear_count.loc[gear_count.Gear == 'EL', 'CPUE'] / ratio #scale CPUE for EL
    year_cpue = table_summary(gear_count, ['Species', 'Year', 'Location'], 'CPUE', ['mean'], ['mean']) #mean gives CPUE for Year

    return year_cpue
# calculates the CPUE by determining the CPUE for each trip
# @Param fish_df: the fish dataframe subset to calculate CPUE across
def cpue_precise(fish_df):
    titles = ['count']
    layers = ['Species', 'Year', 'Location', 'Month', 'Site']
    feature = 'Length'
    calcs = ['count']

    site_count = table_summary(fish_df, layers, feature, calcs, ['count']) #count the fish cought for each colection
    site_count['CPUE'] = site_count['count'].divide(8) #calculate CPUE for each site
    year_cpue = table_summary(site_count, ['Species', 'Year', 'Location'], 'CPUE', ['mean'], ['mean']) #calculate CPUE across year/location

    return year_cpue

# calculates the CPUE by determining the CPUE across each year, assuming that 4 trips were made each year_cpue
# and all gear types performed equally well
# @Param fish_df: the fish dataframe subset to calculate CPUE across
def cpue_simple(fish_df):
    titles = ['CPUE']
    layers = ['Species', 'Year', 'Location']
    feature = 'Length'
    calcs = [lambda x: len(x)/32]#divide catch by 32 = 4 nets * 2 nights * 4 trips in a year

    loc_cpue = table_summary(fish_df, layers, feature, calcs, titles)
    return loc_cpue
# determines the ratio of fish caught with EL to fish caught with GN (EL/GN)
# @Param fish_df: the entire fish dataframe to use as a reference in determining EL to GN ratio
def get_el_ratio(fish_df):
    layers = ['Year', 'Location', 'Site', 'Month', 'Day', 'Gear']
    feature = 'Length'
    calcs = ['count']

    year_gear_counts = table_summary(fish_df, layers, feature, calcs, ['num_fish'])
    gear_means = table_summary(year_gear_counts, ['Gear'], 'num_fish', ['mean'], ['Mean'])
    el = gear_means.loc[gear_means['Gear'] == 'EL', 'Mean'].iloc[0]
    gn = gear_means.loc[gear_means['Gear'] == 'GN', 'Mean'].iloc[0]
    el_ratio = el/gn

    return el_ratio
