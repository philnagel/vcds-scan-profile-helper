from collections import OrderedDict
try:
    import winreg
except ImportError:
    import _winreg as winreg #py 2.7
import os


from .constants import *

test_scan = '/Users/philippnagel/Desktop/Log-WVWBF03D668004117-321660km-199870mi.txt'


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


class MyAutoScan:
    def __init__(self, txt_file=find_my_autoscan()):
        self.txt = txt_file
        parsed = self.parse_my_scan()
        self.comments = parsed[COMMENTS]
        self.cars = parsed[CARS]


    def parse_my_scan(self):
        with open(self.txt, 'r') as f:
            content = [l.strip() for l in f]
        content_d = OrderedDict()
        content_d[COMMENTS] = []
        content_d[CARS] = {}
        for line in content:
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
        self.cars[CAR] = d


    def update_file(self):
        nl = '\r\n'
        with open(self.txt, 'w') as f:
            for comment in self.comments:
                f.write('{}{}'.format(comment, nl))
            f.write(nl)
            for car in self.cars.values():
                f.write('{}{}'.format(
                    ','.join([car[CAR], car[DESCRIPTION], *car[MODULES]]), nl))
