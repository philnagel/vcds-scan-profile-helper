from vcds_scan_parser.base import *

from consolemenu import *
from consolemenu.items import *

autoscan = MyAutoScan()

menu = ConsoleMenu("Autoscan Helper", "Tool for importing cars into MyAutoScan in VCDS")

function_item = FunctionItem("List Current Cars", print(autoscan.cars.keys()))

menu.append_item(function_item)

menu.show()