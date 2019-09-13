import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
import pyreadstat

df1, meta = pyreadstat.read_sav('/Users/lazarus/galvanize/datasets/osfstorage-archive/CCAM SPSS Data.sav')
df1.to_csv('/Users/lazarus/galvanize/capstone_1/data/climate_survey_data.csv')

'''
end product: bar graph of each static demographicgraphic's % change in belief
static demographics:
'gender'__________2
'generation'______6
'income_category'_3
'race'____________4
'party_x_ideo'____6
SPECIAL CASE ***'religion'_15***
SPECIAL CASE ***'evangelical'_4*** # look up evangelical environmental movement
'''

class DemographicAnalysis:
    def __init__(self, df):
        self.df = df1[df1.year != 1] # get rid of 2008 because it's weird
    
    def split_demographics(self, df):
        # columns_to_split = input('Which categories do you want to split? ') <----interative for future users
        columns_to_split = ['gender', 'generation', 'income_category', 'race', 'party_x_ideo'] # choose which demographics to separate from their column categories
        # split demographics under each column into lists
        demographics = [['male', 'female'], ['igen_genz', 'millenials', 'gen_x', 'baby_boomers', 'silent', 'greatest'], ['<50k', '50k-99k', '100k<'], ['white', 'black', 'other', 'hispanic'], ['lib_dem', 'mod_dem', 'independent', 'mod_rep', 'con_rep']]
        demographic_columns = []
        for i1 in range(len(columns_to_split)):
            for i2 in range(1, int(df.loc[:,columns_to_split[i1]].max()+1)):
                df[demographics[i1][i2-1]] = np.where(df.loc[:,columns_to_split[i1]]==i2,1,0)
                demographic_columns.append(demographics[i1][i2-1])
                print(df[demographics[i1][i2-1]], "has been added to the dataframe.")
            print(df.columns)
        print(demographic_columns)
        return demographic_columns

    # interactive version to pretty up later
    '''
    new_columns = []
    def split_demographics(col=columns_to_split):
        for col in columns_to_split:
            for i in range(int(df.loc[:,col].min()), int(df.loc[:,col].max()+1)):
                demographic_name = str(input('demographic name?: '))
                demographic_name = "'"+demographic_name+"'"
                df[demographic_name] = np.where(df.loc[:,col]==i,1,0)
                new_columns.append(demographic_name)
                print(df[demographic_name], "has been added to the dataframe.")
            print(df.columns)
        print(new_columns)
    '''

    def apply_weight_wave(self,df,demographic_columns):
        demographics_weighted_wave = []
        for i in range(len(demographic_columns)):
            df[demographic_columns[i]+'_weighted_wave'] = df[demographic_columns[i]] * df['weight_wave']
            demographics_weighted_wave.append(demographic_columns[i]+'_weighted_wave')
        print(df.columns)
        return demographics_weighted_wave


    def apply_weight_aggregate(self,df,demographic_columns):
        demographics_weighted_aggregate = []
        for i in range(len(demographic_columns)):
            df[demographic_columns[i]+'_weighted'] = df[demographic_columns[i]] * df['weight_aggregate']
            demographics_weighted_aggregate.append(demographic_columns[i]+'_weighted')
        print(df.columns)
        return demographics_weighted_aggregate


    def believers_per_demographic(self,df,demographic_columns,demographics_weighted_wave):
        believer_columns = []
        df['humans_cause'] = np.where(df['cause_original']==1, 1, 0) # dividend column for calculating % belief for each demographicgraphic
        for i in range(len(demographic_columns)):
            df[demographics_weighted_wave[i]+'_believe'] = df[demographics_weighted_wave[i]] * df['humans_cause']
            believer_columns.append(demographics_weighted_wave[i]+'_believe')
        print(df.columns)
        # self.believer_columns = believer_columns
        return believer_columns
    
    def create_df_aggregated(self,df,believer_columns,demographics_weighted_wave):
        df1 = df[believer_columns]
        df2 = df[demographics_weighted_wave]
        df3 = df['year']
        df_concat = pd.concat([df1, df2, df3], axis=1)
        df_aggregated = df_concat.groupby('year').agg(np.sum)
        print(df_aggregated.describe())
        print(df_aggregated.info())
        return df_aggregated

    def create_percent_believe_columns(self,demographic_columns,df_aggregated,believer_columns,demographics_weighted_wave):
        percent_columns = []
        for i in range(len(demographic_columns)):
            df_aggregated['percent_'+demographic_columns[i]+'_believe'] = (df_aggregated[believer_columns[i]] / df_aggregated[demographics_weighted_wave[i]]) * 100
            percent_columns.append('percent_'+demographic_columns[i]+'_believe')
        print(df_aggregated.describe())
        print(df_aggregated.info())

    # df_percent_change = dfregated[percent_columns]

if __name__ == "__main__":
    DemographicAnalysis.split_demographics() # <---------- separate coded demographics from category column, create columns for each demographic
    DemographicAnalysis.apply_weight_wave(self,df,demographic_columns)  # <---------- create new columns with individuals' weight based on wave, since we are grouping by year
    DemographicAnalysis.believers_per_demographic(self,df,demographic_columns,demographics_weighted_wave) # <--- create new columns with just the weights of believers for each demographic
    DemographicAnalysis.create_df_aggregated(self,df,believer_columns,demographics_weighted_wave) # <-------- aggregate and sum to get total believers and total population per demographic
    DemographicAnalysis.create_percent_believe_columns(self,demographic_columns,df_aggregated,believer_columns,demographics_weighted_wave) # < use your newly aggregated believers and total population columns to calculate % belief per year
 
'''
--DF--
y-ax: categories within columns
x-ax: % belief per year
for loop that iterates through rows, 
identifies min and max, 
adds tuple to an empty matrix [].

--NEW DF--
y-ax: categories within columns
x-ax: difference % change
'''
