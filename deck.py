import random
import time
import os

def test():
    print 1
    
class Deck(object):
    def __init__(self):
        self.main_deck = {}
        self.side_deck = {}
        self.extra_deck = {}
        self.main_deck_size = 40
        self.side_deck_size = 15
        self.extra_deck_size = 15
        self.deck_name = ""
        self.file_path = ""

    def delete_deck(self):
        self.file_path = "c:\Users\Sam\Deck_files\\" + str(self.deck_name) + ".txt"
        os.remove(self.file_path)         

    def save(self):
        self.file_path = "c:\Users\Sam\Deck_files\\" + str(self.deck_name) + ".txt"
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
            f.write('\n')
    
    def load(self, name):
        self.deck_name = name
        self.file_path = "c:\Users\Sam\Deck_files\\" + str(self.deck_name) + ".txt"
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
        self.main_deck = string2Dict(deck_raw[2])
        self.extra_deck = string2Dict(deck_raw[4])
        self.side_deck = string2Dict(deck_raw[6])

    def print_deck(self):
        self.count_size()
        print "Deck Name: " + self.deck_name
        print "\nMain Deck: " + str(self.main_deck_size) + " cards"
        for element in self.main_deck:
            print element + ": " + str(self.main_deck[element])
        print "\nExtra Deck: " + str(self.extra_deck_size) + " cards"
        for element in self.extra_deck:
            print element + ": " + str(self.extra_deck[element])
        print "\nSide Deck: " + str(self.side_deck_size) + " cards"
        for element in self.side_deck:
            print element + ": " + str(self.side_deck[element])

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

    def add_card(self, pile, name, number):
        if name in pile.keys():
            pile[name] += number
        else:
            pile[name] = number

    def remove_card(self, pile, name, number):
        pile[name] -= number
        if pile[name] == 0:
            pile.pop(name)

    def make_main_deck_dict(self):
        res_f = 3
        res_c = 3
        res_s = 3
        res_search = 3
        level5s = 9
        rtn_d_lords = 3
        desires = 3
        upstart = 0

        cardDict = {'Pot of Desires' : desires,
                    'Flare Resonator' : res_f,
                    'Creation Resonator' : res_c,
                    'Synkron Resonator' : res_s,
                    'Resonator Call' : res_search,
                    'Level 5' : level5s,
                    'Return of the Dragon Lords' : rtn_d_lords,
                    'Upstart' : upstart}
        
        deck_size = 40
        deck = []

        for element in cardDict:
            i = 0
            while i < cardDict[element]:
                deck.append(element)
                i +=  1

        while len(deck) < deck_size:
            deck.append('Card')

        self.main_deck = cardDict
        self.main_deck_size = deck_size

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

def create_deck():
    d = Deck()
    d.deck_name = raw_input("What is the name of the deck?\n")
    d.save()
    edit_deck(d)
    
def edit_deck(d):
    states =  ['main', 'side', 'extra', 'none', 'done']
    actions = ['add', 'remove', 'print', 'none', 'done']
    action = 'none'
    repeat = 0
    parts = [d.main_deck, d.side_deck, d.extra_deck, d.deck_name]

    d.print_deck()
    state = raw_input("What part of the deck do you want to work on?\n")
    
    while state != 'done':
        while state not in states:
            print 'Error ' + state + ' is not a valid part of the deck'
            print 'main, side, and extra are the valid parts of the deck'
            state = raw_input("What part of the deck do you want to work on?\n")   

        if state in states[0:2]:
            part = parts[states.index(state)]

        while action != 'done':
            
            if state == 'done':
                action = 'done'

            if action == 'none':
                action = raw_input("Would you like to add or remove cards from the " + state + " deck?\n")

            if action == 'print':
                d.main_deck = parts[0]
                d.side_deck = parts[1]
                d.extra_deck = parts[2]
                d.print_deck()
                action = 'none'

            if action == 'name':
                print 'Name is: ' + d.deck_name
                d.delete_deck()
                d.deck_name = raw_input("What would you like to change it to?\n")
                d.save()
                action = 'none'
                
            while action == 'add':
                if not repeat:
                    card = raw_input("What card would you like to add?\n")

                if card in actions:
                    action = card
                    break

                if card in part:
                    print 'There are currently ' + str(part[card]) + ' copies of ' + card + ' already in the deck'
                                
                num = int(raw_input("How many copies of " + card + " do you want to add?\n"))

                if num > 3:
                    print 'You can only have 3 copies of a card in your deck'
                    repeat = 1
                elif card in part.keys():
                    if (part[card] + num) > 3:
                        print 'You can only have 3 copies of a card in your deck'
                        repeat = 1
                    else:
                        repeat = 0
                        d.add_card(part, card, num)
                        print 'Added ' + card
                else:
                    repeat = 0
                    d.add_card(part, card, num)
                    print 'Added ' + card

            while action == 'remove':
                if not repeat:
                    card = raw_input("What card would you like to remove?\n")

                if card in actions:
                    action = card
                    break
                
                if card in part.keys():
                    print 'There are ' + str(part[card]) + ' copies of ' + card

                    num = int(raw_input("How many copies of " + card + " do you want to remove?\n"))
                    if num > part[card]:
                        print 'Error, you are trying to remove more copies than exist'
                        repeat = 1
                    else:
                        repeat = 0
                        d.remove_card(part, card, num)
                else:
                    print card + ' is not in the ' + state + ' deck'
                
            if action not in actions:
                print 'Error: invalid action entered: ' + action
                print 'Valid actions are:'
                action = 'none'
                for element in actions:
                    print element

        action = 'none'
        state = raw_input("What part of the deck do you want to work on?\n")

    d.main_deck = parts[0]
    d.side_deck = parts[1]
    d.extra_deck = parts[2]
    d.save()

