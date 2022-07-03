"""The module is for scrape profiles

This module combines 4 scraping methods to scrape profiles from faculty pages.
"""

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
        res_lst = []
        try:
            res_lst.append(self.scraping_tr.get_department_info_tr(soups))
            res_lst.append(self.scraping_tr.get_department_info_tr(soups))
        except:
            pass

        try:
            res_lst.append(self.scraping_children.get_department_info_children(soups))
        except:
            pass

        try:
            res_lst.append(self.scraping_class_name.get_department_info_class(soups))
        except:
            pass

        if len(res_lst) == 0:
            try:
                return self.scraping_bf.get_department_info_bf(soups)
            except:
                raise Exception("FAILED")
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
