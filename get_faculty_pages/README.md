# <font color="Salmon">get_faculty_pages</font>

This directory contains a file that allows users to find faculty directories.

## <font color="IndianRed">Item:</font>
- <font color="orange">find_faculty_pages.ipynb</font>: both the methods for scraping directories (from a source containing links to all department pages of a university) and its application. 

## <font color="IndianRed">How to use (<font color="orange">find_faculty_pages.ipynb</font>):</font> 
### <font color="SteelBlue">Import relevant packages</font>
    import re
    import json
    import sys
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
### <font color="SteelBlue">Get Selenium driver</font>
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
### <font color="SteelBlue">Find department pages</font>
    department_pages = find_department_pages(driver, departments_url, no_pages, css_selector, nth_element):
- Parameters:
  - driver: the Selenium driver.
  - departments_url (str): the url of the web page containing links to websites of every department of a school.
  - no_pages (int): the number of pages in the webpage.
  - css_selector (str): the css_selector for the html tags containing information of each department. 
  - nth_element (int): the nth child in the selected tag containing information of the department. (only applicable for some pages)
- Returns:
  - department_pages (list of dict): each dict contains the name of the department and its url.
- The standard method doesn't work for all pages, new scrapers have to build if this doens't work.
### <font color="SteelBlue">Find the directory within the department page</font>
    faculty_page = find_faculty_page(driver, url)
- Parameters:
  - driver: the Selenium driver.
  - url (str): the link for the department page.
- return: faculty_page (str): the url of a particular departments.
- Sometimes the url selected might not be the correct one. Manual inspection are required. (directories_cleaning in the data_cleaning folder)
### <font color="SteelBlue">Example</font>
    departments_url = "https://www.columbia.edu/content/academics/departments"
    no_pages = 5
    css_selector = '.dynamic-grid-listing-item.grid-item.angular-animate.ng-trans.ng-trans-fade-down.ng-scope'
    columbia_departments = find_department_pages(driver, departments_url, no_pages, css_selector)
    for item in columbia_departments:
        url = item.get('url')
        item.update({'faculty_page': find_faculty_page(driver, url)})
    with open(sys.path[0] + '/../data/columbia/columbia_directories_updated.json', 'w') as f:
        json.dump(columbia_departments, f)

## <font color="IndianRed">To-do:</font>
- Divide the methods and application into 2 files.
- Improve the success rate for guessing the faculty page.
