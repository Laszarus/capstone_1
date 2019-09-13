# Who Cares About Climate Change? (2010-2017)
To better understand Americans’ views on climate change, the [Yale Program on Climate Change Communication (YPCCC)] (http://climatecommunication.yale.edu/) and the [George Mason University Center for Climate Change Communication (Mason 4C)](http://www.climatechangecommunication.org/) have conducted nationally representative surveys of U.S. adults twice a year for the past decade. 

## The Data
Surveys were administered twice a year in 'waves' from 2010-2017 (appproximately 2-3k a year). They were also administered in 2008, but not in 2009, 
so to avoid making assumptions about a gap in the data, I just cut that year out. That leaves us with:

**52 columns, 17,860 points:**
    - 3 metadata columns
    - 2 weighting columns
    - 18 opinion questions, bucketed
    - 29 demographical questions, bucketed

**
```
      happening  cause_original cause_other_text  cause_recoded  sci_consensus
2169        3.0             2.0                             4.0            2.0
2170        3.0             2.0                             4.0            2.0
2171        3.0             1.0                             6.0            1.0
2172        1.0             2.0                             4.0            2.0
2173        3.0             2.0                             4.0            1.0
```
![](/images/survey_questions_snap.png)
```
In [11]: df.iloc[1364, 7]                                                                                                                                                                     
Out[11]: 'with the world so hate mongered the lord will soon comr to take us home'
```

**Weighting** 
Designed to make samples better reflect census data based on age, gender, race, region, metropolitan status, education, and income.







