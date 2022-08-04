# <font color="Salmon">data_cleaning</font>

This directory contains the modules for data cleaning.

## <font color="IndianRed">Items:</font>
- <font color="orange">experimenting</font>: the folder contains the .ipynb files during the experimentation.
- <font color="orange">directory_cleaning.ipynb</font>: contains both the methods and application for reviewing and correcting the faculty pages scraped.
- <font color="orange">profile_cleaning.py (profile_cleaning.ipynb for its application)</font>: contains the methods for standardizing the formats of profiles (names, ranks, urls)
- <font color="orange">dedupe_profiles_within_department.py</font>: dedupe the profiles.
- <font color="orange">gender_race_cleaning.ipynb</font>: contains both the methods and application for standardizing the formats of gender and race data inferred.
- <font color="orange">adding_gender_race_metadata.py (adding_gender_race_metadata.ipynb for its application)</font>: Add gender and race metadata to each department's info.

## <font color="IndianRed">How to use (<font color="orange">directory_cleaning.ipynb</font>):</font>
### <font color="SteelBlue">Import relevant packages</font>
    import time 
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
### <font color="SteelBlue">Get Selenium driver</font>
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
### <font color="SteelBlue">Check page</font>
    check_page(url, driver)
- The driver will get the web page from the url indicated and stop for 5 seconds for the user's manual inspection
### <font color="SteelBlue">Example</font>
    columbia = pd.read_json(sys.path[0] + '/../data/columbia/columbia_directories_updated.json')
    to_check = []

    # manually inspect the first 20 web pages
    for i in range(20):
        print("__________")
        print(i, columbia.loc[i, 'department'])
        url = columbia.loc[i, 'faculty_page']
        if url is None:
            to_check.append(i)
        else:
            check_page(url, driver)

    # add the index of incorrect pages
    to_check = []
    to_check.extend([0,3,6])

    # then manually find the correct page
    update = []
    update.append([0, "https://www8.gsb.columbia.edu/faculty-research/divisions/accounting/faculty-research"])
    update.append([3, "https://www.anesthesiology.cuimc.columbia.edu/about-us/our-people/our-faculty"])
    update.append([6, "https://www.apam.columbia.edu/directory?gsarqfields%5Bbiotypetid%5D=30"])
    
    # update the pages
    for u in update:
    row = u[0]
    new = u[1]
    columbia.loc[row,'faculty_page'] = new

    # drop med schools
    to_drop = []
    for i in columbia.index:
        if 'cumc' in columbia.iloc[i, 1] or columbia.iloc[i, 2] is None:
            to_drop.append(i)
    columbia_directories_sans_med = columbia.drop(to_drop)
    
    # dump as json file
    columbia_directories_sans_med.to_json(sys.path[0] + '/../data/columbia/columbia_directories_sans_med.json', orient="records")

## <font color="IndianRed">How to use (<font color="orange">profile_cleaning.py</font>):</font>
### <font color="SteelBlue">Import the module and initialize the object</font>
    from profile_cleaning import ProfileCleaning
    p_cleaning = ProfileCleaning()
### <font color="SteelBlue">Clean the profiles</font>
    processed_school_list = p_cleaning.clean_profiles(in_path, out_path)
- Parameters:
  - in-path (str): specifies the path for the json file to be processed.
  - out_path (str): specifies the path for the output of processed json file.
- Returns:
  - processed_school_list (list of dict): the list containing departments info with processed profiles.
- The function separates the first/middle/last names, detects the academic rank, and formats the url for each profile.
- The updated list is also dumped as a json file to the location specified in the out_path.

### <font color="SteelBlue">Example</font>
    p_cleaning = ProfileCleaning()
    in_path = sys.path[0] + '/../data/columbia/columbia_test_sans_processing.json'
    out_path = sys.path[0] + '/../data/columbia/columbia_test_processed.json'
    columbia_processed = p_cleaning.clean_profiles(in_path, out_path)

## <font color="IndianRed">How to use (<font color="orange">adding_gender_race_metadata.py</font>):</font>
### <font color="SteelBlue">Import the module and initialize the object</font>
    from adding_gender_race_metadata import AddGenderRaceMetadata
    a = AddGenderRaceMetadata()
### <font color="SteelBlue">Add the metadata</font>
    a.add_gender_race_metadata(the_school)
- Parameters:
  - the_school(the list of dictionary containing a school's department info)
- The function adds the metadata summarizing each department's gender and race data as gender_race_data in the department's dict
