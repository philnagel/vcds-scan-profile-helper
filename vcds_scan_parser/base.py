import logging
from collections import OrderedDict
try:
    import winreg
except ImportError:
    import _winreg as winreg #py 2.7
import os


from .constants import *

logger = logging.getLogger(__name__)
test_scan = r"C:\Users\Phil\git-repos\vcds-scan-profile-helper\test_data\Log-WVWBF03D668004117-321660km-199870mi.txt"



def find_vcds_path():
    search_paths = [
        r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Ross-Tech\VCDS\Release\VCDS.exe']
    for path in search_paths:
        reg_name = path.split('\\')[0]
        key_path = '\\'.join(path.split('\\')[1:])
        if hasattr(winreg, reg_name):
            reg = getattr(winreg, reg_name)
        else:
            continue
        try:
            key = winreg.OpenKey(reg, key_path, 0, winreg.KEY_READ)
        except FileNotFoundError:
            continue
        value, _ = winreg.QueryValueEx(key, '')
        return os.path.dirname(value)


def get_modules_from_file(txt):
    with open(txt, 'r', errors='ignore') as f:
        content = [l.strip() for l in f]
    modules = []
    for i in content:
        if i.startswith('Address'):
            module = i.split(' ')[1].replace(':', '')
            modules.append(module)
    return modules


def get_scan_files():
    scanpth = os.path.join(find_vcds_path(), 'Scans')
    return [os.path.join(scanpth, file) for file in os.listdir(scanpth)
        if file.endswith('.txt') and not file == 'ReadMe.txt']


class MyAutoScan:
    def __init__(self, txt_file=None):
        self.logfiles = get_scan_files()
        self.txt = os.path.join(find_vcds_path(), 'MyAutoScan.txt')
        parsed = self.parse_my_scan(self.txt)
        self.comments = parsed[COMMENTS]
        self.cars = parsed[CARS]
        self.default_txt_file = os.path.join(find_vcds_path(), 'AutoScan.txt')
        self.default_cars = self.parse_my_scan(self.default_txt_file)[CARS]


    def __verify_cars(self):
        if len(self.cars) + len(self.default_cars) > 250:
            raise ValueError('Too May Chassis Types')
        for car in self.cars.values():
            self.__verify_car(car, new=False)
        return True


    def __verify_car(self, car, new=True):
        errors = []
        if len(car[CAR]) > 3:
            errors.append(
                'Chassis Code "{}" Too Long, must be 3 characters or less!'.format(car[CAR]))
        if len(car[DESCRIPTION]) > 15:
            errors.append(
                'Description "{}" Too Long, must be 15 characters or less!'.format(car[DESCRIPTION]))
        if len(car[MODULES]) > 125:
            errors.append('Too Many Module Addresses, must be less 125 or less!')
        if new:
            if car[CAR] in list(self.cars.keys()) + list(self.default_cars.keys()):
                errors.append('Chassis Code "{}" already exists'.format(car[CAR]))
        if errors:
            raise ValueError('; '.join(errors))
        return True


    def parse_my_scan(self, file):
        with open(file, 'r') as f:
            content = [l.strip() for l in f]
        content_d = {}
        content_d[COMMENTS] = []
        content_d[CARS] = OrderedDict()
        for line in content:
            if line.strip():
                if line.startswith(';'):
                    content_d[COMMENTS].append(line)
                else:
                    d = {}
                    items = line.split(',')
                    d[CAR] = items[0].strip()
                    d[DESCRIPTION] = items[1].strip()
                    d[MODULES] = [i.strip() for i in items[2:]]
                    content_d[CARS][d[CAR]] = d
        return content_d


    def __format_car(self, car):
        format_list = [car[CAR], car[DESCRIPTION], *car[MODULES]]
        return ','.join(format_list)


    def add_car(self, car, description, modules):
        d = {CAR: car,
             DESCRIPTION: description,
             MODULES: modules}
        self.__verify_car(d)
        self.cars[CAR] = d


    def delete_car(self, car):
        if hasattr(car, CAR):
            car = car[CAR]
        try:
            del self.cars[car]
        except KeyError:
            logger.warning('Could not delete chassis code "{}" because it was not found'.format(car))


    def update_file(self):
        nl = '\n'
        self.__verify_cars()
        with open(self.txt, 'w') as f:
            for comment in self.comments:
                f.write('{}{}'.format(comment, nl))
            f.write(nl)
            for car in self.cars.values():
                f.write('{}{}'.format(
                    ','.join([car[CAR], car[DESCRIPTION], *car[MODULES]]), nl))

