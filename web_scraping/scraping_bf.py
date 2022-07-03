"""The module is for scraping profiles by using brute force

This module is the last resort after all 3 other methods fail.
"""

from statistics import mode
from scraping_helpers import ScrapingHelpers


class ScrapingBf:
    """The class is contains the method to scrape the profiles using brute force.

    Attributes:
        soups(a list of BeautifulSoup): the soups generated from a particular faculty page.
    """

    def __init__(self):
        """The constructor for the ScrapingBf class.
        """

        self.helper = ScrapingHelpers()

    def find_profile_bf(self, tag, count):
        """The helper method is for finding the level the tag that only contains image/name
        needs to go up to find the parent tag that contains the profile.

        A tag containing images/names is passed in. The method uses helper.is_title to find
        whether the tag's stripped_strings contains the keywords of titles. If not, the method
        is then recursively applied to the tag's parent. If a keyword is found, it returns the
        current tag and the count.

        Parameters:
            tag(bs4.element.Tag): a tag containing images/names.
            count(int): current number of count

        Returns:
            tag(bs4.element.Tag): the profile tag.
            count(int): the number of level the tag containing only image/name needs to go up to get
            the profile tag.
        """

        string = ' '.join(list(tag.stripped_strings))
        if self.helper.is_title(string):
            return tag, count
        count = count + 1
        return self.find_profile_bf(tag.parent, count)

    def get_department_info_bf(self, soups):
        """The method is for finding profiles in the soups using the common tag name.

        The soups are passed in then it samples tags containing image/name. Then for each tag
        sampled, it uses find_profile_bf to find the level to go up to. Then it find all the tags
        containing images/names and then go up to the mode of the level to get profile tags. It
        then extract the information from the profile tags

        Parameters:
            soups(a list of bs4.element.BeautifulSoup): the soups extracted from the webpages.

        Returns:
            items(a list of dict): all the profiles found in the soups.
        """

        tmp_tags, using_background, using_headshots = self.helper.select_tmp_tags(soups)

        counts = []
        tmp_profile_tags = []
        for tmp_tag in tmp_tags:
            try:
                tmp_profile_tag, tmp_count = self.find_profile_bf(tmp_tag, 0)
                counts.append(tmp_count)
                tmp_profile_tags.append(tmp_profile_tag)
            except:
                pass

        if len(counts) == 0:
            raise Exception("bf failed")
        if len(set(counts)) == len(counts):
            raise Exception("counts are all different")
        count = mode(counts)

        tmp_profile_tags = [t for (t, c) in zip(tmp_profile_tags, counts) if c == count]
        name_pos, title_pos = self.helper.find_pos(tmp_profile_tags)

        all_tags = []
        if using_headshots:
            for soup in soups:
                if using_background:
                    all_tags.extend(self.helper.get_headshots_background_image(soup))
                else:
                    all_tags.extend(soup.find_all('img'))
        else:
            for i in range(len(soups)):
                all_tags.extend(self.helper.find_name_tags(soups[i:]))
        profile_tags = []
        for tag in all_tags:
            for i in range(count):
                tag = tag.parent
            profile_tags.append(tag)
        items = self.helper.get_info(profile_tags, name_pos, title_pos, using_background)
        return items


if __name__ == "__main__":
    s = ScrapingBf()
    the_url = input("Website page: ")
    the_soups = s.helper.get_soups(the_url, s.helper.get_driver())
    res = s.get_department_info_bf(the_soups)
    print(f"length = {len(res)}")
    print(res[0])
    print(res[len(res)//2])
    print(res[-1])
