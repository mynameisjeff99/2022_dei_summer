"""The module is for summarizing the gender race data of a school.

This module counts the number of each category for each departments
"""


class AddGenderRaceData:
    """This is the class for summarizing the gender/race data.

    Attributes:
        school(a list of dict): the school information (after detecting gender and race)
    """

    def __init__(self):
        """The constructor for the AddGenderRaceData class.
        """

        self.ranks = ['professor', 'associate professor', 'assistant professor',
                      'teaching staff', 'other']

    def add_gender_race_data(self, school):
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
                    no_genders_name = {'female': 0, 'male': 0, 'unknown': 0}
                    no_races_name = {'white': 0, 'black': 0, 'api': 0,
                                     'hispanic': 0, 'unknown': 0}
                    no_genders_img = {'female': 0, 'male': 0, 'unknown': 0}
                    no_races_img = {'white': 0, 'black': 0, 'api': 0,
                                    'hispanic': 0, 'unknown': 0}
                    tmp = {'no_genders_name': no_genders_name, 'no_races_name': no_races_name,
                                                            'no_genders_img': no_genders_img,
                                                            'no_races_img': no_races_img}
                    gender_race_data.update({i: tmp})

                for p in profiles:
                    rank = p.get('rank')
                    # gender name
                    gender_name = p.get('gender')
                    gender_race_data.get(rank).get('no_genders_name').\
                        update({gender_name: gender_race_data.get(rank).
                               get('no_genders_name').get(gender_name) + 1})
                    gender_race_data.get('all').get('no_genders_name'). \
                        update({gender_name: gender_race_data.get('all').
                               get('no_genders_name').get(gender_name) + 1})

                    # race name
                    race_name = p.get('race')
                    gender_race_data.get(rank).get('no_races_name').\
                        update({race_name: gender_race_data.get(rank).
                               get('no_races_name').get(race_name) + 1})
                    gender_race_data.get('all').get('no_races_name').\
                        update({race_name: gender_race_data.get('all').
                               get('no_races_name').get(race_name) + 1})

                    # gender img
                    gender_img = p.get('gender_img')
                    gender_race_data.get(rank).get('no_genders_img'). \
                        update({gender_img: gender_race_data.get(rank).
                               get('no_genders_img').get(gender_img) + 1})
                    gender_race_data.get('all').get('no_genders_img'). \
                        update({gender_img: gender_race_data.get('all').
                               get('no_genders_img').get(gender_img) + 1})

                    # race img
                    race_img = p.get('race_img')
                    gender_race_data.get(rank).get('no_races_img'). \
                        update({race_img: gender_race_data.get(rank).
                               get('no_races_img').get(race_img) + 1})
                    gender_race_data.get('all').get('no_races_img'). \
                        update({race_img: gender_race_data.get('all').
                               get('no_races_img').get(race_img) + 1})

                department.update({'gender_race_data': gender_race_data})

            else:
                department.update({'gender_race_data': None})
