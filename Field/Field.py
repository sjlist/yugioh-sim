import random
import Common.Common as Common
from Common.Common import bcolors
import sys
from Common.Errors import *


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
            try:
                draw = random.sample(self.deck, 1)[0]
            except ValueError:
                raise

            try:
                self._move_card(draw, self.deck, self.hand)
            except CardMissing:
                raise
            i += 1

    def banish_rand(self, num, target):
        banish = random.sample(target, num)
        for element in banish:
            try:
                self._move_card(element, target, self.banished)
            except CardMissing:
                raise

    def discard_rand(self, num):
        hand = random.sample(self.hand, num)
        for element in hand:
            try:
                self._move_card(element, self.hand, self.grave)
            except CardMissing:
                raise

    def _move_card(self, card, src, dest):
        if card not in src:
            raise CardMissing("Missing a card from the src pile", card, src)

        src.remove(card)
        dest.append(card)

    def _put_card(self, card, src, src_loc, dest, dest_loc):
        if src_loc == -1:
            if card in src:
                src.remove(card)
            else:
                raise CardMissing("Missing a card from the src pile", card, src)
        else:
            if src[src_loc] != "":
                src[src_loc] = ""
            else:
                raise ZoneError("Field Zone is empty", src_loc, src)

        if dest_loc == -1:
            dest.append(card)
        else:
            if dest[dest_loc] == "":
                dest[dest_loc] = card
            else:
                raise ZoneError("Field Zone is full", dest_loc, dest)

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

        raise PileError(pile)

    def do_action(self, action):
        # Actions are lists of length 3 or 5, [card, src, dest, src loc, dest loc]

        if action[0] == 'summon':
            card = action[1]
            pile = self.get_pile(action[2])
            try:
                self._put_card(card, pile, -1, self.m_zone, int(action[3]))
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'draw':
            try:
                self.draw_num(int(action[1]))
            except ValueError:
                raise

            return True

        if action[0] == 'TOKEN':
            if action[1] == 'summon':
                try:
                    self._put_card('TOKEN', ['TOKEN'], 0, self.m_zone, int(action[2]))
                except ZoneError:
                    raise

                return True

            if action[1] == 'remove':
                try:
                    self._put_card('TOKEN', self.m_zone, int(action[2]), [], -1)
                except (ZoneError, CardMissing):
                    raise

                return True

            raise InvalidOption("Invalid option passed in for a token", action[1])

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

                try:
                    self._move_card(card, src, dest)
                except CardMissing:
                    raise

            return True

        # This is a catch all option for now. Should not be needed in the long run
        card = action[0]
        src = self.get_pile(action[1])
        dest = self.get_pile(action[2])

        if len(action) == 3:
            try:
                self._move_card(card, src, dest)
            except CardMissing:
                raise

            return True

        if len(action) == 5:
            src_loc = int(action[3])
            dest_loc = int(action[4])
            try:
                self._put_card(card, src, src_loc, dest, dest_loc)
            except (ZoneError, CardMissing):
                raise

            return True

        raise InvalidOption("Invalid option passed into do_action", action)

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
