import requests
from bs4 import BeautifulSoup
import re
from statistics import mode
import unidecode

class ScrapingHelpers:
    def get_soup(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        return soup.body

    def select_headshots(self, soup):
        headshots = soup.find_all('img')
        if len(headshots) < 3:
            raise Exception("Not enough imgs")
        elif len(headshots) < 10:
            items = [headshots[len(headshots) // 3], headshots[len(headshots) // 3 * 2], headshots[len(headshots) - 2]]
        elif len(headshots) > 50:
            items = [headshots[len(headshots) // 10 * i] for i in range(1, 10)]
        else:
            items = [headshots[len(headshots) // 7 * i] for i in range(1, 7)]
        return items


    def find_name_pos(self, tag):
        pos = 0
        strs = tag.stripped_strings
        while True:
            try:
                s = next(strs)
                if re.match(
                        "^([a-zA-Z.\-]*[,]* [a-zA-Z.]* [a-zA-Z.\-]*|[a-zA-Z.\-]*[,]* [a-zA-Z.\-]*)[, Ph.D.]*$",
                        unidecode.unidecode(" ".join(s.split()))):
                    if "University" not in s and "College" not in s and "Department" not in s \
                            and "Faculty" not in s and "Research" not in s and "Interest" not in s and "Staff" not in s \
                            and "Profile" not in s and "Student" not in s:
                        return pos
                pos += 1
            except:
                raise Exception("name position not found")

    def find_title_pos(self, tag):
        pos = 0
        strs = tag.stripped_strings
        while True:
            try:
                s = next(strs)
                if re.match(
                        "(?i).*(Professor|Lecturer|Student|Director|Fellow|Adjunct|Assistant|Coordinator|Postgraduate|Postdoctoral|Scientist|Visiting|Associate|Staff|PhD).*",
                        s):
                    return pos
                else:
                    pos += 1
            except:
                raise Exception("title position not found")

    def find_pos(self, tags):
        name_positions = []
        title_positions = []
        for tag in tags:
            try:
                name_pos = self.find_name_pos(tag)
                title_pos = self.find_title_pos(tag)
                name_positions.append(name_pos)
                title_positions.append(title_pos)
            except:
                pass

        if len(name_positions) == 0:
            raise Exception("failed to find positions")
        name_pos = mode(name_positions)
        title_pos = mode(title_positions)
        return name_pos, title_pos

    def is_name(self, s):
        if s is None:
            return None
        elif re.match("^([a-zA-Z.\-]*[,]* [a-zA-Z.]* [a-zA-Z.\-]*|[a-zA-Z.\-]*[,]* [a-zA-Z.\-]*)[, Ph.D.]*$",
                      unidecode.unidecode(" ".join(s.split()))):
            return s
        else:
            return None

    def is_title(self, s):
        if s is None:
            return None
        elif re.match("(?i).*(Professor|Lecturer|Student|Director|Fellow|Adjunct|Assistant|Coordinator|Doctoral|Postgraduate|Postdoctoral|Scientist|Visiting|Associate|Staff|Dean|Senior|Preceptor).*",s):
            return s
        else:
            return None

    def find_by_pos(self, tag, pos):
        it = tag.stripped_strings
        try:
            item = next(x for i, x in enumerate(it) if i == pos)
        except:
            item = None
        return item

    def find_img(self, tag):
        img_tag = tag.find('img')
        if img_tag is not None:
            try:
                return img_tag['src']
            except:
                pass
            try:
                return img_tag['srcset'].split()[0]
            except:
                pass
        return None

    def get_info(self, profs, name_pos, title_pos):
        items = []
        total = 0
        no_fails = 0
        for p in profs:
            name = self.find_by_pos(p, name_pos)
            name = self.is_name(name)
            title = self.find_by_pos(p, title_pos)
            title = self.is_title(title)
            img = self.find_img(p)
            if name is not None and title is not None:
                item = {'name': name, 'title': title, 'img': img}
                items.append(item)
                total += 1
                if name is None or title is None:
                    no_fails += 1
        if no_fails / total > 1 / 3 or total < 5:
            raise Exception("FAILED")
        return items


if __name__ == "__main__":
    h = ScrapingHelpers()
    url = input("Website page: ")
    soup = h.get_soup(url)
    headshots = h.select_headshots(soup)
    for headshot in headshots[:3]:
        print("___________________________")
        print(headshot)