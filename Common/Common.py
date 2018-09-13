import os
import glob

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

def string2List(string):
    list = string[1:-1].replace("'", "").split(', ')
    if list == ['']:
        return []
    else:
        return list

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

def dict2List(dict):
    l = []
    for key in dict.keys():
        l.extend([key] * dict[key])

    return l

def fileExists(folder, file):
    for path, dirs, files in os.walk('./{}'.format(folder)):
        for d in dirs:
            for f in glob.iglob(os.path.join(path, d, '{}'.format(file))):
                return True
    return False

def parentFolder(folder, file):
    for path, dirs, files in os.walk('./{}'.format(folder)):
        for d in dirs:
            for f in glob.iglob(os.path.join(path, d, '{}'.format(file))):
                return True, d
    return False, ""

def numItemsDict(d):
    num = 0
    for key in d.keys():
        num+= d[key]
    return num
