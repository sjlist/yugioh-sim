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

        for type in self.extra_deck:
            for element in self.extra_deck[type]:
                extra_size += self.extra_deck[type][element]

        for element in self.side_deck:
            side_size += self.side_deck[element]

        self.main_deck_size = main_size
        self.extra_deck_size = extra_size
        self.side_deck_size = side_size

    def init_main(self):
        main_list = []
        for type in self.main_deck:
            for element in self.main_deck[type]:
                try:
                    c = Card.Card(element)
                    c.load()
                    main_list += self.main_deck[type][element] * [c]
                except IOError:
                    main_list += self.main_deck[type][element] * [Card.Card(element, type)]

        return main_list

    def init_extra(self):
        extra_list = []
        for type in self.extra_deck:
            for element in self.extra_deck[type]:
                try:
                    c = Card.Card(element)
                    c.load()
                    extra_list += self.extra_deck[type][element] * [c]
                except IOError:
                    extra_list += self.extra_deck[type][element] * [Card.Card(element, type)]

        return extra_list

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
        print "Deck Name: " + self.deck_name
        print "Combo Folder : " + self.combo_folder
        print "\nMain Deck: " + str(self.main_deck_size) + " cards"
        for type in self.main_deck:
            for element in self.main_deck[type]:
                print element + ": " + str(self.main_deck[type][element])
        print "\nExtra Deck: " + str(self.extra_deck_size) + " cards"
        for type in self.extra_deck:
            for element in self.extra_deck[type]:
                print element + ": " + str(self.extra_deck[type][element])
        print "\nSide Deck: " + str(self.side_deck_size) + " cards"
        for element in self.side_deck:
            print element + ": " + str(self.side_deck[element])

    def add_card(self, pile, name, number):
        if name in pile.keys():
            pile[name] += number
        else:
            pile[name] = number

    def remove_card(self, pile, name, number):
        pile[name] -= number
        if pile[name] == 0:
            pile.pop(name)
