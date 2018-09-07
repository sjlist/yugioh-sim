def string2Dict(string):
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


def string2List(string):
    return string[1:-1].replace("'", "").split(', ')


def dict2List(dict):
    l = []
    for key in dict.keys():
        l.extend([key] * dict[key])

    return l
