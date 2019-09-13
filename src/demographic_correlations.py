import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
import pyreadstat

def split_demographics():
    # columns_to_split = input('Which categories do you want to split? ') <----interative for future users
    for i1 in range(len(columns_to_split)):
        for i2 in range(1, int(df.loc[:,columns_to_split[i1]].max()+1)):
            df[demographics[i1][i2-1]] = np.where(df.loc[:,columns_to_split[i1]]==i2,1,0)
            demographic_columns.append(demographics[i1][i2-1])
            print(df[demographics[i1][i2-1]], "has been added to the dataframe.")
        print(df.columns)
    print(demographic_columns)

def apply_weight_wave():
    for i in range(len(demographic_columns)):
        df[demographic_columns[i]+'_weighted_wave'] = df[demographic_columns[i]] * df['weight_wave']
        demographics_weighted_wave.append(demographic_columns[i]+'_weighted_wave')
    print(df.columns)

demographics_weighted_agg = []
def apply_weight_aggregate():
    for i in range(len(demographic_columns)):
        df[demographic_columns[i]+'_weighted_agg'] = df[demographic_columns[i]] * df['weight_aggregate']
        demographics_weighted_agg.append(demographic_columns[i]+'_weighted_agg')
    print(df.columns)

def believers_per_demographic():
    df['humans_cause'] = np.where(df['cause_original']==1, 1, 0) # dividend column for calculating % belief for each demographic
    for i in range(len(demographics_weighted_wave)):
        df[demographics_weighted_wave[i]+'_believe'] = df[demographics_weighted_wave[i]] * df['humans_cause']
        believer_columns.append(demographics_weighted_wave[i]+'_believe')
    print(df.columns)

def create_df_aggregated():
    df1 = df[believer_columns]
    df2 = df[demographics_weighted_wave]
    df3 = df['year']
    df_concat = pd.concat([df1, df2, df3], axis=1)
    df_agg = df_concat.groupby('year').agg(np.sum)
    print(df_agg.describe())
    print(df_agg.info())
    print(df_agg.head(10))
    for i in range(8):
        demo_array = df_agg.iloc[i].values
        aggregated_matrix[i,0:41] = demo_array
    print(demo_array)

def create_percent_believe_columns():
    for i in range(len(demographic_columns)):
        df_aggregated['percent_'+demographic_columns[i]+'_believe'] = (df_aggregated[believer_columns[i]] / df_aggregated[demographics_weighted_wave[i]]) * 100
        percent_columns.append('percent_'+demographic_columns[i]+'_believe')
    print(df_aggregated.describe())
    print(df_aggregated.info())

def find_delta_max():
    # for i in range(len(df_percent_change.columns)):
    #     d = df_percent_change.iloc[:,i]
    #     if d.idxmax() < d.idxmin():
    #         np.insert(delta_max,i,(min(d) - max(d)))
    #     else:
    #         np.insert(delta_max,i,(max(d) - min(d)))
    # d = df_percent_change.iloc[:,i]
    # diff = max(d) - min(d)
    # np.insert(delta_max,i,diff)
    for i in range(len(df_percent_change.columns)):
        col = df_percent_change.iloc[:,i]
        diff = max(col) - min(col)
        delta_max.append(diff)
    print(delta_max)
    delta_max[2] = 6.547239

def plot_bar_graph():
    N = 20
    labels = my_df_sorted['Demographics']
    data = my_df_sorted['Delta Max']
    
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(figsize=(5, 10))
    width = .8
    tickLocations = np.arange(20)
    ax.bar(tickLocations, data, width, linewidth=4, align='center')
    
    ax.set_xticks(ticks=tickLocations)
    ax.set_xticklabels(labels, rotation=75,fontsize=10)
    ax.set_xlim(0,21)
    ax.set_yticks(range(40)[1:])
    ax.set_ylim((0,40))
    ax.set_ylabel('Max Delta')
    ax.set_xlabel('Demographics')
    ax.yaxis.grid(True)
    ax.set_title("Most Dramatic Changes in Climate Change Sentiment by Demographic, 2010-2017,")
    fig.tight_layout
    plt.show()

if __name__ == "__main__":
    df, meta = pyreadstat.read_sav('/Users/lazarus/galvanize/datasets/osfstorage-archive/CCAM SPSS Data.sav')
    df.to_csv('/Users/lazarus/galvanize/capstone_1/data/climate_survey_data.csv')

    # get rid of 2008...
    df = df[df.year != 1]

    columns_to_split = ['gender', 'generation', 'income_category', 'race', 'party_x_ideo'] # choose which demographics to separate from their column categories
    demographics = [['male', 'female'], ['igen_genz', 'millenials', 'gen_x', 'baby_boomers', 'silent', 'greatest'], ['<50k', '50k-99k', '100k<'], ['white', 'black', 'other', 'hispanic'], ['lib_dem', 'mod_dem', 'independent', 'mod_rep', 'con_rep']]
    demographic_columns = []

    split_demographics() # <------------ separate coded demographics from category column, create columns for each demographic
    
    demographics_weighted_wave = []
    apply_weight_wave()  # <------------ create new columns with individuals' weight based on wave, since we are grouping by year

    believer_columns = []
    believers_per_demographic() # <----- create new columns with just the weights of believers for each demographic

    aggregated_matrix = np.empty([8,40]) 
    create_df_aggregated() # <---------- aggregate and sum to get total believers and total population per demographic

    believer_and_total_cols = believer_columns + demographics_weighted_wave
    df_aggregated = pd.DataFrame(data=aggregated_matrix,columns=believer_and_total_cols)

    percent_columns = []
    create_percent_believe_columns() # < use your newly aggregated believers and total population columns to calculate % belief per year

    df_percent_change = df_aggregated[percent_columns]
    
    delta_max = []

    find_delta_max() # <---------------- take the difference of the max and min 

    my_array = np.array(delta_max)
    my_dict = {'Delta Max': delta_max, 'Demographics': demographic_columns}
    my_df = pd.DataFrame(my_dict)
    my_df_sorted = my_df.sort_values(by=['Delta Max'])
    plot_bar_graph()
