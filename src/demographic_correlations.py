import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
import pyreadstat

df, meta = pyreadstat.read_sav('/Users/lazarus/galvanize/datasets/osfstorage-archive/CCAM SPSS Data.sav')
df.to_csv('/Users/lazarus/galvanize/capstone_1/data/climate_survey_data.csv')

'''
end product: bar graph of each static demographicgraphic's % change in belief
static demographicgrpahics:
'gender'_______2
'generation'___6
'income_category'_3
'race'_________4
'party_x_ideo'_6
SPECIAL CASE ***'religion'____15***
SPECIAL CAE ***'evangelical'__4 # look up evangelical environmental movement ***
'''

# get rid of 2008 again...
df = df[df.year != 1]

# dividend column for calculating % belief for each demographicgraphic
df['humans_cause'] = np.where(df['cause_original']==1, 1, 0)

# choose which demographics to separate from their column categories

columns_to_split = ['gender', 'generation', 'income_category', 'race', 'party_x_ideo']
# columns_to_split = input('Which categories do you want to split? ') <----interative for future users

demographics = [['male', 'female'], ['igen_genz', 'millenials', 'gen_x', 'baby_boomers', 'silent', 'greatest'], ['<50k', '50k-99k', '100k<'], ['white', 'black', 'other', 'hispanic'], ['lib_dem', 'mod_dem', 'independent', 'mod_rep', 'con_rep']]

# split demographics into serparate columns
new_columns = []
def split_demographics(col=columns_to_split):
    for i1 in range(len(columns_to_split)):
        for i2 in range(1, int(df.loc[:,columns_to_split[i1]].max()+1)):
            df[demographics[i1][i2-1]] = np.where(df.loc[:,columns_to_split[i1]]==i2,1,0)
            new_columns.append(demographics[i1][i2-1])
            print(df[demographics[i1][i2-1]], "has been added to the dataframe.")
        print(df.columns)
    print(new_columns)

# interactive version
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

def apply_weight_wave():
    for i in range(len(new_columns)):
        df[new_columns[i]+'_weighted'] = df[new_columns[i]] * df['weight_wave']
    print(df.columns)

def apply_weight_aggregate():
    for col in new_columns:
        df[col.join(['_weighted'])] = df[col] * df['weight_aggregate']
        print(type(df[col]))

    # print(df.columns)

'''
now we'll need a weighting function, first using 'weight_wave' because we just want to 
isolate 'percent_yes' for each demographicgraphic per year to identify highs and lows
'''

'''
delta metric should be from the **lowest** % belief level to the highest over the 10-year span 
LOWEST. 

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
