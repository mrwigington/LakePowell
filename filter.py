import pandas as pd

class Filter:
    # initialize filter object with pandas data frame
    def __init__(self, df):
        self.df = df.copy() #pandas data frame

    # select columns of interest by name
    def selectColumns(self, cols):
        self.df = self.df[cols]

    # def years(years):


    def gear(self, gear):
        self.df = self.df[self.df.Gear == gear]

    def species(self, species):
        self.df = self.df[self.df.Species == species]

    #male and female are True/False values
    def sex(self, male, female):
        if male and female:
            self.df = self.df[self.df.Sex == "M" or self.df.Sex == "F"]
        elif male and not female:
            self.df = self.df[self.df.Sex == "M"]
        elif not male and female:
            self.df = self.df[self.df.Sex == "F"]

    def sites(self, sites):
        self.df = self.df[self.df.Site == sites]

    #inclusive range
    def rangeLength(self, low, high):
        self.df = self.df[self.df.Length >= low]
        self.df = self.df[self.df.Length <= high]

    #inclusive range
    def rangeMass(self, low, high):
        self.df = self.df[self.df.Mass >= low]
        self.df = self.df[self.df.Mass <= high]

    #inclusive range
    def rangeKtl(self, low, high):
        self.df = self.df[self.df.Ktl >= low]
        self.df = self.df[self.df.Ktl <= high]

    # def rangeYears(year1, year2):
    #     a = list(range(year1, year2 + 1))
    #     self.df.loc(self.df['Date'] in )
    # df.columns = column_headers
    # df.iloc[:,1] = df.iloc[:,1].dt.strftime('%Y%m%d')
