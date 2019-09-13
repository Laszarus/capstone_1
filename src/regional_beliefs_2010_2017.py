import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
import pyreadstat

'''
pyreadstat is a python package to read and write: 
-sas (sas7bdat, sas7bcat, xport)
-spps (sav, zsav, por)
-stata (dta)
data files into/from pandas dataframes
'''

df, meta = pyreadstat.read_sav('/Users/lazarus/galvanize/datasets/osfstorage-archive/CCAM SPSS Data.sav')
df.to_csv('/Users/lazarus/galvanize/capstone_1/data/climate_survey_data.csv')

'''
Each respondent was given a weight, based on the sample demographics vs the US census demographics, in order to 
make the sample responses more accurately reflect those of the whole population. Essentially the weighted columns
will be summed instead of counting a particular variable. 
'''

# this survey is weird and skips 2009? so i'm just going to start at 2010 for the sake of consistency...
# setting up new columns to sum later
df = df[df.year != 1]

df['humans_cause'] = np.where(df['cause_original']==1, 1, 0)
df['humans_cause_weighted'] = df['humans_cause'] * df['weight_wave']

# 'slimming' down the dataframe to the relevant columns
df_slim = df[['region4','year','humans_cause','humans_cause_weighted','weight_wave']]

# creating a 4x8 matrix with regions on the y-axis, years on the x-axis, % belief per year per region
region_matrix = np.empty([4,8])
def create_region_matrix():
    for i in range(4):
        region_df = df_slim[df_slim.region4 == i + 1]
        region_df = region_df.groupby('year').agg({
            'humans_cause' : np.sum,
            'humans_cause_weighted' : np.sum,
            'weight_wave' : np.count_nonzero
        })
        region_df.rename(columns={'weight_wave' : 'total_asked'}, inplace=True)
        region_df['percent_yes'] = (region_df['humans_cause'] / region_df['total_asked']) * 100
        region_array = region_df['percent_yes'].values
        region_matrix[i, 0:9] = region_array

# same thing, but with weighted scores...
region_matrix_weighted = np.empty([4,8])
def create_region_matrix_weighted():
    for i in range(4):
        region_df = df_slim[df_slim.region4 == i + 1]
        region_df = region_df.groupby('year').agg({
            'humans_cause' : np.sum,
            'humans_cause_weighted' : np.sum,
            'weight_wave' : np.sum,
        })
        region_df.rename(columns={'weight_wave' : 'total_asked_weighted'}, inplace=True)
        region_df['percent_yes_weighted'] = (region_df['humans_cause_weighted'] / region_df['total_asked_weighted']) * 100
        region_array_weighted = region_df['percent_yes_weighted'].values
        region_matrix_weighted[i, 0:9] = region_array_weighted

def plot_regions():
    names = ['Northeast', 'Midwest', 'South', 'West']
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(figsize=(12,8))
    x = np.linspace(2010, 2017, 8)

    for i in range(4):
        y = region_matrix_weighted[i, :]
        ax.plot(x, y, alpha=.75, linewidth=4, label=names[i], marker='h')
    ax.set_title('American Belief in Climate Change by Region (2010-2017)')
    ax.set_xlabel('Year')
    ax.set_ylim(40,65)
    ax.set_ylabel('Percent Belief in Antrhopogenic Climate Change')
    ax.legend()
    plt.show()
    fig.savefig('/Users/lazarus/galvanize/capstone_1/images/weighted_region4_plot.png')

