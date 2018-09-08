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

        return True

    def allThere(self, combo_req, combo_ava):
        for element in combo_req.keys():
            if combo_req[element] > combo_ava.count(element):
                return False

        return True

# SAVE LOAD AND EDITOR FUNCTIONS
    def print_combo(self):
        print("Combo: {}".format(self.name))
        print("Hand Requirement: \n{}".format(self.hand))
        print("Hand or Deck Requirment: \n{}".format(self.hand_or_deck))
        print("Deck Requirement: \n{}".format(self.deck))
        print("Extra Deck Requirement: \n{}".format(self.extra))
        print("Grave Requirement: \n{}".format(self.grave))
        print("Combo Movement: \n{}".format(self.movement))
        print("Subcombos: \n{}".format(self.subcombos))
        print("Combo Folder: \n{}".format(self.folder))

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
            f.write('\nMovement\n')
            f.write(str(self.movement))
            f.write('\nSubcombos\n')
            f.write(str(self.subcombos))
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

        self.name = deck_raw[0]
        self.folder = deck_raw[2]
        self.hand = common.string2Dict(deck_raw[4])
        self.hand_or_deck = common.string2Dict(deck_raw[6])
        self.deck = common.string2Dict(deck_raw[8])
        self.extra = common.string2Dict(deck_raw[10])
        self.grave = common.string2Dict(deck_raw[12])
        self.movement = common.string2Dict(deck_raw[14])
        self.subcombos = common.string2List(deck_raw[16])


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
