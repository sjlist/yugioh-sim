import os
import json
import Card

class Deck(object):
    def __init__(self, deck_name = ""):
        self.main_deck = {}
        self.side_deck = {}
        self.extra_deck = {}
        self.main_deck_size = 40
        self.side_deck_size = 15
        self.extra_deck_size = 15
        self.deck_name = deck_name
        self.file_path = "./decks/"
        self.combo_folder = self.deck_name

    def count_size(self):
        main_size = 0
        extra_size = 0
        side_size = 0

        for type in self.main_deck:
            for element in self.main_deck[type]:
                main_size += self.main_deck[type][element]

        for type in self.extra_deck["monster"]:
            for element in self.extra_deck["monster"][type]:
                extra_size += self.extra_deck["monster"][type][element]

        for element in self.side_deck:
            side_size += self.side_deck[element]

        self.main_deck_size = main_size
        self.extra_deck_size = extra_size
        self.side_deck_size = side_size

    def init_pile(self, pile):
        pile_list = []
        for card_type in pile:
            for element in pile[card_type]:
                try:
                    len(pile[card_type][element])
                    for card_name in pile[card_type][element]:
                        card = self.load_card(card_name, card_type, element)
                        pile_list += [card] * pile[card_type][element][card_name]
                except TypeError:
                    card = self.load_card(element, card_type)
                    pile_list += [card] * pile[card_type][element]

        return pile_list

    def load_card(self, card_name, card_type="", card_subtype=""):
        try:
            c = Card.Card(card_name)
            c.load()
            return c
        except IOError:
            c = Card.Card(card_name, card_type, card_subtype)
            return c

# SAVE LOAD AND EDITOR FUNCTIONS
    def delete_deck(self):
        self.file_path = "./decks/" + str(self.deck_name) + ".json"
        os.remove(self.file_path)

    def save(self):
        jsonOBJ = {
                    'Name': self.deck_name,
                    'main_deck': self.main_deck,
                    'side_deck': self.side_deck,
                    'extra_deck': self.extra_deck,
                    'combo_folder': self.combo_folder
                  }
        json.dump(jsonOBJ, open("./decks/{}.json".format(self.deck_name), 'w'))

    def load(self, name):
        jsonOBJ = json.load(open("./decks/{}.json".format(name)))
        self.main_deck = jsonOBJ['main_deck']
        self.side_deck = jsonOBJ['side_deck']
        self.extra_deck = jsonOBJ['extra_deck']
        self.deck_name = jsonOBJ['Name']
        self.combo_folder = jsonOBJ['combo_folder']

# Editor Functions
    def print_deck(self):
        self.count_size()
        print("Deck Name: {}".format(self.deck_name))
        print("Combo Folder : {}".format(self.combo_folder))
        print("\nMain Deck: {} cards".format(str(self.main_deck_size)))
        for card_type in self.main_deck:
            for element in self.main_deck[card_type]:
                print("{}: {}".format(element, str(self.main_deck[card_type][element])))
        print("\nExtra Deck: {} cards".format(str(self.extra_deck_size)))
        for card_type in self.extra_deck["monster"]:
            for element in self.extra_deck["monster"][card_type]:
                print("{}: {}".format(element, str(self.extra_deck["monster"][card_type][element])))
        print("\nSide Deck: {} cards".format(str(self.side_deck_size)))
        for element in self.side_deck:
            print("{}: {}".format(element, str(self.side_deck[element])))

    def add_card(self, pile, name, number):
        if name in pile.keys():
            pile[name] += number
        else:
            pile[name] = number

    def remove_card(self, pile, name, number):
        pile[name] -= number
        if pile[name] == 0:
            pile.pop(name)
