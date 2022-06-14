import sys
import json
import pandas as pd
import gender_guesser.detector as gender
from ethnicolr import census_ln, pred_census_ln, pred_wiki_ln
import numpy as np
import cv2
from urllib.request import Request, urlopen
from deepface import DeepFace

class GenderRaceRecognition:
    def __init__(self):
        self.gender_detector = gender.Detector()

    def detech_gender_race(self, in_path, out_path=None, limit=None):
        with open(in_path) as f:
            school = json.load(f)
        if limit is not None:
            school = school[:limit]
        for department in school:
            self.detech_using_name(department)
            self.detech_using_img(department)
        if out_path is not None:
            with open(out_path, 'w') as f:
                json.dump(school, f)
        return school

    def detech_using_name(self, department):
        if department.get('profiles') is not None:
            for p in department.get('profiles'):
                self.guess_gender_name(p, self.gender_detector)
            profiles_w_race = self.guess_race_name(department.get('profiles'))
            department.update({'profiles': profiles_w_race})
        return department

    def detech_using_img(self, department):
        if department.get('profiles') is not None:
            for p in department.get('profiles'):
                img_url = p.get('img')
                try:
                    img = self.get_img(img_url)
                    gender, race = self.detech_gender_race_img(img)
                    p.update({'gender_img': gender, 'race_img': race})
                except:
                    p.update({'gender_img': None, 'race_img': None})
                    pass
        return department

    # name helper functions
    def guess_gender_name(self, p, gender_detector):
        fname = p.get('first_name')
        gender = None
        if fname is not None:
            gender = gender_detector.get_gender(fname)
        p.update({'gender': gender})

    def guess_race_name(self, lst):
        df = pd.DataFrame(lst)
        odf = pred_census_ln(df, 'last_name')
        odf = odf[["name", "title", "img", "first_name", "middle_name", "last_name", "gender", "race"]]
        res = odf.to_dict(orient='records')
        return res

    # img helper functions
    def get_img(self, url):
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

    def detech_gender_race_img(self, img):
        obj = DeepFace.analyze(img_path=img, actions=['gender', 'race'])
        gender = obj.get('gender')
        race = obj.get('dominant_race')
        return gender, race

if __name__ == "__main__":
    t = GenderRaceRecognition()
    print(t.detech_gender_race(sys.path[0] + '/../data/dartmouth/dartmouth_test_processed.json', out_path=None, limit=2))