import json
import re

class ProfileCleaning:
    # url helper functions
    def clean_profiles(self, in_path, out_path):
        with open(in_path) as f:
            school_dict = json.load(f)
        for department in school_dict:
            if department.get('profiles') is not None:
                department_lk = self.get_department_lk(department.get('url'))
                for p in department.get('profiles'):
                    self.process_name(p)
                    self.to_full_url(p, department_lk)
        with open(out_path, 'w') as f:
            json.dump(school_dict, f)
        return school_dict

    def get_department_lk(self, url):
        return re.match("^(https|http)://[a-zA-Z0-9.-]*/", url).group(0)[:-1]

    def to_full_url(self, p, department_lk):
        lk = p.get('img')
        if lk is not None:
            if lk[0] == '/' and lk[:2] != '//':
                lk = department_lk + lk
                p.update({'img': lk})

    # name helper functions
    def process_name(self, p):
        name = p.get('name')
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
        p.update({'name': name, 'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name})