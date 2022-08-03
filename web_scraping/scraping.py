"""The module is for scrape profiles

This module combines 4 scraping methods to scrape profiles from faculty pages.
"""

import logging
import json
from scraping_helpers import ScrapingHelpers
from scraping_tr import ScrapingTr
from scraping_class_name import ScrapingClass
from scraping_children import ScrapingChildren
from scraping_bf import ScrapingBf


class Scraping:
    """This is the driver class for scraping profiles using the combination of methods.

    Attributes:
        url(str): the link for a particular faculty page.
    """

    def __init__(self):
        """The constructor for the Scraping class.
        """

        self.helpers = ScrapingHelpers()
        self.driver = self.helpers.get_driver()
        self.scraping_tr = ScrapingTr()
        self.scraping_class_name = ScrapingClass()
        self.scraping_children = ScrapingChildren()
        self.scraping_bf = ScrapingBf()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def scrape_faculty(self, in_path, out_path):
        """The driver method for scraping profiles.

        The method reads a json file and then process it to add faculty information to
        each department.

        Parameters:
            in_path(str): the path to json file containing school information.
            out_path(str): the path to output the updated json file.

        Returns:
            school(a list of dict): updated school information.
        """

        no_success = 0
        self.logger.addHandler(logging.FileHandler(in_path + '/../scraping_log.log', mode='w'))

        with open(in_path, 'r') as file:
            school = json.load(file)
            self.logger.info('____ Loaded the school with %s departments ____', len(school))

        for department in school:
            department_name = department.get("department")
            url = department.get('faculty_page')
            no_success += 1
            self.logger.info('Scraping faculty page for %s (%s)',
                             department_name, url)
            try:
                res = self.get_department_info(url)
                department.update({'success': True, 'profiles': res})
                self.logger.info('Scraping for %s department successes (%s profiles found)',
                                 department_name, len(res))
            except:
                department.update({'success': False})
                self.logger.debug('Scraping for %s department fails', department_name)

        with open(out_path, 'w') as file:
            json.dump(school, file)

        self.logger.info('Scraped successfully for %s out of %s departments', no_success, len(school))
        return school

    def get_department_info(self, url):
        """The method for scraping profiles using 4 method.

        The method creates soups from the url. It uses 3 methods(tr, children, class name), then
        compares the result to select the one with the best performance. If all 3 methods fail,
        the method proceeds to use bruteforce method.

        Parameters:
            url(str): the link for a particular faculty page.

        Returns:
            profiles(a list of dict): if all 4 methods failed, it returns None.
        """

        soups = self.helpers.get_soups(url, self.driver)
        self.logger.info('Got soups (number of soups = %s)', len(soups))

        res_lst = []
        try:
            res = self.scraping_tr.get_department_info_tr(soups)
            res_lst.append(res)
            self.logger.info('TR successes (length = %s)', len(res))
        except:
            self.logger.debug('TR fails')

        try:
            res = self.scraping_children.get_department_info_children(soups)
            res_lst.append(res)
            self.logger.info('CHILDREN successes (length = %s)', len(res))
        except:
            self.logger.debug('CHILDREN fails')

        try:
            res = self.scraping_class_name.get_department_info_class(soups)
            res_lst.append(res)
            self.logger.info('CLASS NAME successes (length = %s)', len(res))
        except:
            self.logger.debug('CLASS NAME fails')

        if len(res_lst) == 0:
            self.logger.info('All 3 methods failed, now using BF')
            try:
                res = self.scraping_bf.get_department_info_bf(soups)
                self.logger.info('BF successes (length = %s)', len(res))
                return res
            except:
                self.logger.debug('BF fails')
                raise Exception("EVERYTHING FAILED")

        else:
            curr = None
            for res in res_lst:
                if curr is None or len(res) > len(curr):
                    curr = res
            return curr


if __name__ == "__main__":
    s = Scraping()
    lk = input("Website page: ")
    result = s.get_department_info(lk)
    print(f"length = {len(result)}")
    print(result[0])
    print(result[len(result)//2])
    print(result[-1])
