"""The module is for scraping profiles using children of the tag containing all the profiles.

This module exploits the design of some pages (having a tag containing all profiles as children).
"""

from scraping_helpers import ScrapingHelpers


class ScrapingChildren:
    """The class contains the method to scrape the profiles using children of the tag.

    Attributes:
        soups(a list of bs4.element.BeautifulSoup): the soups generated from a faculty page.
    """

    def __init__(self):
        """The constructor for the ScrapingChildren class.
        """

        self.helper = ScrapingHelpers()

    @staticmethod
    def find_profile_children(tags):
        """The helper method is for finding tags (as the children of the target tag) containing
        profiles in the soups.

        A list of tags containing images/names are passed in then the method recursively add
        parents into a list until a parent is already in the list. That tag would be designated as
        the target_tag. Then the method returns all the direct children of the target_tag as the
        profiles.

        Parameters:
            tags(a list of bs4.element.Tag): the tags containing images/names

        Returns:
            items(a list of bs4.element.Tag): the profile tags.
        """

        parents = []
        the_parent = None
        target_tag = None
        while target_tag is None:
            new_tags = []
            for tag in tags:
                tmp_parent = tag.parent
                if tmp_parent in parents:
                    target_tag = tag
                    the_parent = tmp_parent
                    break
                parents.append(tmp_parent)
                new_tags.append(tmp_parent)
            tags = new_tags

        tag_name = target_tag.name
        children = the_parent.findChildren(recursive=False)
        profile_tags = []
        for child in children:
            if child.name == tag_name:
                profile_tags.append(child)
        return profile_tags

    def get_department_info_children(self, soups):
        """The method is for finding profiles in the soups using children of the target_tag.

        The soups are passed in then it samples tags containing image/name. Then it uses
        find_profile_children to find all the tags containing profiles. Then it extracts
        information from all the profile tags.

        Parameters:
            soups(a list of bs4.element.BeautifulSoup): the soups extracted from the webpages.

        Returns:
            profiles(a list of dict): all the profiles found in the soups.
        """

        profile_tags = []
        all_tmp_tags = []
        using_background = False
        for i in range(len(soups)):
            try:
                tmp_tags, using_background, _ = self.helper.select_tmp_tags(soups[i:])
                all_tmp_tags.extend(tmp_tags)
                profile_tags.extend(self.find_profile_children(tmp_tags))
            except:
                pass

        tmp_profile_tags = []
        for tmp_tag in all_tmp_tags:
            for profile_tag in profile_tags:
                if str(tmp_tag) in str(profile_tag):
                    tmp_profile_tags.append(profile_tag)
                    break
        tmp_profile_tags = list(set(tmp_profile_tags))
        if len(tmp_profile_tags) / len(all_tmp_tags) < 2 / 3:
            raise Exception("children failed")
        name_pos, title_pos = self.helper.find_pos(tmp_profile_tags)

        profiles = self.helper.get_info(profile_tags, name_pos, title_pos, using_background)
        return profiles


if __name__ == "__main__":
    s = ScrapingChildren()
    the_url = input("Website page: ")
    the_soups = s.helper.get_soups(the_url, s.helper.get_driver())
    res = s.get_department_info_children(the_soups)
    print(f"length = {len(res)}")
    print(res[0])
    print(res[len(res)//2])
    print(res[-1])
