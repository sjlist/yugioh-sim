import json

class Card(object):
    def __init__(self, name, type="", effects=[]):
        self.name = name
        self.type = type
        self.effects = effects


    def load(self):
        jsonOBJ = json.load(open("./cards/{}.json".format(self.name)))
        self.type = jsonOBJ["type"]
        self.effects = jsonOBJ["effects"]
