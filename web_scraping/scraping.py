from scraping_helpers import ScrapingHelpers
from scraping_tr import ScrapingTr
from scraping_class_name import ScrapingClass
from scraping_children import ScrapingChildren
from scraping_bf import ScrapingBf

class Scraping:
    def __init__(self):
        self.helpers = ScrapingHelpers()
        self.driver = self.helpers.get_driver()
        self.scraping_tr = ScrapingTr()
        self.scraping_class_name = ScrapingClass()
        self.scraping_children = ScrapingChildren()
        self.scraping_bf = ScrapingBf()


    def get_department_info(self, URL):
        soups = self.helpers.get_soups(URL, self.driver)
        res_lst = []
        try:
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
    url = input("Website page: ")
    res = s.get_department_info(url)
    print(f"length = {len(res)}")
    print(res[0])
    print(res[len(res)//2])
    print(res[-1])