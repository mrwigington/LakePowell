import pandas as pd
import numpy as np
from statistics import *

class Join():
    def __init__(self, fish_df, water_df):
        self.fish_df = fish_df.copy()
        self.water_df = water_df.copy()
        self.new_table = []
        self.date_dict = {}

    def range_join(self, spread, operation):
        # for every row in the fish data, calculate a summary of the water data
        # that matches the size of the spread
        for i in range(0, len(self.fish_df.index)):
        # for i in range(2):
            row = self.fish_df.iloc[i]
            day = row.Day
            month = row.Month
            year = row.Year

            #truth lists of rows where each condition is met
            day_bool = self.water_df["DAY"] == day
            month_bool = self.water_df["MONTH"] == month
            year_bool = self.water_df["YEAR"] == year
            key = str(day) + "/" + str(month) + "/" + str(year)
            value = []

            if not (key in self.date_dict):
                #only the index in the water data that matches the specific date
                index = self.water_df.index[day_bool & month_bool & year_bool]
                #get the range of rows in the water data
                start = index[0] - spread
                end =  index[0] + spread + 1
                summary = self.water_df.iloc[start:end, ]

                elevation = self.calc_val(operation, summary.loc[:,"ELEVATION"])
                content = self.calc_val(operation, summary.loc[:, "CONTENT"])
                inflow = self.calc_val(operation, summary.loc[:, "INFLOW"])
                outflow = self.calc_val(operation, summary.loc[:, "OUTFLOW"])
                high_temp = self.calc_val(operation, summary.loc[:, "HIGH TEMP"])
                low_temp = self.calc_val(operation, summary.loc[:, "LOW TEMP"])
                # total_temp = self.calc_val(operation, list(summary.loc[:, "LOW TEMP"]).extend(list(summary.loc[:, "HIGH TEMP"])))
                water = self.calc_val(operation, summary.loc[:, "WATER"])
                print("vals: ", elevation, content, inflow)
                value = [day, month, year, elevation, content, inflow,
                        outflow, high_temp, low_temp, water]
                self.new_table.append(value)
                self.date_dict[key] = value

        sum_data = pd.DataFrame.from_records(self.new_table)
        sum_data.columns = ["DAY", "MONTH", "YEAR", "ELEVATION", "CONTENT", "INFLOW",
                            "OUTFLOW", "HIGH TEMP", "LOW TEMP", "WATER"]
        new_df = pd.merge(self.fish_df, sum_data,  how='left', left_on=['Day','Month', 'Year'], right_on = ['DAY', 'MONTH', 'YEAR'])

        print(new_df.iloc[-100:-50,])


    def calc_val(self, operation, data):
        if operation == "min":
            return min(list(data))
        elif operation == "max":
            return max(list(data))
        elif operation == "mean":
            return mean(list(data))



    def join_fish_and_water(self, fish_data, water_data, time_unit):
        time_unit = time_unit.lower()

        #select the fish data
        #add a year_month column
        fish_yrs_dfs = {}
        fish_years = fish_data["Year"].unique()
        fish_months = fish_data["Month"].unique()
        # concatenate the years and months together
        fish_data["year_month"] = fish_data["Year"].astype(str) + "_" + fish_data["Month"].astype(str)
        fish_time = fish_data['year_month'].unique()

        if time_unit == "month":
            timeU = fish_data["year_month"].unique()
        else:
            timeU = fish_data["Year"].unique().astype(str)

        fish_yrm_dfs = {}
        for  year_or_month in timeU:
            if time_unit == "month":
                fish_sel = fish_data.loc[fish_data['year_month'] == year_or_month]
            else:
                fish_sel = fish_data.loc[fish_data['Year'].astype(str) == year_or_month]

            fish_sel = fish_sel.reset_index()
            fish_yrm_dfs[year_or_month] = fish_sel

        #select water data
        #make a column for water data
        water_data["year_month"] = water_data["YEAR"].astype(str) + "_" + water_data["MONTH"].astype(str)
        # pull out selected columns
        water_yrm_dfs = {}
        for year_or_month in timeU:
            if time_unit == "month":
                water_sel = water_data.loc[water_data['year_month'] == year_or_month]
            else:
                water_sel = water_data.loc[water_data['YEAR'] == year_or_month]
            water_yrm_dfs[year_or_month] = water_sel

        #Get the averages for the water data
        averages = {}
        for year_or_month in water_yrm_dfs:
            df = water_yrm_dfs.get(year_or_month)
            df = df.drop(columns=["MONTH", "DAY", "YEAR", "year_month"])
            avg = df.mean()
            avg = avg.to_frame()
            avg = avg.transpose()
            averages[year_or_month] = avg


        #Join the fish and water data together (based on month or year)
        joined_tables = []
        for year_or_month in timeU:
            fishdf = fish_yrm_dfs.get(str(year_or_month))
            waterdf = averages.get(str(year_or_month))
            #repeat the water data averages
            repeat = len(fishdf.index)
            col = waterdf.columns
            newwater = pd.DataFrame(np.repeat(waterdf.values,repeat,axis=0), columns=col)
            newwater = newwater.drop(columns=["Unnamed: 0"])
            joined = fishdf.join(newwater)
            joined_tables.append(joined)


        # Concatentate the joined tables together
        #iterate through all the joined tables and append them together.
        for position in range(len(joined_tables)):
            if position == 0:
                finaldf = joined_tables[0]
            else:
                finaldf = finaldf.append(joined_tables[position], ignore_index=True)

        return finaldf
