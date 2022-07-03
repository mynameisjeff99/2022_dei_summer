"""The module is for adding gender and race information to the json file with profiles

This module uses pre-trained ML models to get gender and race information
"""

import sys
import json
from urllib.request import Request, urlopen
import pandas as pd
import gender_guesser.detector as g_detector
from ethnicolr import pred_census_ln
import numpy as np
import cv2
from deepface import DeepFace


class GenderRaceRecognition:
    """This is the class for adding gender and race information to the json file.

    Attributes:
        in_path(str): the path for the json file containing a school's departments
        with faculty profiles.
        out_path(str): the path for saving the result.
        the_range(int): the range of departments.
    """

    def __init__(self):
        """The constructor for the GenderRaceRecognition class.
        """

        self.gender_detector = g_detector.Detector()

    def detect_gender_race(self, in_path, out_path=None, the_range=None):
        """The method for adding gender and race information to the dictionary containing profiles
        of a school.

        The method loads the json file as a list of dictionaries. It then uses detect_using_name
        and detect_using_name to add gender and race information to the profiles. Finally, it
        output the json file to the path passed in.

        Parameters:
            in_path(str): the path for the json file containing a school's departments
            with faculty profiles.
            out_path(str): the path for saving the result.
            the_range(int): the range of departments.

        Returns:
            school(lst): the updated list.
        """

        with open(in_path) as file:
            school = json.load(file)
        if the_range is not None:
            school = school[the_range[0]:the_range[1]]
        for department in school:
            self.detect_using_name(department)
            self.detect_using_img(department)
        if out_path is not None:
            with open(out_path, 'w') as file:
                json.dump(school, file)
        return school

    def detect_using_name(self, department):
        """The method for adding gender and race information using the person's name.

        The method uses guess_gender_name and guess_race_name to add the information
        to the profiles.

        Parameters:
            department(a list of dict): the department list.

        Returns:
            department(a list of dict): updated department list.
        """
        if department.get('profiles') is not None:
            for profile in department.get('profiles'):
                self.guess_gender_name(profile, self.gender_detector)
            profiles_w_race = self.guess_race_name(department.get('profiles'))
            department.update({'profiles': profiles_w_race})
        return department

    def detect_using_img(self, department):
        """The method for adding gender and race information using the headshot.

        The method uses guess_gender_img and guess_race_img to add the information
        to the profiles.

        Parameters:
            department(a list of dict): the department list.

        Returns:
            department(a list of dict): updated department list.
        """

        if department.get('profiles') is not None:
            for profile in department.get('profiles'):
                img_url = profile.get('img')
                try:
                    img = self.get_img(img_url)
                    gender, race = self.detect_gender_race_img(img)
                    profile.update({'gender_img': gender, 'race_img': race})
                except:
                    profile.update({'gender_img': None, 'race_img': None})
        return department

    @staticmethod
    def guess_gender_name(profile, gender_detector):
        """The helper function for guess the gender from the name.

        The function uses gender_guesser library to infer the gender from the first name.

        Parameters:
            profile(dict): a person's profile.
        """

        fname = profile.get('first_name')
        gender = None
        if fname is not None:
            gender = gender_detector.get_gender(fname)
        profile.update({'gender': gender})

    @staticmethod
    def guess_race_name(profiles):
        """The helper function for guess the race from the name.

        The function uses the census model from the ethnicolr library to
        infer the race from the last name.

        Parameters:
            profiles(a list of dict): profiles from a particular department.

        Returns:
            new_profiles: updated profiles with races detected using names.
        """

        df = pd.DataFrame(profiles)
        odf = pred_census_ln(df, 'last_name')
        odf = odf[["name", "title", "img", "first_name",
                   "middle_name", "last_name", "gender", "race"]]
        new_profiles = odf.to_dict(orient='records')
        return new_profiles

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
    def detect_gender_race_img(img):
        """The helper function for guess the gender and race from the img.

        The function uses the DeepFace library to infer the gender and race from the img.

        Parameters:
            img: the image after conversion.

        Returns:
            gender(str): the gender inferred.
            race(str): the race inferred.
        """

        obj = DeepFace.analyze(img_path=img, actions=['gender', 'race'])
        gender = obj.get('gender')
        race = obj.get('dominant_race')
        return gender, race


if __name__ == "__main__":
    t = GenderRaceRecognition()
    print(t.detect_gender_race(
        sys.path[0] + '/../data/dartmouth/dartmouth_test_processed.json',
        out_path=None, the_range=[0,2]))
