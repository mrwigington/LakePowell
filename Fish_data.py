import pandas as pd
import numpy as np
import download
import cleaner

#NOTE: We're going to have to move loading out of the initializer because they're going to need to call download first.

class Fish():
    def __init__(self):
        #initialize a dictionary or somthing to hold dataframes
        self.dataframes = {}
        #+++++++++++++++++++++++++++++++++++++++++++get and parse the fish data ++++++++++++++++++++++++++++++++++++++++++++++++++
        fish_data_path = "data/fishdata"
        #build the fish data parsar
        fish_df = pd.read_excel(fish_data_path)
        column_headers = ["FishID","Date", "TREND","Gear", "Species", "Sex", "Length",
                          "Mass", "Ktl", "Weight", "Maturity", "Age structure",
                          "stomach", "gonads", "fat_index", "parasite", "misc 1 text",
                          "misc 2 num", "misc 3 text", "misc 4 num", "Site", "KFL"]

        fish_df.columns = column_headers

        #clean fish data
        clean = cleaner.Cleaner(fish_df)
        fish_df = clean.clean_fish_data() #all clean values default to true
        # print(clean.get_dirty_data())

        #split fish data date into Day, Month, Year columns
        fish_df['Day'] = pd.DatetimeIndex(fish_df['Date']).day
        fish_df['Month'] = pd.DatetimeIndex(fish_df['Date']).month
        fish_df['Year'] = pd.DatetimeIndex(fish_df['Date']).year

        self.dataframes["fish_data"] = fish_df

        #++++++++++++++++++++++++++++++++++++++++++get and parse the water data +++++++++++++++++++++++++++++++++++++++++++++++++++++
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

        water_df["MONTH"]= df_months.astype(int)
        water_df["DAY"]= new[2].astype(int)
        water_df["YEAR"]= new[3].astype(int)

        self.dataframes['water_data'] = water_df

    def download(self):
        download_msg = "Downloading fish data . . ."
        print(download_msg, end='\r')
        fish_data_path = download.download_fish_file()
        print(" " * len(download_msg), end='\r') # Erase the downloading message

        download_msg = "Downloading fish data . . ."
        fish_data_path = download.download_fish_file()
        water_data_path = download.download_water_data()
        print(" " * len(download_msg), end='\r') # Erase the downloading message



    def load_data():
        pass


    def get_fish_data(self):
        return self.dataframes["fish_data"]

    def get_water_data(self):
        return self.dataframes["water_data"]

    def join_fish(self, fish_data, water_data, time_unit):
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
