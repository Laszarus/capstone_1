import pandas as pd

def dta_to_csv(ds_name, dta_name, csv_name):
    name = pd.io.stata.read_stata(dta_name)
    name.to_csv(csv_name)
    
# navigate to ‎⁨/Users⁩/lazarus⁩/galvanize⁩/⁨local_data⁩/climate_beliefs 

# dataset_s1 = pd.io.stata.read_stata('S1_Dataset.DTA')
# data.to_csv('my_stata_file.csv')