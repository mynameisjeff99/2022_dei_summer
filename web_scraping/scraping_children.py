from scraping_helpers import ScrapingHelpers

class ScrapingChildren:
    def __init__(self):
        self.helper = ScrapingHelpers()

    def find_profile_children(self, tags):
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
                else:
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
        profs = []
        all_headshots = []
        for i in range(len(soups)):
            try:
                headshots, using_background = self.helper.select_headshots(soups[i:])
                all_headshots.extend(headshots)
                profs.extend(self.find_profile_children(headshots))
            except:
                pass

        tags = []
        for h in all_headshots:
            for p in profs:
                if str(h) in str(p):
                    tags.append(p)
                    break
        tags = list(set(tags))
        if len(tags) / len(all_headshots) < 2 / 3:
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