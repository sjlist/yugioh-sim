import os
import glob
import Deck.Card as Card


# Color class for pretty printing
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Convert a string into a dictionary with a int as a value
def string2DictInt(string):
    d = dict()
    value_end = 0
    while True:
        name_start = string.find("'", value_end) + 1
        name_end = string.find("'", name_start)
        name = string[name_start:name_end]

        value_start = name_end + 3
        value_end = string.find(",", value_start)

        if value_end == -1:
            if name != '{':
                value = int(string[value_start:len(string)-1])
                d[name] = value
                return d
            else:
                return d

        value = int(string[value_start:value_end])

        d[name] = value

    return d


# Convert a dictionary of card names to a list of Cards of a type
def dict2card(pile_dict, type):
    pile_list = dict2List(pile_dict)
    return list2card(pile_list, type)


# Convert a list of card names to a list of Cards of a type
def list2card(pile_list, type):
    card_list = []
    for element in pile_list:
        if element[:3] == "ANY":
            card_list.append(Card.Card(element, element[3:].lower()))
        else:
            card_list.append(Card.Card(element, type))

    return card_list


# Convert a string into a dictionary with a string as a value
def string2DictString(string):
    d = dict()
    value_end = 0
    while True:
        name_start = string.find("'", value_end) + 1
        name_end = string.find("'", name_start)
        name = string[name_start:name_end]

        value_start = name_end + 3
        value_end = string.find(",", value_start)

        if value_end == -1:
            if name != '{':
                value = string[value_start+1:len(string)-2]
                d[name] = value
                return d
            else:
                return d

        value = string[value_start+1:value_end-1]

        d[name] = value

    return d


# convert a string into a list
def string2List(string):
    _list = string[1:-1].replace("'", "").split(', ')
    if _list == ['']:
        return []
    else:
        return _list


# Convert a string into a tuple list
def string2TupleList(string):
    if string == '[]':
        return []
    list = []
    elements = string[2:-2].split("], [")
    for element in elements:
        i = []
        items = element.split(", ")
        for item in items:
            i.append(item.split("'")[1])
        list.append(i)
    return list


# Convert a dictionary into a list, assumes the values of the dictionary are ints
def dict2List(_dict):
    l = []
    for key in _dict.keys():
        l.extend([key] * _dict[key])

    return l


# Check if a file exists
def fileExists(folder, _file):
    for path, dirs, files in os.walk('./{}'.format(folder)):
        for d in dirs:
            if os.path.isfile("./{}/{}".format(d, _file)):
                return True
    return False


# Find the first parent folder of a file
def parentFolder(folder, _file):
    for path, dirs, files in os.walk('./{}'.format(folder)):
        for d in dirs:
            if os.path.isfile("./{}/{}".format(d, _file)):
                return True, d
    return False, ""


# Count the number of items in the dictionary, assuming the values in the dict are ints
def numItemsDict(d):
    num = 0
    for key in d.keys():
        num += d[key]
    return num
