# Combo is a class with three variales, the nad, deck, and extra deck requirements for the combo to work
# Hand, deck, and extra deck are all dictionaries
import Common.Common as common
import os


class Combo():
    def __init__(self, name="", hand_req={}, hand_or_deck={}, deck_req={}, extra_req={}, grave_req={}, subcombos=[], folder=""):
        self.name = name
        self.hand = hand_req
        self.hand_or_deck = hand_or_deck
        self.deck = deck_req
        self.extra = extra_req
        self.grave = grave_req
        self.subcombos = subcombos
        self.folder = folder
        self.file_path = ""

    def isCombo(self, f):
        for combo in self.subcombos:
            if combo != '':
                c = self.__init__()
                c.load(combo, self.folder)
                c.isCombo(f)

        return self.allThere(self.hand, f.hand) and self.allThere(self.deck, f.deck) and \
               self.allThere(self.extra, f.extra) and self.allThere(self.hand_or_deck, f.hand + f.deck) and \
               self.allThere(self.grave, f.grave)

    def allThere(self, combo_req, combo_ava):
        for element in combo_req.keys():
            if combo_req[element] != combo_ava.count(element):
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
            f.write('\nSubcombos\n')
            f.write(str(self.subcombos))
            f.write('\nFolder\n')
            f.write(str(self.folder))
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
        self.hand = common.string2Dict(deck_raw[2])
        self.hand_or_deck = common.string2Dict(deck_raw[4])
        self.deck = common.string2Dict(deck_raw[6])
        self.extra = common.string2Dict(deck_raw[8])
        self.grave = common.string2Dict(deck_raw[10])
        self.subcombos = common.string2List(deck_raw[12])
        self.folder = deck_raw[14]

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

