import json
from Common.Common import get_json_attr


class Card(object):
    def __init__(self, name, type="", subtype="", effects=[]):
        self.name = name
        self.type = type
        self.subtype = subtype
        self.effects = effects

    def load(self):
        jsonOBJ = json.load(open("./cards/{}.json".format(self.name)))
        self.type = get_json_attr(jsonOBJ, "type")
        self.subtype = get_json_attr(jsonOBJ, "subtype")
        self.effects = get_json_attr(jsonOBJ, "effects")
