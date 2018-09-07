import random

class Field:
    def __init__(deck):
        self.deck     = deck
        self.hand     = []
        self.grave    = []
        self.banished = []
        self.m_zone   = ["", "", "", "", "", "", ""]
        self.st_zone  = ["", "", "", "", ""]
        self.draw_num(5)

    def draw_num(self, num):
        i = 0
        while i < num:
            draw = random.sample(src,1)
            self.move_card(draw, self.deck, self.hand)
            i += 1

    def banish_rand(self, num, target):
        banish = random.sample(target, num)
        for element in banish:
            self.move_card(element, target, self.banished)

    def move_card(card, src, dest):
        src.remove(card)
        dest.append(card)
