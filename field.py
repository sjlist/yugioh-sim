from deck import Deck
import random

def test():
    f = Field()
    f.load_deck('Greg')
    f.shuffle(f.deck)
    f.draw_num(5, f.deck, f.hand)
    

class Field(object):
    def __init__(self):
        self.hand = []
        self.deck = []
        self.grave = []
        self.extra = []
        self.banish = []
        self.mzone = ['empty','empty','empty','empty','empty']
        self.backrow = ['empty','empty','empty','empty','empty']
        self.extra_faceup = []
        self.field_zone = ['empty']
        self.emzone = ['empty','empty']
        normal_summon = 0
        pendulum_summon = 0
        HOPT = []

    def reset(self):
        self.hand = []
        self.deck = []
        self.grave = []
        self.extra = []
        self.banish = []
        self.mzone = ['empty','empty','empty','empty','empty']
        self.backrow = ['empty','empty','empty','empty','empty']
        self.extra_faceup = []
        self.field_zone = ['empty']
        self.emzone = ['empty','empty']

    def load_deck(self, name):
        d = Deck()
        d.load(name)
        for element in d.main_deck.keys():
            self.deck += [element] * d.main_deck[element]
        
        for element in d.extra_deck.keys():
            self.extra += [element] * d.extra_deck[element]
        
    def shuffle(self, target):
        random.shuffle(target)

    def start_duel(self, deck_name):
        f.load_deck(deck_name)
        f.shuffle(f.deck)
        f.draw_num(5, f.deck, f.hand)
        print f.hand

    def draw_num(self, num, src, dest):
        i = 0
        while i < num:
            dest.append(src.pop(0))
            i += 1

    def banish_rand(self, num, target):
        banish = random.sample(target, num)
        for element in banish:
            target.remove(element)

    def add_card(self, card, src, dest):
        src.remove(card)
        dest.append(card)

    
