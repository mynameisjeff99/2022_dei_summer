"""The module is for modifying the profiles part of the data collected

This module standardizes faculty members' names, links to their headshots, and their ranks.
"""

import json
import re


class ProfileCleaning:
    """This is the class for cleaning the profiles.

    Attributes:
        in_path(str): the path for the json file containing a school's departments
        with faculty profiles.
        out_path(str): the path for saving the result.
    """

    def __init__(self):
        """The constructor for the ProfileCleaning class.
        """

        self.title_categories = {'assistant professor': ['assistant professor'],
                            'associate professor': ['associate professor'],
                            'professor': ['professor'],
                            'teaching staff': ['instructor', 'lecturer']}

    def clean_profiles(self, in_path, out_path):
        """This is the driver method for cleaning the profiles.

        Parameters:
            in_path(str): the path for the json file containing a school's departments
            with faculty profiles.
            out_path(str): the path for saving the result.

        Returns:
            school(a list of dict): school information with updated profiles
        """

        with open(in_path, 'r') as file:
            school = json.load(file)
        for department in school:
            if department.get('profiles') is not None:
                department_base_url = self.get_department_base_url(department.get('url'))
                for profile in department.get('profiles'):
                    self.process_title(profile)
                    self.process_name(profile)
                    self.to_full_url(profile, department_base_url)
        with open(out_path, 'w') as file:
            json.dump(school, file)
        return school

    @staticmethod
    def process_name(profile):
        """This is the function for standardizing a name's format to [first name]
        [middle name] [last name]. In addition, it also adds each component of the
        name to the profile.

        Parameters:
            profile(dict): a faculty member's profile.
        """

        name = profile.get('name')
        first_name = None
        middle_name = None
        last_name = None
        if name is not None:
            name = re.sub(', Ph.D.', '', name)
            name = name.strip()
            if ',' in name:
                tmp = name.split(', ', 2)
                name = ' '.join([tmp[1], tmp[0]])
            names = name.split(' ')
            first_name = names[0]
            if len(names) == 2:
                middle_name = None
                last_name = names[1]
            elif len(names) == 3:
                middle_name = names[1]
                last_name = names[2]
        profile.update({'name': name, 'first_name': first_name,
                        'middle_name': middle_name, 'last_name': last_name})

    def process_title(self, profile):
        """This is the method for adding the standardized academic rank inferred from
        the title to the profile.

        Parameters:
            profile(dict): a faculty member's profile.
        """

        title = profile.get('title')
        rank = 'other'
        for k, v in self.title_categories.items():
            if re.match(fr"(?i).*({'|'.join(v)}).*", title):
                rank = k
                break
        profile.update({'rank': rank})

    @staticmethod
    def get_department_base_url(url):
        """This is the helper function for getting the base url of a department page
        as the base url for the links to the headshots.

        Parameters:
            url(str): the department page's url.

        Returns:
            base_url(str): the base url for the department page.
        """

        base_url = re.match(r"^(https|http)://[a-zA-Z0-9.-]*", url).group(0)

        return base_url

    @staticmethod
    def to_full_url(profile, department_base_url):
        """This is the function for updating the img's url to the full path.

        Parameters:
            profile(dict): a faculty member's profile.
        """

        img_url = profile.get('img')
        if img_url is not None:
            if img_url[0] == '/' and img_url[:2] != '//':
                img_url = department_base_url + img_url
                profile.update({'img': img_url})
