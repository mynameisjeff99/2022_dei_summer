import requests
from bs4 import BeautifulSoup
import re
from statistics import mode
import unidecode
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class ScrapingHelpers:

    def get_driver(self):
        #https://stackoverflow.com/questions/47508518/google-chrome-closes-immediately-after-being-launched-with-selenium
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
        opts.add_argument("start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        return driver

    def get_soups(self, url, driver=None, page_limit=5):
        soups = []
        if driver is None:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html5lib')
            soups.append(soup.body)

        # https://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python
        else:
            driver.get(url)
            time.sleep(5)
            html = driver.page_source
            soups.append(BeautifulSoup(html, 'html5lib').body)
            to_click = driver.find_elements(By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                                                  "'abcdefghijklmnopqrstuvwxyz'), 'next')]")
            for c in to_click:
                if len(c.get_attribute("innerText")) > 10:
                    to_click.remove(c)
            while len(to_click) != 0 and page_limit != 0:
                page_limit -= 1
                try:
                    #to_click[0].click()
                    webdriver.ActionChains(driver).move_to_element(to_click[0]).click(to_click[0]).perform()
                    #driver.execute_script("arguments[0].click();", to_click[0])
                    time.sleep(3)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html5lib').body
                    if soup == soups[-1]:
                        break
                    soups.append(soup)
                    to_click = driver.find_elements(By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                                                                  "'abcdefghijklmnopqrstuvwxyz'), 'next')]")
                    for c in to_click:
                        if len(c.get_attribute("innerText")) > 10:
                            to_click.remove(c)
                except:
                    break
        return soups

    def select_headshots(self, soups):
        soup = soups[0]
        headshots = soup.find_all('img')
        using_backgrounds = False
        if len(headshots) < 5:
            headshots_background = self.select_headshots_background_image(soup)
            if len(headshots_background) > 5:
                headshots = headshots_background
                using_backgrounds = True
            else:
                raise Exception('not enough img')
        if len(headshots) < 10:
            items = [headshots[len(headshots) // 3], headshots[len(headshots) // 3 * 2], headshots[len(headshots) - 2]]
        elif len(headshots) > 50:
            items = [headshots[len(headshots) // 10 * i] for i in range(1, 10)]
        else:
            items = [headshots[len(headshots) // 7 * i] for i in range(1, 7)]
        return items, using_backgrounds


    def select_headshots_background_image(self, soup):
        img_tags = soup.find_all('div', style=lambda value: value and 'background-image' in value)
        return img_tags


    def get_url_background_img(self, tag):
        img_tag = tag.find('div', style=lambda value: value and 'background-image' in value)
        url = re.findall('\((.*?)\)', img_tag['style'])[0]
        return url

    def find_name_pos(self, tag):
        pos = 0
        strs = tag.stripped_strings
        while True:
            try:
                s = next(strs)
                if re.match(
                        "^([A-Z][a-zA-Z.-]*[,]* [A-Z][a-zA-Z.-]* [A-Z][a-zA-Z.-]*|[A-Z][a-zA-Z.-]*[,]* [A-Z][a-zA-Z.-]*)(, Ph.D.)*$",
                        unidecode.unidecode(" ".join(s.split()))):
                    if "University" not in s and "College" not in s and "Department" and "Professor" not in s \
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
        elif re.match("^([A-Z][a-zA-Z.-]*[,]* [A-Z][a-zA-Z.-]* [A-Z][a-zA-Z.-]*|[A-Z][a-zA-Z.-]*[,]* [A-Z][a-zA-Z.-]*)(, Ph.D.)*$",
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

    def find_img(self, tag, using_headshots):
        if using_headshots:
            try:
                return self.get_url_background_img(tag)
            except:
                pass

        else:
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

    def get_info(self, profs, name_pos, title_pos, using_background):
        items = []
        total = 0
        no_fails = 0
        for p in profs:
            name = self.find_by_pos(p, name_pos)
            name = self.is_name(name)
            title = self.find_by_pos(p, title_pos)
            title = self.is_title(title)
            img = self.find_img(p, using_background)
            if name is not None and title is not None:
                item = {'name': name, 'title': title, 'img': img}
                items.append(item)
                total += 1
                if name is None or title is None:
                    no_fails += 1
        if no_fails / total > 1 / 3 or total < 5:
            raise Exception("failed, too many errors")
        return items


if __name__ == "__main__":
    h = ScrapingHelpers()
    url = input("Website page: ")
    driver = h.get_driver()
    soups = h.get_soups(url, driver)
    print(len(soups))
    headshots = h.select_headshots(soups)
    for headshot in headshots[:3]:
        print("___________________________")
        print(headshot)