from scraping_helpers import ScrapingHelpers
import re
from statistics import mode

class Scraping:
    def __init__(self):
        self.helper = ScrapingHelpers()

    def find_profs_tr(self, soup):
        profs = soup.find_all('tr')

        if len(profs) == 0:
            raise Exception("No tr")
        return profs


    def get_department_info_tr(self, soup):
        profs = self.find_profs_tr(soup)

        tags = [profs[len(profs) // 5 * i] for i in range(1, 6)]

        name_pos, title_pos = self.helper.find_pos(tags)

        items = self.helper.get_info(profs, name_pos, title_pos)
        return items


    ## Profile class name
    def find_profile_class(self, tag, levels_allowed = 2):
        if levels_allowed == 0:
            raise Exception("Class name not found")
        s = ' '.join(list(tag.stripped_strings))
        if re.search(
                r"(?i)(Professor|Lecturer|Student|Director|Fellow|Adjunct|Assistant|Coordinator|Postgraduate|Postdoctoral|Scientist|Visiting|Associate|Staff|PhD|Dean|Senior|Preceptor)",
                s):
            tag_s = str(tag)
            m = re.findall(r'class="(.+?)"', tag_s)
            # allow going up 2 more levels if 'class=' is not found
            if len(m) == 0:
                return self.find_profile_class(tag.parent, levels_allowed - 1)
            else:
                return tag, m[0]
        else:
            return self.find_profile_class(tag.parent, levels_allowed)


    def get_department_info_class(self, soup):
        headshots = self.helper.select_headshots(soup)

        profile_classes = []
        tags = []
        for headshot in headshots:
            try:
                tag, profile_c = self.find_profile_class(headshot, 2)
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

        profs = soup.find_all(attrs={'class': profile_class})
        items = self.helper.get_info(profs, name_pos, title_pos)
        return items


    ## Children

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


    def get_department_info_children(self, soup):
        headshots = self.helper.select_headshots(soup)

        profs = self.find_profile_children(headshots)

        tags = []
        for h in headshots:
            for p in profs:
                if str(h) in str(p):
                    tags.append(p)
                    break
        tags = list(set(tags))
        if len(tags) / len(headshots) < 2 / 3:
            raise Exception("children failed")

        name_pos, title_pos = self.helper.find_pos(tags)

        items = self.helper.get_info(profs, name_pos, title_pos)
        return items


    ## Brute Forcing

    def find_profile_bf(self, tag, count):
        s = ' '.join(list(tag.stripped_strings))
        if re.search(
                r"(?i)(Professor|Lecturer|Student|Director|Fellow|Adjunct|Assistant|Coordinator|Postgraduate|Postdoctoral|Scientist|Visiting|Associate|Staff|PhD|Dean|Senior|Preceptor)",
                s):
            return tag, count
        else:
            count = count + 1
            return self.find_profile_bf(tag.parent, count)


    def get_department_info_bf(self, soup):
        headshots = self.helper.select_headshots(soup)

        counts = []
        tags = []
        for headshot in headshots:
            try:
                tag, count = self.find_profile_bf(headshot, 0)
                counts.append(count)
                tags.append(tag)
            except:
                pass

        if len(counts) == 0:
            raise Exception("bf failed")
        elif len(set(counts)) == len(counts):
            raise Exception("counts are all different")
        else:
            count = mode(counts)

        tags = [t for (t, c) in zip(tags, counts) if c == count]
        name_pos, title_pos = self.helper.find_pos(tags)

        all_headshots = soup.find_all('img')
        profs = []
        for t in all_headshots:
            for i in range(count):
                t = t.parent
            profs.append(t)
        items = self.helper.get_info(profs, name_pos, title_pos)
        return items


    def get_department_info(self, URL):
        soup = self.helper.get_soup(URL)
        res_lst = []
        try:
            res_lst.append(self.get_department_info_tr(soup))
        except:
            pass

        try:
            res_lst.append(self.get_department_info_children(soup))
        except:
            pass

        try:
            res_lst.append(self.get_department_info_class(soup))
        except:
            pass

        if len(res_lst) == 0:
            try:
                return (self.get_department_info_bf(soup))
            except:
                raise Exception("FAILED")
        else:
            curr = None
            for res in res_lst:
                if curr is None or len(res[1]) > len(curr[1]):
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