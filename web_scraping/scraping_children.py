"""The module is for scraping profiles using children of the tag containing all the profiles.

This module exploits the design of some pages (having a tag containing all the profiles as children).
"""

from scraping_helpers import ScrapingHelpers


class ScrapingChildren:
    """The class contains the method to scrape the profiles using children of the tag.

    Attributes:
        soups(a list of bs4.element.BeautifulSoup): the soups generated from a particular faculty page.
    """

    def __init__(self):
        """The constructor for the ScrapingChildren class.
        """

        self.helper = ScrapingHelpers()

    def find_profile_children(self, tags):
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
        parent = None
        target_tag = None

        while target_tag is None:
            new_tags = []
            for tag in tags:
                tmp_parent = tag.parent
                if tmp_parent in parents:
                    target_tag = tag
                    parent = tmp_parent
                    break
                parents.append(tmp_parent)
                new_tags.append(tmp_parent)
            tags = new_tags

        tag_name = target_tag.name
        children = parent.findChildren(recursive=False)
        items = []
        for c in children:
            if c.name == tag_name:
                items.append(c)
        return items

    def get_department_info_children(self, soups):
        """The method is for finding profiles in the soups using children of the target_tag.

        The soups are passed in then it samples tags containing image/name. Then it uses
        find_profile_children to find all the tags containing profiles. Then it extracts
        information from all the profile tags.

        Parameters:
            soups(a list of bs4.element.BeautifulSoup): the soups extracted from the webpages.

        Returns:
            items(a list of dict): all the profiles found in the soups.
        """

        profs = []
        all_tmp_tags = []
        using_background = False
        for i in range(len(soups)):
            try:
                tmp_tags, using_background, _ = self.helper.select_tmp_tags(soups[i:])
                all_tmp_tags.extend(tmp_tags)
                profs.extend(self.find_profile_children(tmp_tags))
            except:
                pass

        tags = []
        for h in all_tmp_tags:
            for p in profs:
                if str(h) in str(p):
                    tags.append(p)
                    break
        tags = list(set(tags))
        if len(tags) / len(all_tmp_tags) < 2 / 3:
            raise Exception("children failed")

        name_pos, title_pos = self.helper.find_pos(tags)

        items = self.helper.get_info(profs, name_pos, title_pos, using_background)
        return items


if __name__ == "__main__":
    s = ScrapingChildren()
    url = input("Website page: ")
    soups = s.helper.get_soups(url, s.helper.get_driver())
    res = s.get_department_info_children(soups)
    print(f"length = {len(res)}")
    print(res[0])
    print(res[len(res)//2])
    print(res[-1])