import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
import pyreadstat

# pyreadstat is a python package to read and write 
# sas (sas7bdat, sas7bcat, xport), 
# spps (sav, zsav, por) and 
# stata (dta) data files into/from pandas dataframes. 

# df, meta = pyreadstat.read_sas7bdat('/path/to/a/file.sas7bdat')

df, meta = pyreadstat.read_sav('/Users/lazarus/galvanize/capstone_1/osfstorage-archive/CCAM SPSS Data.sav')
df.to_csv('/Users/lazarus/galvanize/capstone_1/data/climate_survey_data.csv')

# Which region has the largest conversion rate? (% increase in yes-anthropogenic)

# new dataframe only showing respondents indicating climate change 
# is happening and mostly caused by humans
# df_yes_human = df[(df['happening']==3) & (df['cause_original']==1)]

# ??? df['yes_humans'] = np.where(df[(df['happening']==3) & (df['cause_original']==1)], 1, 0)

df = df[df.year != 1]
df['humans_cause'] = np.where(df['cause_original']==1, 1, 0)

'''
def replace_code_with_name('<col>',old=[],new=[]):
    for x in zip(old,new):
        df = df.replace({'col' : x}, {'col' : y}, regex=???)
'''

df_slim = df[['year','humans_cause','region9', 'case_ID']]

''' ???
def create_regional_df(region=1 OR 'ne'):
    df_{} = df_slim[df_slim.region9 =={}.format(region)]
    df_{}_grouped = df_{}.groupby('year').agg({
    'humans_cause' : np.sum,
    'case_ID' : np.count_nonzero
})
'''

df_ne = df_slim[df_slim.region9 == 1]

df_ne_grouped = df_ne.groupby('year').agg({
    'humans_cause' : np.sum,
    'case_ID' : np.count_nonzero
})

df_ne_grouped.rename(columns={'case_ID' : 'total_asked'}, inplace=True)

df_ne_grouped['percent_yes'] = (df_ne_grouped['humans_cause'] / df_ne_grouped['total_asked']) * 100

plt.style.use('fivethirtyeight')
x = np.linspace(2010,2017,8)
y_1_ne = df_ne_grouped.percent_yes
fig, ax = plt.subplots(figsize=(12,8))
ax.plot(x, y_1_ne, alpha=.75, linewidth=4, label='New England')
ax.set_title('American Belief in Climate Change by Region (2010-2017)')
ax.set_xlabel('Year')
ax.set_ylim(40,70)
ax.set_ylabel('Percent Belief in Antrhopogenic Climate Change')
ax.legend()
plt.show()