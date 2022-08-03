"""The module is for guessing a person's gender and race from their name.

The module uses the census data to guess the gender (first name) and race (last name).
"""
import csv
import unidecode


class CensusNameGuesser:
    """This is the class for returning the percentages of genders and races for names.

    Attributes:
        first_name(str): the first name of a person.
        last_name(str): the last name of a person.
    """

    def __init__(self):
        """The constructor of the CensusNameGuesser class.
        """

        self.genders_csv_path = 'census_genders_w_pct.csv'
        self.genders_dictionary = {}
        with open(self.genders_csv_path, newline='', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            self.genders_dictionary.update({item.get('first_name'): float(item.get('pctmale')) for item in reader})

        self.races_csv_path = 'census_races_w_pct.csv'
        self.races_dictionary = {}
        with open(self.races_csv_path, newline='', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            self.races_dictionary.update(
                {item.get('last_name'): {'pctwhite': float(item.get('pctwhite')),
                                         'pctapi': float(item.get('pctapi')),
                                         'pctblack': float(item.get('pctblack')),
                                         'pcthispanic': float(item.get('pcthispanic')),
                                         'pctaian': float(item.get('pctaian'))} for item in reader})

    def gender_guesser(self, first_name):
        """The function uses the first name to predict a person's gender (in pct).

        Parameters:
            first_name(str): the first name of a person.
        """

        pct_male = self.genders_dictionary.get(unidecode.unidecode(first_name.lower().strip()))
        if pct_male is None:
            return None
        pct_female = 100 - pct_male
        genders = {'pctmale': pct_male, 'pctfemale': pct_female}
        return genders

    def race_guesser(self, last_name):
        """The function uses the last name to predict a person's race (in pct).

        Parameters:
            last_name(str): the last name of a person.
        """
        races = self.races_dictionary.get(unidecode.unidecode(last_name.lower().strip()))
        return races


if __name__ == '__main__':
    test = CensusNameGuesser()
    f_name = input('First name: ')
    print(test.gender_guesser(f_name))
    l_name = input('Last name: ')
    print(test.race_guesser(l_name))
