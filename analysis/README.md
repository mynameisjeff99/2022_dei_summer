# <font color="Salmon">analysis</font>

This directory contains a notebook used for exploratory data analysis.

## <font color="IndianRed">Items:</font>
- <font color="orange">experimenting</font>: the folder contains the .ipynb files during the experimentation.
- <font color="orange">gender_race_data_visualization.ipynb</font>: the file for exploratory data analysis.

## <font color="IndianRed">How to use (<font color="orange">gender_race_data_visualization.ipynb</font>):</font>
### <font color="SteelBlue">Import relevant packages</font>
    import numpy as np
    import pandas as pd
    import sys
    import json
    import matplotlib.pyplot as plt
### <font color="SteelBlue">Get the df containing a school's departmental gender and race data</font>
    the_departmental_df = get_departmental_df(the_school)
- Parameters:
  - the_school (list of dict): containing all the department info of a school.
- Returns:
  - the_departmental_df (pd.DataFrame): a df with the rows containing the number of faculty members being in each category grouped by department, rank. E.g. {department: stats, rank: professor, gender_male: 9, race_white: 8, race_hispanic: 1}
### <font color="SteelBlue">Get the df in pct</font>
    the_departmental_pct_df = get_pct_df(the_departmental_df)
- Returns:
  - the_departmental_pct_df (pd.DataFrame): similar to the_departmental_df, but rather than having ints, it has percentages.
- When calculating the percentages, it excludes unknown. E.g. 10 male, 10 female, 5 unknown --> 50% male
- the_departmental_pct_df is dumped as a json file in the output folder

### <font color="SteelBlue">Get the whole school df in pct</font>
    the_whole_school_pct_df = get_whole_school_pct_df(the_departmental_df)
- Returns:
  - the_whole_school_pct_df (pd.DataFrame): similar to the_departmental_pct_df, but aggregated for the whole school.
- he_whole_school_pct_df is dumped as a json file in the output folder

### <font color="SteelBlue">Visualization</font>
- See the notebook for details.
- A comparison with the data from the NCES human resources data (the scraper is in the web_scraping folder) is also included. E.g. For columbia the data can be found in https://nces.ed.gov/ipeds/datacenter/FacsimileView.aspx?surveyNumber=9&unitId=166027&year=2020

## <font color="IndianRed">To do:</font>
- Further analyze the data.
- Conduct analysis for departments across schools.
