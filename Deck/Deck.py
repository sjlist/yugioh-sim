import random
import time
import os
from Common.Common import string2DictInt

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

        for element in self.main_deck:
            main_size += self.main_deck[element]

        for element in self.extra_deck:
            extra_size += self.extra_deck[element]

        for element in self.side_deck:
            side_size += self.side_deck[element]

        self.main_deck_size = main_size
        self.extra_deck_size = extra_size
        self.side_deck_size = side_size

#### SAVE LOAD AND EDITOR FUNCTIONS ####
    def delete_deck(self):
        self.file_path = "./decks/" + str(self.deck_name) + ".txt"
        os.remove(self.file_path)

    def save(self):
        print self.file_path
        self.file_path = "./decks/" + str(self.deck_name) + ".txt"
        print "Saving " + self.deck_name
        print "In: " + self.file_path
        with open(self.file_path, 'w') as f:
            f.write('\n')
            f.write(self.deck_name)
            f.write('\nMain Deck\n')
            f.write(str(self.main_deck))
            f.write('\nExtra Deck\n')
            f.write(str(self.extra_deck))
            f.write('\nSide Deck\n')
            f.write(str(self.side_deck))
            f.write('\nCombo Folder\n')
            f.write(str(self.combo_folder))
            f.write('\n')

    def load(self, name):
        self.deck_name = name
        self.file_path = "./decks/" + str(self.deck_name) + ".txt"
        file_list = []
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

        self.deck_name = deck_raw[0]
        self.main_deck = string2DictInt(deck_raw[2])
        self.extra_deck = string2DictInt(deck_raw[4])
        self.side_deck = string2DictInt(deck_raw[6])
        self.combo_folder = deck_raw[8]

    def print_deck(self):
        self.count_size()
        print "Deck Name: " + self.deck_name
        print "Combo Folder : " + self.combo_folder
        print "\nMain Deck: " + str(self.main_deck_size) + " cards"
        for element in self.main_deck:
            print element + ": " + str(self.main_deck[element])
        print "\nExtra Deck: " + str(self.extra_deck_size) + " cards"
        for element in self.extra_deck:
            print element + ": " + str(self.extra_deck[element])
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
