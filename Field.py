import random
import Common.Common as Common

class Field:
    def __init__(self, deck):
        self.deck = Common.dict2List(deck.main_deck)
        self.hand = []
        self.grave = []
        self.extra = Common.dict2List(deck.extra_deck)
        self.banished = []
        self.m_zone = ["", "", "", "", "", "", ""]
        self.st_zone = ["", "", "", "", ""]
        self.draw_num(5)

    def draw_num(self, num):
        i = 0
        while i < num:
            draw = random.sample(self.deck,1)[0]
            self.move_card(draw, self.deck, self.hand)
            i += 1

    def banish_rand(self, num, target):
        banish = random.sample(target, num)
        for element in banish:
            self.move_card(element, target, self.banished)

    def move_card(self, card, src, dest):
        src.remove(card)
        dest.append(card)

    def print_field(self):
        print ("Deck:\n{}\n".format(self.deck))
        print ("Hand:\n{}\n".format(self.hand))
        print ("Grave:\n{}\n".format(self.grave))
        print ("Banished:\n{}\n".format(self.banished))
        print ("Monster Zone:\n{}\n".format(self.m_zone))
        print ("ST Zones:\n{}\n".format(self.st_zone))
        print ("Extra Deck:\n{}".format(self.extra))
