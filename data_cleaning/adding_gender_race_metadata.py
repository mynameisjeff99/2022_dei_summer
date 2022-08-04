"""The module is for summarizing the gender race data of a school.

This module counts the number of each category for each departments
"""


class AddGenderRaceMetadata:
    """This is the class for summarizing the gender/race data.

    Attributes:
        school(a list of dict): the school information (after detecting gender and race)
    """

    def __init__(self):
        """The constructor for the AddGenderRaceData class.
        """

        self.ranks = ['professor', 'associate professor', 'assistant professor',
                      'teaching staff', 'other']

    def add_gender_race_metadata(self, school):
        """This is the method for summarizing the gender and race data.

        Parameters:
            school(a list of dict): the school information (after detecting gender and race)
        """

        for department in school:
            profiles = department.get('profiles')
            if profiles is not None:
                gender_race_data = {}
                categories = []
                categories.append('all')
                categories.extend(self.ranks)
                for i in categories:
                    no_genders = {'female': 0, 'male': 0, 'unknown': 0}
                    no_races = {'white': 0, 'black': 0, 'api': 0,
                                     'hispanic': 0, 'unknown': 0}
                    tmp = {'no_genders': no_genders, 'no_races': no_races}
                    gender_race_data.update({i: tmp})

                for p in profiles:
                    rank = p.get('rank')
                    gender = p.get('gender_detected')
                    gender_race_data.get(rank).get('no_genders').\
                        update({gender: gender_race_data.get(rank).
                               get('no_genders').get(gender) + 1})
                    gender_race_data.get('all').get('no_genders'). \
                        update({gender: gender_race_data.get('all').
                               get('no_genders').get(gender) + 1})

                    race = p.get('race_detected')
                    gender_race_data.get(rank).get('no_races').\
                        update({race: gender_race_data.get(rank).
                               get('no_races').get(race) + 1})
                    gender_race_data.get('all').get('no_races').\
                        update({race: gender_race_data.get('all').
                               get('no_races').get(race) + 1})

                department.update({'gender_race_data': gender_race_data})

            else:
                department.update({'gender_race_data': None})
