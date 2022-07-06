"""The module is for helper methods for scraping

The helper methods are used across different scraping methods
"""

import time
import re
from statistics import mode
import requests
import spacy
from bs4 import BeautifulSoup
import unidecode
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class ScrapingHelpers:
    """The class contains the helper methods for the web scraping methods.
    """

    def __init__(self):
        """The constructor for the ScrapingHelpers class.
        """

        self.nlp = spacy.load("en_core_web_sm")
        self.user_agent = ''.join(["user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) ",
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
                           "83.0.4103.97 Safari/537.36"])
        self.titles = ["Professor", "Lecturer", "Student", "Director", "Fellow", "Adjunct",
                       "Assistant", "Coordinator", "Postgraduate", "Postdoctoral", "Scientist",
                       "Visiting", "Associate", "Staff", "PhD", "Dean", "Preceptor", "Senior"]
        self.name_pattern = "[A-Z][a-zA-Z.-]*"
        self.not_name_keywords = ["University", "College", "Department", "Professor", "Faculty",
                                  "Research", "Interest", "Staff", "Profile", "Student"]

    def get_driver(self):
        """The method creates a Chrome driver for Selenium.

        Returns:
            driver: Chrome driver for Selenium.
        """

        #https://stackoverflow.com/questions/47508518/
        # google-chrome-closes-immediately-after-being-launched-with-selenium
        opts = Options()
        opts.add_argument(self.user_agent)
        opts.add_argument("start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        return driver

    @staticmethod
    def get_soups(url, driver=None, page_limit=5):
        """The methods extract soups from the faculty page(s).

        if driver is not passed in, the method directly extract a soup from the page using BS4,
        if a driver is specified, the method uses Selenium to generate the page source then
        generates the soup from the source code. If a next button is found on the page, then
        the driver get the next page and then generate another soup until no next button is
        found or reaches the page limit.

        Parameters:
            url(str): the link for a particular faculty page.
            driver: Chrome driver for Selenium.
            page_limit(int): Max # of pages.

        Returns:
            soups(a list of bs4.element.BeautifulSoup): Soups extracted from the faculty page(s).

        To-do: find other ways to find the next page button
        """

        soups = []
        if driver is None:
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html5lib')
            soups.append(soup.body)

        # https://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python
        else:
            driver.get(url)
            time.sleep(5)
            html = driver.page_source
            soups.append(BeautifulSoup(html, 'html5lib').body)
            to_click = driver.find_elements(
                By.XPATH, "".join(["//a[contains(translate",
                                   "(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', ",
                                   "'abcdefghijklmnopqrstuvwxyz'), 'next')]"]))

            for item in to_click:
                if len(item.get_attribute("innerText")) > 10:
                    to_click.remove(item)
            while len(to_click) != 0 and page_limit != 0:
                page_limit -= 1
                try:
                    webdriver.ActionChains(driver).move_to_element(to_click[0]).\
                        click(to_click[0]).perform()
                    time.sleep(3)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html5lib').body
                    if soup == soups[-1]:
                        break
                    soups.append(soup)
                    to_click = driver.find_elements(
                        By.XPATH,"".join(["//a[contains(translate",
                                          "(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', ",
                                          "'abcdefghijklmnopqrstuvwxyz'), 'next')]"]))

                    for item in to_click:
                        if len(item.get_attribute("innerText")) > 10:
                            to_click.remove(item)
                except:
                    break
        return soups

    @staticmethod
    def get_headshots_background_image(soup):
        """The method find the tags that embed the headshots as background-image.

        It finds all 'div' tags that have 'background-image' in style

        Parameters:
            soup(bs4.element.BeautifulSoup): a soup extracted from the faculty page.

        Returns:
            img_tags(a list of bs4.element.Tag): the tags that contain 'background-image' in style.
        """

        img_tags = soup.find_all('div', style=lambda value: value and 'background-image' in value)
        return img_tags

    @staticmethod
    def get_url_background_img(tag):
        """The method find url for if headshots are embedded as background-images.

        It uses Regex to find the url of headshots from the tag's style.

        Parameters:
            tag(bs4.element.Tag): tag containing a profile.

        Returns:
            url(str): the url for the headshot.
        """

        img_tag = tag.find('div', style=lambda value: value and 'background-image' in value)
        url = re.findall(r'\((.*?)\)', img_tag['style'])[0]
        return url

    def find_name_tags(self, soups):
        """The method finds all hyperlink tags from the soups (when too few headshots are found).

        The method find all hyperlink tags that contain a string that is determined to be a name.

        Parameters:
            soups(a list of bs4.element.BeautifulSoup): Soups extracted from the faculty page(s).

        Returns:
            items(a list of bs4.element.Tag): tags that contain names.
        """

        elements = soups[0].find_all('a')
        items = []
        for element in elements:
            strings = list(element.stripped_strings)
            for string in strings:
                if self.is_name(string, True):
                    items.append(element)
        return items

    def select_tmp_tags(self, soups):
        """The method find temporary tags used for determine the positions of name/title in a tag.

        The method first find tags that contain images. If the # tags is less than 5, then it
        finds tags that contain names. If none of the methods find more than 5 tags, it raises an
        exception. Then according to the number of tags found, it returns a portion of tags as
        temporary tags.

        Parameters:
            soups(a list of bs4.element.BeautifulSoup): Soups extracted from the faculty page(s).

        Returns:
            tmp_tags(a list of bs4.element.Tag): temporary tags.
            using_background(bool): whether the headshots are embedded as background-images
            using_headshots(bool): whether the headshots are found (as 'img' or 'background-image')
        """
        soup = soups[0]
        tags = soup.find_all('img')
        using_background = False
        using_headshots = True
        if len(tags) < 5:
            headshots_background = self.get_headshots_background_image(soup)
            if len(headshots_background) > 5:
                tags = headshots_background
                using_background = True
            else:
                # raise Exception('not enough img')
                tags = self.find_name_tags(soups)
                using_headshots = False
                if len(tags) <= 5:
                    raise Exception("failed to enough tags")

        if len(tags) < 10:
            tmp_tags = [tags[len(tags) // 3], tags[len(tags) // 3 * 2], tags[len(tags) - 2]]
        elif len(tags) > 50:
            tmp_tags = [tags[len(tags) // 10 * i] for i in range(1, 10)]
        else:
            tmp_tags = [tags[len(tags) // 7 * i] for i in range(1, 7)]
        return tmp_tags, using_background, using_headshots

    def is_name(self, string, strict=False):
        """The method determines whether a string is a person's name.

        The method first process the name (i.e. get rid of and title and convert the text
        into standard [first name] [last name] format (in case if there is a ',') and translate
        it into unicode. Then if the strict param is True, it uses the nlp model, otherwise
        it uses Regex, to determine whether the line is a person's name.

        Parameters:
            string(str): a line of text.
            strict(bool): whether the result will be determined strictly.

        Returns:
            bool: whether the line of text is a person's name.
        """

        if string is None:
            return False
        string = re.sub(r', Ph.D.', '', string)
        string = re.sub(r', MD', '', string)
        string = string.strip()
        string = unidecode.unidecode(" ".join(string.split()))
        if ',' in string:
            tmp = string.split(', ', 2)
            string = ' '.join([tmp[1], tmp[0]])
        string = unidecode.unidecode(" ".join(string.split()))

        if strict:
            doc = self.nlp(string)
            for ent in doc.ents:
                if ent.label_ == "PERSON" and ent.end_char - ent.start_char + 7 > len(string):
                    return True

        elif re.match(fr"^({self.name_pattern} {self.name_pattern} {self.name_pattern}|"
                      fr"{self.name_pattern} {self.name_pattern})$", string) \
                and not re.search(fr"{('|'.join(self.not_name_keywords))}", string):
            return True

        return False

    def is_title(self, string):
        """The method determines whether a string is a title

        The method uses Regex to match the string with a list of keywords associated
        with titles. If none of the keywords are in the string, return False.

        Parameters:
            s(str): a line of text.

        Returns:
            bool: whether the string is a title.
        """

        if string is None:
            return False
        string = unidecode.unidecode(" ".join(string.split()))
        return bool(re.match(fr"(?i).*({'|'.join(self.titles)}).*", string))

    def find_name_pos(self, tag):
        """The method find the position of the name in a profile.

        The method first gets a list of strings from the profile tag. Then go through each
        string until it find a string that is a name by using is_name method. It raises
        an exception is no name is found.

        Parameters:
            tag(bs4.element.Tag): a profile tag.

        Returns:
            pos(int): the position of the string containing the name
        """

        pos = 0
        strs = tag.stripped_strings
        while True:
            try:
                string = next(strs)
                if self.is_name(string, True):
                    return pos
                pos += 1
            except:
                raise Exception("name position not found")

    def find_title_pos(self, tag):
        """The method find the position of the title in a profile.

        The method first gets a list of strings from the profile tag. Then go through each
        title until it find a string that is a title by using is_title method. It raises
        an exception is no title is found.

        Parameters:
            tag(bs4.element.Tag): a profile tag.

        Returns:
            pos(int): the position of the title containing the name
        """
        pos = 0
        strs = tag.stripped_strings
        while True:
            try:
                string = next(strs)
                if self.is_title(string):
                    return pos
                pos += 1
            except:
                raise Exception("title position not found")

    def find_pos(self, tags):
        """The method find the positions of name/title in tags.

        The method first find name/title positions for all the tags. Then return the most
        positions that are frequent among the tags. It raises an exception if no positions are
        found.

        Parameters:
            tags(a list of bs4.element.Tag): a list of profile tags.

        Returns:
            name_pos(int): the mode of name positions
            title_pos(int): the mode of title positions
        """

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

        if len(name_positions) == 0 or len(title_positions) == 0:
            raise Exception("failed to find positions")
        name_pos = mode(name_positions)
        title_pos = mode(title_positions)
        return name_pos, title_pos

    @staticmethod
    def find_by_pos(tag, pos):
        """The method finds a string by position.

        The method go through the stripped strings in a tag to find string in the specified pos.

        Parameters:
            tag(bs4.element.Tag): a profile tag.
            pos(int): the position for name of title.

        Returns:
            item(str): the string found.
        """

        strings = tag.stripped_strings
        try:
            item = next(x for i, x in enumerate(strings) if i == pos)
        except:
            item = None
        return item

    def find_img(self, tag, using_background):
        """The method finds the image in a tag.

        The method finds the image (headshots) based on whether they are embedded
        as 'background-image'.

        Parameters:
            tag(bs4.element.Tag): a profile tag.
            using_background(bool): whether the images are embeeded as 'background-image'.

        Returns:
            img(url): the image found in the tag; returns None if nothing found.
        """

        if using_background:
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
        """The method finds information about profiles.

        For each profile, it finds the name and title using positions provided, and it also
        finds the image (headshot). It then returns a list of dict. If too many failed, it
        raises an exception.

        Parameters:
            profs(a list of bs4.element.Tag): profile tags.
            name_pos(int): the position of name in each profile tag's strings.
            title_pos(int): the position of title in each profile tag's strings.
            using_background(bool): whether the images are embeeded as 'background-image'.

        Returns:
            items(a list of dict): the information found for all the profiles.
        """

        items = []
        total = 0
        no_fails = 0
        for prof in profs:
            name = self.find_by_pos(prof, name_pos)
            if not self.is_name(name):
                name = None
            title = self.find_by_pos(prof, title_pos)
            if not self.is_title(title):
                title = None
            img = self.find_img(prof, using_background)
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
    the_url = input("Website page: ")
    the_driver = h.get_driver()
    the_soups = h.get_soups(the_url, the_driver)
    print(len(the_soups))
    the_tags, _, _ = h.select_tmp_tags(the_soups)
    for the_tag in the_tags[:3]:
        print("___________________________")
        print(the_tag)
