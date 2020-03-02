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
