import random
import time

class Deck(object):
    def __init__(self):
	self.main_deck = {}
	self.side_deck = {}
	self.extra_deck = {}
	self.file_name = ""

    def save(self):
	with open(self.file_name, 'r') as f:
	    f.write(str(self.main_deck))
	    f.write(str(self.extra_deck))
	    f.write(str(self.side_deck))
    
    def load(self):
	output = raw_input("What is the name of the deck?n>")
	self.file_name = str(output) + '.txt'	
	with open(self.file_name, 'r') as f:
            s = f.read()
            self.main_deck = ast.literal_eval(s)
	
def make_deck():
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

    return deck

    
def draw_num(num, src, dest):
    i = 0
    while i < num:
        draw = random.sample(src,1)
        src.remove(draw[0])
        dest.append(draw[0])
        i += 1

def banish_rand(num, target):
    banish = random.sample(target, num)
    for element in banish:
        target.remove(element)

def add_card(card, src, dest):
    src.remove(card)
    dest.append(card)
