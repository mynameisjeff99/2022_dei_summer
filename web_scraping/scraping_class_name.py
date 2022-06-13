from scraping_helpers import ScrapingHelpers
import re
from statistics import mode

class ScrapingClass:
    def __init__(self):
        self.helper = ScrapingHelpers()

    def find_profile_class(self, tag, levels_allowed=2):
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


    def get_department_info_class(self, soups):
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