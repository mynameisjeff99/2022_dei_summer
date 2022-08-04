# <font color="Salmon">gender_race_recognition</font>

This directory contains the files related to gender and race detection.

## <font color="IndianRed">Items:</font>
- <font color="orange">experimenting</font>: the folder contains the .ipynb files during the experimentation.
- <font color="orange">deepface</font>: the repository from [serengil/deepface](https://github.com/serengil/deepface). The output provides percentages for the gender recognition. (the package DeepFace doesn't)
- <font color="orange">gender_census_data</font>: the folder contains files recording first name, gender, and percentage of each race in the US. They are used to build the gender guesser. Data can be found in https://www.ssa.gov/oact/babynames/limits.html.
- <font color="orange">race_census_data</font>: the folder contains files recording last name, race, and percentage of each race in the US. They are used to build the race guesser. Data can be found in https://www.census.gov/topics/population/genealogy/data/2010_surnames.html.
- <font color="orange">get_census_name_csv.ipynb</font>: transform the census data to .csv files.
- <font color="orange">gender_race_recognition_pct.py (gender_race_recognition_pct.ipynb for application)</font>: module for inferring gender and race percentages from the name and headshot of profiles.
- <font color="orange">data_labeling.ipynb</font>: the notebook for manually labeling gender and race of profiles for the train/test set.
- <font color="orange">classify_from_pct_data.ipynb</font>: the notebook contains the training of classifiers to predict the gender and race of profiles from the percentage data.

## <font color="IndianRed">How to use (<font color="orange">data_labeling.ipynb</font>):</font>
### <font color="SteelBlue">Import relevant packages</font>
    import sys
    import json
    import requests
    import random
    import PIL.Image
    from IPython.display import Image, clear_output
    from io import BytesIO
### <font color="SteelBlue">Get the json file</font>
    the_school = get_school_json(school)
- Parameters:
  - school (str): the name of school (lower)
- Returns:
  - the_school (list of dict): the list containing all departments' information.
### <font color="SteelBlue">Label the profile</font>
    count = data_labeling(the_school, count):
- Parameters:
  - the_school (list of dict): the list containing all departments' information.
  - count (int): the number of profiles already labeled.
- Returns:
  - count (int): the number of profiles already labeled.
- It randomly selects unlabeled profiles. For each profile, the name and image of the profile will be displayed. 
- The user will have to enter {g}{r} as the input. {g} is the first letter of the gender ('u': 'unknown', 'm': 'male', 'f': 'female'). {r} is the first letter for the race ('u': 'unknown', 'w': 'white', 'a': 'api', 'b': 'black', 'h': 'hispanic', 'n': 'native').
- After the user entering the input. race_labeled and gender_labeled will be added to the profile dict.
### <font color="SteelBlue">Example</font>
    columbia = get_school_json('columbia')
    count = 0
    count = data_labeling(columbia, count)
    with open(sys.path[0] + '/../data/columbia/columbia_w_profiles_labeled.json', 'w') as f:
        json.dump(columbia, f)

## <font color="IndianRed">How to use (<font color="orange">gender_race_recognition_pct.py</font>):</font>
### <font color="SteelBlue">Import the module and initialize the object</font>
    from gender_race_recognition_pct import GenderRaceRecognition
    recognition = GenderRaceRecognition()
### <font color="SteelBlue">Get the input and output path</font>
    in_path, out_path = get_paths(school)
- Parameters:
  - school (str): the name of school (lower)
- Returns:
  - in-path (str): specifies the path for the json file to be processed.
  - out_path (str): specifies the path for the output of processed json file.
### <font color="SteelBlue">Add percentage data (gender and race) to the profiles</font>
    the_school = recognition.detect_gender_race(in_path, out_path)
- Returns: 
  - the_school (list of dict): updated department information with profiles having percentage data added.
- the_school is also dumped as a json file in the location specified in the out_path.
### <font color="SteelBlue">Example</font>
    in_path, out_path = get_paths('columbia')
    columbia = recognition.detect_gender_race(in_path, out_path)

## <font color="IndianRed">How to use (<font color="orange">classify_from_pct_data.ipynb</font>):</font>
### <font color="SteelBlue">Import relevant packages and changes the sns setting</font>
    import sys
    import json
    import numpy as np
    import pandas as pd
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB, GaussianNB
    from sklearn.linear_model import LogisticRegression
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style="white")
### <font color="SteelBlue">Get the json file</font>
    the_school = get_school_json(school)
- Parameters:
  - school (str): the name of school (lower)
- Returns:
  - the_school (list of dict): the list containing all departments' information.
### <font color="SteelBlue">Get gender and race pct data from a particular profile</font>
    the_profile = get_profile(profile)
- Parameters:
  - profile (dict): the profile of a particular faculty member.
- Returns:
  - the_profile (dict): the gender and race pct data of that profile.
### <font color="SteelBlue">Transform the all the pct data into a df and train the classifiers</font>
- See the notebook for details
- Currently, logistic regression is used for gender. Multinomial naive Bayes is used for race.
### <font color="SteelBlue">Detect the gender and race of a profile</font>
    the_gender = detect_gender(row, clf)
    the_race = detect_race(row, clf)
- Parameters:
  - row (a row in the df): the row containing the gender/race pct data.
  - clf (sklearn model): the trained classifier.
- Returns:
  - the_gender/the_race (str): the gender/race inferred from the pct data.
- All the profiles are classified (df with new columns race_detected and gender_detected). See the notebook for details.
### <font color="SteelBlue">Update the profiles in school list</font>
- See the notebook for details

## <font color="IndianRed">To-do:</font>
- Reorganize the folder for clarity.
- Separate get_census_names_csv into 2 files.
- Separate data_labeling into 2 files.
- Separate classify_from_pct_data into 2 files.
- Improve the gender guesser to place more weight for names used by people born in 1950-1990.
- In classify_from_pct_data, find a better way to classify partial-detected data (i.e. having pct data inferred from only name or only image)