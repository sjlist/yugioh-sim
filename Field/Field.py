import random
import Common.Common as Common
from Common.Common import bcolors
import sys

class Field:
    def __init__(self, deck):
        self.deck = Common.dict2List(deck.main_deck)
        self.hand = []
        self.grave = []
        self.extra = Common.dict2List(deck.extra_deck)
        self.banished = []
        self.m_zone = ["", "", "", "", "", "", ""]
        self.st_zone = ["", "", "", "", ""]

    def draw_num(self, num):
        i = 0
        while i < num:
            draw = random.sample(self.deck,1)[0]
            self.do_action([draw, 'deck', 'hand'])
            i += 1

    def banish_rand(self, num, target):
        banish = random.sample(target, num)
        for element in banish:
            self.do_action([element, target, 'banished'])

    def discard_rand(self, num):
        hand = random.sample(self.hand, num)
        for element in hand:
            self._move_card(element, self.hand, self.grave)

    def _move_card(self, card, src, dest):
        src.remove(card)
        dest.append(card)

    def _put_card(self, card, src, src_loc, dest, dest_loc):
        if src_loc == -1:
            src.remove(card)
        else:
            src[src_loc] = ""

        if dest_loc == -1:
            dest.append(card)
        else:
            dest[dest_loc] = card

    def get_pile(self, pile):
        if pile == 'deck':
            return self.deck
        if pile == 'hand':
            return self.hand
        if pile == 'grave':
            return self.grave
        if pile == 'extra':
            return self.extra
        if pile == 'banished':
            return self.banished
        if pile == 'm_zone':
            return self.m_zone
        if pile == 'st_zone':
            return self.st_zone

        print("{} not a pile".format(pile))
        sys.exit()

    def do_action(self, action):
        # Actions are lists of length 3 or 5, [card, src, dest, src loc, dest loc]

        if action[0] == 'draw':
            if len(f.deck) == int(action[1]):
                print("{}Cannot draw, not enough cards in deck{}".format(bcolors.FAIL, bcolors.ENDC))
                return False
            f.draw_num(int(action[1]))
            return True

        if action[0] == 'TOKEN':
            if action[1] == 'summon':
                if self.m_zone[int(action[2])] != "":
                    print("{}{} is already in m_zone {}{}".format(bcolors.FAIL, self.m_zone[int(action[2])], int(action[2]), bcolors.ENDC))
                    return False
                self._put_card('TOKEN', ['TOKEN'], 0, self.m_zone, int(action[2]))
                return True
            if action[1] == 'remove':
                if self.m_zone[int(action[2])] != "TOKEN":
                    print("{}A token is not in m_zone {}{}".format(bcolors.FAIL, int(action[2]), bcolors.ENDC))
                    return False
                self._put_card('TOKEN', self.m_zone, int(action[2]), [], -1)
                return True
            print("{}{} is not a token action{}".format(bcolors.FAIL, action[1], bcolors.ENDC))
            return False

        if action[0] == 'discard':
            src = self.hand
            dest = self.grave
            if action[1] == 'random':
                self.discard_rand(int(action[2]))
            else:
                try:
                    card = self.hand[int(action[1])]
                except ValueError:
                    card = action[1]

                self._move_card(card, src, dest)

            return True

        card = action[0]
        src = self.get_pile(action[1])
        dest = self.get_pile(action[2])

        if len(action) == 3:
            if not card in src:
                print("{}{} is not in the {}{}".format(bcolors.FAIL, card, action[1], bcolors.ENDC))
                self.print_field()
                return False
            self._move_card(card, src, dest)
        elif len(action) == 5:
            src_loc = int(action[3])
            dest_loc = int(action[4])
            if src_loc != -1 and src[src_loc] != card:
                print("{}{} is not in the {} zone {}{}".format(bcolors.FAIL, card, action[1], src_loc, bcolors.ENDC))
                return False
            if dest_loc != -1 and dest[dest_loc] != "":
                print("{}{} is already in the {} zone {}{}".format(bcolors.FAIL, dest[dest_loc], action[2], dest_loc, bcolors.ENDC))
                return False
            self._put_card(card, src, src_loc, dest, dest_loc)
        else:
            print("{}{} is not a valid action{}".format(bcolors.FAIL, action, bcolors.ENDC))
            return False
        return True

    def combine(self, f):
        self.deck = self.deck + f.deck
        self.hand = self.hand + f.hand
        self.grave = self.grave + f.grave
        self.extra = self.extra + f.extra
        self.banished = self.banished + f.banished
        for i in range(0, len(self.m_zone)):
            if self.m_zone[i] != "" and f.m_zone[i] != "":
                print("{}Failed to combine fields, m_zone {} was full on both fields{}".format(bcolors.FAIL, i, bcolors.ENDC))
                return False
            if self.m_zone[i] == "":
                self.m_zone[i] = f.m_zone[i]

        for i in range(0, len(self.st_zone)):
            if self.st_zone[i] != "" and f.st_zone[i] != "":
                print("{}Failed to combine fields, st_zone {} was full on both fields{}".format(bcolors.FAIL, i, bcolors.ENDC))
                return False
            if self.st_zone[i] == "":
                self.st_zone[i] = f.st_zone[i]

        return True

    def print_field(self):
        print("Deck:\n{}\n".format(self.deck))
        print("Hand:\n{}\n".format(self.hand))
        print("Grave:\n{}\n".format(self.grave))
        print("Banished:\n{}\n".format(self.banished))
        print("Monster Zone:\n{}\n".format(self.m_zone))
        print("ST Zones:\n{}\n".format(self.st_zone))
        print("Extra Deck:\n{}".format(self.extra))
