"""The module is for adding gender and race information (in percentage)
to the json file with profiles

This module uses pre-trained ML models to get gender and race information
"""

import sys
import json
from urllib.request import Request, urlopen
import numpy as np
import cv2
from census_name_guesser import CensusNameGuesser
import deepface.DeepFace as DeepFace


class GenderRaceRecognition:
    """This is the class for adding gender and race information to the json file.

    Attributes:
        in_path(str): the path for the json file containing a school's departments
        with faculty profiles.
        out_path(str): the path for saving the result.
        the_range(int): the range of departments (for debugging).
    """

    def __init__(self):
        """The constructor for the GenderRaceRecognition class.
        """

        self.census_guesser = CensusNameGuesser()

    def detect_gender_race(self, in_path, out_path=None, department_ind=None):
        """The method for adding gender and race information to the dictionary containing profiles
        of a school.

        The method loads the json file as a list of dictionaries. It then uses detect_using_name
        and detect_using_name to add gender and race information to the profiles. Finally, it
        output the json file to the path passed in.

        Parameters:
            in_path(str): the path for the json file containing a school's departments
            with faculty profiles.
            out_path(str): the path for saving the result.
            department_ind(int): the index of the department (for testing).

        Returns:
            school(lst): the updated list.
        """

        with open(in_path, 'r') as file:
            school = json.load(file)
        # for testing
        if department_ind is not None:
            school = school[department_ind: department_ind+1]
        for department in school:
            profiles = department.get('profiles')
            if profiles is not None:
                for profile in profiles:
                    pct_data = {}
                    pct_from_name = self.detect_using_name(profile)
                    pct_data.update(pct_from_name)
                    pct_from_img = self.detect_using_img(profile)
                    pct_data.update(pct_from_img)
                    profile['pct_data'] = pct_data
                print(f'{department.get("department")}: {len(profiles)} '
                      f'profiles completed')
            else:
                print(f'{department.get("department")}: 0 profiles completed')

        if out_path is not None:
            with open(out_path, 'w') as file:
                json.dump(school, file)

        return school

    def detect_using_name(self, profile):
        """The method for adding gender and race information using the person's name.

        The method uses the functions in CensusNameGuesser.

        Parameters:
            profile(dict): a person's profile

        Returns:
            {race_pct_name(dict): race percentage
            gender_pct_name(dict): gender percentage}
        """
        last_name = profile.get('last_name')
        first_name = profile.get('first_name')
        if '-' in last_name:
            last_name = last_name.split('-')[0]
        race_pct = self.census_guesser.\
            race_guesser(last_name)
        gender_pct = self.census_guesser.\
            gender_guesser(first_name)
        return {'race_pct_name': race_pct,
                'gender_pct_name': gender_pct}


    def detect_using_img(self, profile):
        """The method for adding gender and race information using a person's headshot.

        The method uses DeepFace.

        Parameters:
            profile(dict): a person's profile

        Returns:
            {race_pct_img(dict): race percentage
            gender_pct_img(dict): gender percentage}
        """

        img_url = profile.get('img')
        if img_url is None:
            return {'race_pct_img': None,
                    'gender_pct_img': None}
        try:
            img = self.get_img(img_url)
            obj = DeepFace.analyze(img_path=img,
                                   actions=['gender', 'race'],
                                   enforce_detection=True, prog_bar=False)
        except:
            return {'gender_img': None,
                    'race_img': None}

        race_pct = obj.get('race')
        race_pct = self.format_race_img(race_pct)
        gender_pct = obj.get('gender')
        gender_pct = self.format_gender_img(gender_pct)
        return {'race_pct_img': race_pct,
                'gender_pct_img': gender_pct}

    @staticmethod
    def get_img(url):
        """The helper function for getting images from url links.

        The function uses Request and urlopen to read the image from url. Then
        it uses cv2 to decode image. If the number of channels is only 1,
        the method also converts it to 3 channels.

        Parameters:
            url(str): the link for the img.

        Returns:
            img: the image in the url.
        """

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        arr = np.asarray(bytearray(webpage), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        if len(img.shape) == 2:
            img = cv2.merge((img, img, img))
        # https://stackoverflow.com/questions/36872379/how-to-remove-4th-channel-from-png-images
        elif len(img.shape) > 2 and img.shape[2] == 4:
            # convert the image from RGBA2RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

    @staticmethod
    def format_race_img(dictionary):
        new_dict = {'pctwhite': max(dictionary.get('white'), dictionary.get('middle eastern')),
                    'pctblack': dictionary.get('black'),
                    'pctapi': max(dictionary.get('asian'), dictionary.get('indian')),
                    'pcthispanic': dictionary.get('latino hispanic')}
        return new_dict

    @staticmethod
    def format_gender_img(dictionary):
        new_dict = {'pctmale': dictionary.get('Man'),
                    'pctfemale': dictionary.get('Woman')}
        return new_dict


if __name__ == "__main__":
    test = GenderRaceRecognition()
    print(test.detect_gender_race(
        sys.path[0] + '/../data/columbia/columbia_w_profiles_labeled.json',
        department_ind=0))
