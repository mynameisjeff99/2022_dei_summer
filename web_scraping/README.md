# <font color="Salmon">web_scraping</font>

This directory contains the modules and applications related to scraping data from faculty directories.

## <font color="IndianRed">Items:</font>
- <font color="orange">experimenting</font>: folder containing .ipynb files during the experimentation,
- <font color="orange">scraping_{method}.py</font>: modules containing different methods for scraping profiles from university departments' faculty pages.
- <font color="orange">scraping.py</font>: the script containing the driver function for scraping profiles.
- <font color="orange">scraping_{school_name}.ipynb</font>: the application of scraping (currently for 8 Ivy League schools).
- <font color="orange">scrape_nces_data.ipynb</font>: the notebook used to scrape data from the NCES databse for comparison.

## <font color="IndianRed">How to use (<font color="orange">scraping.py</font>):</font> 
### <font color="SteelBlue">Import and initialize the object</font>
    from scraping import Scraping
    scraping = Scraping()
### <font color="SteelBlue">Scrape profiles for an individual directory</font>
    profiles = scraping.get_department_info(url)
- Parameter:
  - url (str): the url for a web page containing a directory.
- Returns:
  - profiles (list of dict): a list of profiles contained in the directory.
- Currently, it has estimated success rate of 90% (getting some profiles). However, in some cases, not all the profiles are scraped. 
### <font color="SteelBlue">Scrape profiles for multiple directories</font>
    result_multiple_directories = scraping.scrape_faculty(in_path, out_path)
- Parameters:
  - in-path (str): specifies the path for the json file containing faculty directory's url.
  - out_path (str): specifies the path for the output of the scraping.
- Returns:
  - info of departments containing profiles (list of dict): the original list of departments info (from in_path) with profiles scraped. 
- The info of departments containing profiles are also dumped as a json file saved to the location specified in the out_path.
- A logging (scraping_log.log) containing the failures and information during the scraping process are also saved in the folder specified in the out_path.
### <font color="SteelBlue">Example</font>
    in_path = sys.path[0] + '/../data/columbia/columbia_directories_sans_med.json'
    out_path = sys.path[0] + '/../data/columbia/columbia_w_profiles.json'
    columbia = scraping.scrape_faculty(in_path, out_path)

## <font color="IndianRed">How to use (<font color="orange">scrape_nces_data.ipynb</font>):</font>
### <font color="SteelBlue">Get Selenium driver</font>
    driver = get_driver()
### <font color="SteelBlue">Get the url containing the human resources data</font>
    url = get_school_url(unitid)
- Parameters:
  - unitid (str): the NCES UnitID of a particular school (can be found by searching in https://nces.ed.gov/)
- Returns:
  - url (str): the url of the web page containing the human resources information submitted by the school.
- Currently, the latest data is for 2020.
### <font color="SteelBlue">Get the bs4 soup</font>
    soup = get_soup(url, driver)
### <font color="SteelBlue">Scrape the data</font>
    result = get_tenured_tenure_track_data(soup)
- Returns:
  - NCES demographic data (dict of dict): Dictionary containing a school's NCES demographic data, the first level is gender, the second level is academic ranks.
- The data is also dumped as a json file in the data folder.
- Currently, only data for Professors, Associate professors, and Assistant professors are collected.
### <font color="SteelBlue">Example:</font>
    driver = get_driver()
    columbia_unitid = 190150
    columbia_url = get_school_url(columbia_unitid)
    soup = get_soup(school_url, driver)
    result = get_tenured_tenure_track_data(soup)

## <font color="IndianRed">To-do:</font>
- Improve the success rate of scraping.
- Find a way to verify whether all the profiles are scraped.
- Modify the try-except blocks to specify the exceptions.