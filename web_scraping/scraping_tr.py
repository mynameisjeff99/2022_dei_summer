from scraping_helpers import ScrapingHelpers

class ScrapingTr:
    def __init__(self):
        self.helper = ScrapingHelpers()

    def find_profs_tr(self, soups):
        profs = []
        for soup in soups:
            profs.extend(soup.find_all('tr'))

        if len(profs) == 0:
            raise Exception("No tr")
        return profs


    def get_department_info_tr(self, soups):
        profs = self.find_profs_tr(soups)
        _, using_background = self.helper.select_headshots(soups)

        tags = [profs[len(profs) // 5 * i] for i in range(1, 6)]

        name_pos, title_pos = self.helper.find_pos(tags)

        items = self.helper.get_info(profs, name_pos, title_pos, using_background)
        return items

if __name__ == "__main__":
    s = ScrapingTr()
    url = input("Website page: ")
    soups = s.helper.get_soups(url, s.helper.get_driver())
    res = s.get_department_info_tr(soups)
    print(f"length = {len(res)}")
    print(res[0])
    print(res[len(res)//2])
    print(res[-1])