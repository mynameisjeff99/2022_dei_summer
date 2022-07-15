"""The module is for guessing the gender from a name

The module uses the census data (1880-2021) to get the percentage of the population having
a particular name being male.
"""
import csv
import unidecode


class NameGenderGuesser:
    """This is the class for returning the male pcts for names.

    Attributes:
        first_name(str): the first name of a person
    """

    def __init__(self):
        """The constructor of the NameGenderGuesser class
        """

        self.csv_path = 'census_names_w_pct.csv'
        self.name_dictionary = {}
        with open(self.csv_path, newline='', mode='r') as csv_file:
            reader = csv.reader(csv_file)
            self.name_dictionary.update({row[0]: row[1] for row in reader})

    def gender_guesser(self, first_name):
        """The function uses the first name to predict the percentage of a person
        being male

        Parameters:
            first_name(str): the first name of a person
        """

        return self.name_dictionary.get(unidecode.unidecode(first_name.lower().strip()))


if __name__ == '__main__':
    test = NameGenderGuesser()
    name = input("First name: ")
    print(test.gender_guesser(name))
