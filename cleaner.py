import pandas as pd

class Cleaner:
    # initialize filter object with pandas data frame
    def __init__(self, fish_df):
        self.fish_df = fish_df.copy() #pandas data frame copied to avoid pointer problems
        self.dirty_fish_df = {}

    def clean_fish_data(self):
        prep_data()
        clean_year()
        clean_species()
        clean_length()
        clean_site()


    def clean_year(self):
        current_year = datetime.datetime.now().year()
        bad_year = self.fish_df[(self.fish_df['Year'] < 1962) | (self.fish_df['Year'] > current_year)]
        self.fish_df = self.fish_df[((self.fish_df['Year'] >= 1962) & (self.fish_df['Year'] <= current_year))]
        self.dirty_fish_df = pd.concat([self.dirty_fish_df, bad_year], axis=0)

    def clean_species(self):
        species_list = ["FMS", "LMB", "GSF", "BGL", "BLC", "YBH", "CCF", "BFL", "RSH", "BBH", "STB", "BM,", "OTH", "RLC",
                        "WAE", "SMB", "CRP", "BCL", "TFS", "RDS", "BLG", "FLM", "CC", "BC", "YGH", "WTC", "GZD", "cct",
                        "tfs'", "snb", "sj", "sgf", "gh", "gssf", "bgl", "el", "gdf", "gsf", "cat", "amb", "gnf", "wal",
                        "gsh", "rzb", "gbl", "cpm", "gaf", "gaz", "GLB", "GZDL", "GSDF", "GZC", "RBS"]

        bad_species = self.fish_df[~(self.fish_df['Species'].isin(species_list()))]
        self.fish_df = self.fish_df[(self.fish_df['Species'].isin(species_list()))]
        slef.dirty_fish_df = pd.concat([self.dirty_fish_df, bad_species], axis=0)

    def clean_length():
        bad_length = self.fish_df[~(self.fish_df['Length'].isdigit())]
        self.fish_df = self.fish_df[(self.fish_df['Length'].isdigit())]
        self.dirty_fish_df = pd.concat([self.dirty_fish_df, bad_length], axis=0)

    def clean_mass():
        bad_mass = self.fish_df[~(self.fish_df['Mass'].isdigit())]
        self.fish_df = self.fish_df[(self.fish_df['Mass'].isdigit())]
        self.dirty_fish_df = pd.concat([self.dirty_fish_df, bad_mass], axis=0)

    def clean_site():
        site_list = ["PB", "RN", "BF", "HA", "KC", "NW", "HC", "CC", "FC", "QC", "GH", "SJ", "WW", "PB", "RP", "SC", "WC",
                     "AI", "NC", "RC", "PF", "GC", "ES", " s", "U", "EL", "SA"]

        bad_site = clean[~(clean['Site'].isin(site_list()))]
        self.fish_df = self.fish_df[(self.fish_df['Site'].isin(site_list()))]
        self.dirty_fish_df = pd.concat([self.fish_df, bad_site], axis=0)

    def prep_data():
        self.fish_df['Species'] = self.fish_df['Species'].str.upper()
