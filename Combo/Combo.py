# Combo is a class with three variales, the nad, deck, and extra deck requirements for the combo to work
# Hand, deck, and extra deck are all dictionaries
import Common.Common as common
import os
import cPickle as pickle
import json
from Common.Errors import *
import sys
import Field.Field as Field
import uuid

class Combo():
    def __init__(self, name="", hand_req={}, hand_or_deck={}, deck_req={}, extra_req={},\
                 grave_req={}, movement=[], subcombos=[], folder="none", hand_or_field={}, field={}):
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

    def is_combo(self, f, run_moves=True):
        # Run through subcombos before trying the current combo
        for combo in self.subcombos:
            if combo:
                # If required combo
                if combo[0] == 'r':
                    # Create and test combo
                    c = Combo()
                    combo_completed = False
                    for sc in combo[1:]:
                        c.load(sc, "{}/subcombos".format(self.folder))
                        if c.is_combo(f):
                            combo_completed = True
                            break
                    if not combo_completed:
                        return False

                # Optional combo handling, make a pkl of the field. Test to see if the combo works,
                # if it doesnt, do nothing to the main combo path.
                # If it does work, pass the field state back to the main combo path
                elif combo[0] == 'o':
                    file_name = uuid.uuid4().hex[:6].upper()
                    pickle.dump(f, open('temp/{}.pkl'.format(file_name), 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
                    c = Combo()
                    for sc in combo[1:]:
                        c.load(sc, "{}/subcombos".format(self.folder))
                        try:
                            c.is_combo(f)
                            break
                        except (CardMissing, ZoneError):
                            f = pickle.load(open("temp/{}.pkl".format(file_name)))
                            pass

        # Do all requirement checks for pile state
        if not self.all_there(self.extra, f.extra):
            return False
        if not self.all_there(self.field, f.m_zone + f.st_zone):
            return False
        if not self.all_there(self.hand_or_field, f.m_zone + f.st_zone + f.hand):
            return False
        if not self.all_there(self.hand_or_deck, f.hand + f.deck):
            return False
        if not self.all_there(self.grave, f.grave):
            return False
        if not self.all_there(self.deck, f.deck):
            return False
        if not self.all_there(self.hand, f.hand):
            return False

        # if there are no movement actions, return true
        # if runMoves is true, run the current combos moves
        # Else return true
        if self.movement == [] or self.movement == [[]]:
            return True, []
        elif run_moves:
            return self.play_combo(f)[0]
        else:
            return True, []

    # Check to see if the card is in the combo
    def in_combo(self, card):
        # Check all requirements, if card is in return True, else return false
        for req in self.combo_reqs:
            if card != 'ANYCARD' and card in req.keys():
                return True
        return False

    # play the combo
    def play_combo(self, f):
        OPTIONAL = False
        # for every action in the movements
        for action in self.movement:

            if len(action) > 1 and action[1] == "optional":
                action = action[0]
                OPTIONAL = True

            # if the action is empty, return true
            if not action:
                return True, action

            # try to do the action, catch any errors, return false if errored
            try:
                f.do_action(action)
            except (CardMissing, ValueError, ZoneError, SummonError):
                if OPTIONAL:
                    pass
                else:
                    return False, action
            except (InvalidOption, PileError):
                raise

            if OPTIONAL:
                OPTIONAL = False

        return True, []

    # Check that all cards in the combo_req are in the combo_ava pile(s)
    def all_there(self, combo_req, combo_ava):
        for element in combo_req.keys():
            if element[:3] == "ANY":
                if element == 'ANYCARD':
                    if common.numItemsDict(combo_req) > len(combo_ava):
                        return False
                else:
                    type = element[3:].lower()
                    count = 0
                    for card in combo_ava:
                        if card.type == type:
                            count += 1
                    if combo_req[element] > count:
                        return False
            else:
                count = 0
                for card in combo_ava:
                    if card.name == element:
                        count += 1
                if combo_req[element] > count:
                    return False

        return True

# SAVE LOAD AND EDITOR FUNCTIONS
    # Print the combo with pretty colors
    def print_combo(self):
        print("{}Name:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.name, common.bcolors.ENDC))
        print("{}Combo Folder:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.folder, common.bcolors.ENDC))
        print("{}Subcombos:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.subcombos, common.bcolors.ENDC))
        print("{}Movement:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.movement, common.bcolors.ENDC))
        print("{}Hand Requirement:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.hand, common.bcolors.ENDC))
        print("{}Hand or Deck Requirment:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.hand_or_deck, common.bcolors.ENDC))
        print("{}Deck Requirement:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.deck, common.bcolors.ENDC))
        print("{}Extra Deck Requirement:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.extra, common.bcolors.ENDC))
        print("{}Grave Requirement:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.grave, common.bcolors.ENDC))
        print("{}Field Requirement:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.field, common.bcolors.ENDC))
        print("{}Hand or Field Requirment:{}".format(common.bcolors.OKBLUE, common.bcolors.ENDC))
        print("{}{}{}".format(common.bcolors.WARNING, self.hand_or_field, common.bcolors.ENDC))

    # Save the combo in a json format
    def save(self):
        jsonOBJ = {
                   'Name': self.name,
                   'Folder': self.folder,
                   'hand': self.hand,
                   'hand_or_deck': self.hand_or_deck,
                   'deck': self.deck,
                   'extra': self.extra,
                   'movement': self.movement,
                   'subcombos': self.subcombos,
                   'grave': self.grave,
                   'field': self.field,
                   'hand_or_field': self.hand_or_field
                   }
        json.dump(jsonOBJ, open("./combos/{}/{}.json".format(self.folder, self.name), 'w'))

    # load the combo from a json file and set up the rest of the combo
    def load(self, name, folder):
        jsonOBJ = json.load(open("./combos/{}/{}.json".format(folder, name)))
        self.name = jsonOBJ['Name']
        self.folder = jsonOBJ['Folder']
        self.hand = jsonOBJ['hand']
        self.hand_or_deck = jsonOBJ['hand_or_deck']
        self.deck = jsonOBJ['deck']
        self.extra = jsonOBJ['extra']
        self.grave = jsonOBJ['grave']
        self.movement = jsonOBJ['movement']
        self.subcombos = jsonOBJ['subcombos']
        self.field = jsonOBJ['field']
        self.hand_or_field = jsonOBJ['hand_or_field']
        self.items = [self.name, self.folder, self.subcombos, self.movement]
        self.combo_reqs = [self.hand, self.hand_or_deck, self.deck, self.extra, self.grave, self.field, self.hand_or_field]

### Editor functions ###
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
