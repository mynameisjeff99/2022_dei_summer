from scraping_helpers import ScrapingHelpers
import re
from statistics import mode

class ScrapingBf:
    def __init__(self):
        self.helper = ScrapingHelpers()

    def find_profile_bf(self, tag, count):
        s = ' '.join(list(tag.stripped_strings))
        if re.search(
                r"(?i)(Professor|Lecturer|Student|Director|Fellow|Adjunct|Assistant|Coordinator|Postgraduate|Postdoctoral|Scientist|Visiting|Associate|Staff|PhD|Dean|Senior|Preceptor)",
                s):
            return tag, count
        else:
            count = count + 1
            return self.find_profile_bf(tag.parent, count)


    def get_department_info_bf(self, soups):
        headshots, using_background = self.helper.select_headshots(soups)

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

        all_headshots =[]
        for soup in soups:
            if using_background:
                all_headshots.extend(self.helper.select_headshots_background_image(soup))
            else:
                all_headshots.extend(soup.find_all('img'))

        profs = []
        for t in all_headshots:
            for i in range(count):
                t = t.parent
            profs.append(t)
        items = self.helper.get_info(profs, name_pos, title_pos, using_background)
        return items


if __name__ == "__main__":
    s = ScrapingBf()
    url = input("Website page: ")
    soups = s.helper.get_soups(url)
    res = s.get_department_info_bf(soups)
    print(f"length = {len(res)}")
    print(res[0])
    print(res[len(res)//2])
    print(res[-1])