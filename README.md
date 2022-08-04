# <font color="Salmon">2022_dei_summer</font>

#### This is a project to collect, store, and analyze the diversity metrics for university departments.  

## <font color="IndianRed">Items:</font>
- <font color="orange">get_faculty_pages</font>: finding the faculty pages of university departments.
- <font color="orange">web_scraping</font>: scraping the faculty pages and NCES data.
- <font color="orange">gender_race_recognition</font>: developing and implementing machine learning models to predict each faculty member's gender and race.
- <font color="orange">data_cleaning</font>: processing the data collected.
- <font color="orange">data</font>: storing data collected throughout the process.
- <font color="orange">output</font>: storing summary of data collected and findings.
- <font color="orange">analysis</font>: conducting data analysis and visualization.  

**<font color="SandyBrown">Detailed descriptions of files and instructions can be found in the README file of each folder.</font>**

## <font color="IndianRed">The pipeline with <font color="HotPink">relevant files</font> (<font color="Purple">modules containing functions</font> are listed between brackets)</font>

### <font color="SteelBlue">1. Get the faculty directories for a school and inspect the data</font>
   - get_faculty_directories/<font color="HotPink">find_faculty_directories.ipynb</font>
   - data_cleaning/<font color="HotPink">directories_cleaning.ipynb</font>
### <font color="SteelBlue">2. Scrape the faculty directories and clean the profiles</font>
   - web_scraping/<font color="HotPink">scraping_{school}.ipynb</font> (<font color="Purple">scraping.py</font>) 
   - data_cleaning/<font color="HotPink">profile_cleaning.ipynb</font> (<font color="Purple">profile_cleaning.py</font>)
   - data_cleaning/<font color="HotPink">dedupe_profiles_within_department.ipynb</font>
### <font color="SteelBlue">3. Deploy ML models to get profile's gender and race data in the form of percentage</font>
   - gender_race_recognition/<font color="HotPink">gender_race_recognition_pct.ipynb</font> (<font color="Purple">gender_race_recognition_pct.py</font>)
### <font color="SteelBlue">4. Deploy ML models to classify gender and race based on the pct data and add metadata to each department</font>
   - gender_race_recognition/<font color="HotPink">classify_from_pct_data.ipynb </font>
   - data_cleaning/<font color="HotPink">adding_gender_race_metadata.ipynb</font> (<font color="Purple">adding_gender_race_metadata.py</font>)
### <font color="SteelBlue">5. Conduct data analysis and visualization</font>
   - analysis/<font color="HotPink">gender_race_data_visualization.ipynb</font>  
   
**<font color="SandyBrown">This only includes the most basic tasks, descriptions of other tasks can be found in each folder's README file.</font>**

**<font color="FireBrick">\*Attention: the data folders are reorganized, if the input/output paths are in correct in the notebooks, use "../data/data_during_process" instead.</font>**