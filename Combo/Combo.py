# Combo is a class with three variales, the nad, deck, and extra deck requirements for the combo to work
# Hand, deck, and extra deck are all dictionaries
import Common.Common as common
import os

class Combo():
    def __init__(self, name="", hand_req={}, hand_or_deck={}, deck_req={}, extra_req={}, grave_req={}, movement = {}, subcombos=[], folder="none", hand_or_field = {}, field = {}):
        self.name = name
        self.folder = folder
        self.hand = hand_req
        self.hand_or_deck = hand_or_deck
        self.deck = deck_req
        self.extra = extra_req
        self.grave = grave_req
        self.movement = movement
        self.subcombos = subcombos
        self.field = field
        self.hand_or_field = hand_or_field
        self.items = [self.name, self.folder, self.subcombos, self.movement]
        self.combo_reqs = [self.hand, self.hand_or_deck, self.deck, self.extra, self.grave, self.field, self.hand_or_field]
        self.file_path = ""

    def isCombo(self, f):
        for combo in self.subcombos:
            if combo != '':
                c = Combo()
                c.load(combo, "{}/subcombos".format(self.folder))
                if not c.isCombo(f):
                    return False

        if not self.allThere(self.hand, f.hand):
            return False
        if not self.allThere(self.extra, f.extra):
            return False
        if not self.allThere(self.deck, f.deck):
            return False
        if not self.allThere(self.field, f.m_zone + f.st_zone):
            return False
        if not self.allThere(self.hand_or_field, f.m_zone + f.st_zone + f.hand):
            return False
        if not self.allThere(self.hand_or_deck, f.hand + f.deck):
            return False
        if not self.allThere(self.grave, f.grave):
            return False

        if self.movement == []:
            return True
        else:
            return self.playCombo(f)

    def playCombo(self, f):
        for action in self.movement:
            if not f.move_card(action):
                return False
        return True

    def allThere(self, combo_req, combo_ava):
        for element in combo_req.keys():
            if combo_req[element] > combo_ava.count(element):
                return False

        return True

# SAVE LOAD AND EDITOR FUNCTIONS
    def print_combo(self):
        print("Combo:\n{}".format(self.name))
        print("Combo Folder:\n{}".format(self.folder))
        print("Subcombos:\n{}".format(self.subcombos))
        print("Movement:\n{}".format(self.movement))
        print("Hand Requirement:\n{}".format(self.hand))
        print("Hand or Deck Requirment:\n{}".format(self.hand_or_deck))
        print("Deck Requirement:\n{}".format(self.deck))
        print("Extra Deck Requirement:\n{}".format(self.extra))
        print("Grave Requirement:\n{}".format(self.grave))
        print("Field Requirement:\n{}".format(self.field))
        print("Hand or Field Requirment:\n{}".format(self.hand_or_field))

    def save(self):
        print self.file_path
        self.file_path = "./combos/{}/{}.txt".format(self.folder, self.name)
        if not os.path.exists("./combos/{}".format(self.folder)):
            os.makedirs("./combos/{}".format(self.folder))
        print "Saving " + self.name
        print "In: " + self.file_path
        with open(self.file_path, 'w') as f:
            f.write('\n')
            f.write(self.name)
            f.write('\nFolder\n')
            f.write(str(self.folder))
            f.write('\nSubcombos\n')
            f.write(str(self.subcombos))
            f.write('\nMovement\n')
            f.write(str(self.movement))
            f.write('\nHand Requirement\n')
            f.write(str(self.hand))
            f.write('\nHand or Main Deck Requirement\n')
            f.write(str(self.hand_or_deck))
            f.write('\nMain Deck Requirement\n')
            f.write(str(self.deck))
            f.write('\nExtra Deck Requirement\n')
            f.write(str(self.extra))
            f.write('\nGrave Requirement\n')
            f.write(str(self.grave))
            f.write('\nField Requirement\n')
            f.write(str(self.field))
            f.write('\nHand or Field Deck Requirement\n')
            f.write(str(self.hand_or_field))
            f.write('\n\n')


    def load(self, name, folder):
        self.file_path = "./combos/{}/{}.txt".format(folder, name)
        with open(self.file_path, 'r') as f:
            file_data = f.read()

        loc = 0
        lines = [0]
        while loc != -1:
            loc = file_data.find("\n", loc + 1)
            lines.append(loc)

        lines.remove(-1)

        i = 0
        deck_raw = []
        while i < len(lines) - 1:
            deck_raw.append(file_data[lines[i]+1:lines[i+1]])
            i += 1

        self.items[0] = deck_raw[0]
        self.items[1] = deck_raw[2]
        self.items[2] = common.string2List(deck_raw[4])
        self.items[3] = common.string2TupleList(deck_raw[6])

        i = 0
        while (i+len(self.items))*2 < len(deck_raw):
            self.combo_reqs[i] = common.string2DictInt(deck_raw[(i+len(self.items))*2])
            i += 1

        self.save_items()

    def save_items(self):
        self.name = self.items[0]
        self.folder = self.items[1]
        self.subcombos = self.items[2]
        self.movement = self.items[3]

        self.hand = self.combo_reqs[0]
        self.hand_or_deck = self.combo_reqs[1]
        self.deck = self.combo_reqs[2]
        self.extra = self.combo_reqs[3]
        self.grave = self.combo_reqs[4]
        self.field = self.combo_reqs[5]
        self.hand_or_field = self.combo_reqs[6]


    def add_card(self, pile, name, number):
        if name in pile.keys():
            pile[name] += number
        else:
            pile[name] = number

    def remove_card(self, pile, name, number):
        pile[name] -= number
        if pile[name] == 0:
            pile.pop(name)

    def delete_combo(self):
        self.file_path = "./combos/{}/{}.txt".format(self.folder, self.name)
        os.remove(self.file_path)
