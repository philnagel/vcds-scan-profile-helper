from collections import OrderedDict, defaultdict

from .constants import *


def find_my_autoscan():
    return '/Users/philippnagel/Desktop/MyAutoScan.txt'


def parse_my_scan(txt):
    with open(txt, 'r') as f:
        content = [l for l in f]
    content_d = OrderedDict()
    content_d[COMMENTS] = defaultdict(list)
    for i in content:
        if i.startswith(';'):
            content_d[COMMENTS].append(i)
        else:
            
        


class MyAutoScan:
    def __init__(self, txt_file=find_my_autoscan()):
        self.cars = parse_my_scan(txt_file)
        
        
    def 
    