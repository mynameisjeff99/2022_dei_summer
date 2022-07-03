"""The module is for scraping profiles using common class names among profile tags.

This module exploits the design of some pages (having the common class names for profile tags).
"""

from scraping_helpers import ScrapingHelpers
import re
from statistics import mode


class ScrapingClass:
    """The class is contains the method to scrape the profiles using the common class names.

    Attributes:
        soups(a list of BeautifulSoup): the soups generated from a particular faculty page.
    """

    def __init__(self):
        """The constructor for the ScrapingClass class.
        """

        self.helper = ScrapingHelpers()

    def find_profile_class(self, tag, levels_allowed=2):
        """The helper method is for finding the class name for the parent of the tag that contains
        the profile.

        A tag containing images/names is passed in. The method uses helper.is_title to find
        whether the tag's stripped_strings contains the keywords of titles. If not, the method
        is then recursively applied to the tag's parent. If a keyword is found, the method then
        uses Regex to find the class name and return the current tag and the class name if found.

        Parameters:
            tag(bs4.element.Tag): a tag containing images/names.

        Returns:
            tag(bs4.element.Tag): the profile tag.
            m[0](str): class name.
        """

        if levels_allowed == 0:
            raise Exception("Class name not found")
        s = ' '.join(list(tag.stripped_strings))
        if self.helper.is_title(s):
            tag_s = str(tag)
            m = re.findall(r'class="(.+?)"', tag_s)
            # allow going up 2 more levels if 'class=' is not found
            if len(m) == 0:
                return self.find_profile_class(tag.parent, levels_allowed - 1)
            else:
                return tag, m[0]
        else:
            return self.find_profile_class(tag.parent, levels_allowed)

    def get_department_info_class(self, soups):
        """The method is for finding profiles in the soups using the common tag name.

        The soups are passed in then it samples tags containing image/name. Then for each tag
        sampled, it uses find_profile_class to find the class names. Then it find all the tags
        having the the mode of class names found previously as profile tags Then it extracts
        information from all the profile tags.

        Parameters:
            soups(a list of bs4.element.BeautifulSoup): the soups extracted from the webpages.

        Returns:
            items(a list of dict): all the profiles found in the soups.
        """

        tmp_tags, using_background, _ = self.helper.select_tmp_tags(soups)

        profile_classes = []
        tags = []
        for tmp_tag in tmp_tags:
            try:
                tag, profile_c = self.find_profile_class(tmp_tag, 2)
                profile_classes.append(profile_c)
                tags.append(tag)
            except:
                pass

        if len(profile_classes) == 0:
            raise Exception("class name not found")
        elif len(set(profile_classes)) == len(profile_classes):
            raise Exception("class names for profiles are different")
        else:
            profile_class = mode(profile_classes)

        tags = [t for (t, c) in zip(tags, profile_classes) if c == profile_class]

        name_pos, title_pos = self.helper.find_pos(tags)

        profs = []
        for soup in soups:
            profs.extend(soup.find_all(attrs={'class': profile_class}))

        items = self.helper.get_info(profs, name_pos, title_pos, using_background)
        return items


if __name__ == "__main__":
    s = ScrapingClass()
    url = input("Website page: ")
    soup = s.helper.get_soups(url, s.helper.get_driver())
    res = s.get_department_info_class(soup)
    print(f"length = {len(res)}")
    print(res[0])
    print(res[len(res)//2])
    print(res[-1])