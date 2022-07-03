"""The module is for scraping profile images using the table row element.

This module exploits the design of some pages (using table row (tr) tags for profiles).
"""

from scraping_helpers import ScrapingHelpers


class ScrapingTr:
    """The class contains the method to scrape the profiles using tr.

    Attributes:
        soups(a list of bs4.element.BeautifulSoup): the soups generated from a particular
        faculty page.
    """

    def __init__(self):
        """The constructor for the ScrapingTr class.
        """

        self.helper = ScrapingHelpers()

    @staticmethod
    def find_profs_tr(soups):
        """The helper method is for finding all the tr tags in the soups.

        If found no tr tags, it raises an exception.

        Parameters:
            soups(a list of BeautifulSoup): the soups generated from a particular faculty page.

        Returns:
            profile_tags(a list of BeatufulSoup.Tag): all the tr tags found in the soup.
        """

        profile_tags = []
        for soup in soups:
            profile_tags.extend(soup.find_all('tr'))
        if len(profile_tags) == 0:
            raise Exception("No tr")
        return profile_tags

    def get_department_info_tr(self, soups):
        """The method is for scraping profiles from tr tags.

        It finds all the tr tags from the soups. Then it samples 6 tags from different position to
        find the positions of names and titles from the tags. Then it extract the name, title, and
        img from each profile.

        Parameters:
            soups(a list of bs4.element.BeautifulSoup): the soups generated from a faculty page.

        Returns:
            profiles(a list of dict): all the profiles found in the soups.
        """

        _, using_background, _ = self.helper.select_tmp_tags(soups)
        profile_tags = self.find_profs_tr(soups)
        tmp_tags = [profile_tags[len(profile_tags) // 5 * i] for i in range(1, 6)]
        name_pos, title_pos = self.helper.find_pos(tmp_tags)
        profiles = self.helper.get_info(profile_tags, name_pos, title_pos, using_background)
        return profiles


if __name__ == "__main__":
    s = ScrapingTr()
    the_url = input("Website page: ")
    the_soups = s.helper.get_soups(the_url, s.helper.get_driver())
    res = s.get_department_info_tr(the_soups)
    print(f"length = {len(res)}")
    print(res[0])
    print(res[len(res)//2])
    print(res[-1])
