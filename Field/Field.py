import random
from Common.Common import bcolors
from Common.Errors import *
import Deck.Card as Card


class Field:
    def __init__(self, deck):
        self.deck = deck.init_main()
        self.hand = []
        self.grave = []
        self.extra = deck.init_extra()
        self.banished = []
        self.m_zone = ["", "", "", "", "", "", ""]
        self.st_zone = ["", "", "", "", ""]
        self.normal_summons = [0, 1]

    # summon a card from a pile into a zone number
    def summon(self, card, pile, zone):
        try:
            self._put_card(card, pile, -1, self.m_zone, zone)
        except (ZoneError, CardMissing):
            raise

    # Send a card from the field (either m_zone or st_zone) to the grave
    def field_to_pile(self, card, loc, pile, target):
        try:
            self._put_card(card, pile, loc, target, -1)
        except (ZoneError, CardMissing):
            raise

    # draw some number of cards from the deck to the hand
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

    # Banish num cards randomly from a pile
    def banish_rand(self, num, pile):
        banish = random.sample(pile, num)
        for element in banish:
            try:
                self._move_card(element.name, pile, self.banished)
            except CardMissing:
                raise

    def discard(self, card):
        try:
            self._move_card(card, self.hand, self.grave)
        except CardMissing:
            raise

    # discard num random cards from the hand
    def discard_rand(self, num):
        hand = random.sample(self.hand, num)
        for element in hand:
            try:
                self.discard(element)
            except CardMissing:
                raise

    # move a card from src pile to dest pile
    def _move_card(self, card, src, dest):
        found_card = False
        for element in src:
            if card == element:
                found_card = True

        if not found_card:
            raise CardMissing("Missing a card from the src pile", card.name, src)

        src.remove(card)
        dest.append(card)

    # put a card from a zone to a dest zone
    def _put_card(self, card, src, src_loc, dest, dest_loc):
        if src_loc == -1:
            found_card = False
            for element in src:
                if card == element:
                    src.remove(card)
                    found_card = True
                    break

            if not found_card:
                raise CardMissing("Missing a card from the src pile", card.name, src)
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

    # get the pile from a pile name
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

    def get_card(self, name, pile, zone=-1):
        if zone == -1:
            for element in pile:
                if element.name == name:
                    return element
        elif 0 <= zone <= len(pile):
            return pile[zone]
        else:
            raise ZoneError("Zone {} does not exist".format(zone), zone, pile)

        raise CardMissing("Could not find card {}".format(name), name, pile)

    # do an action
    def do_action(self, action):

        # No card actions
        if action[0] == 'draw':
            # action ['draw', NUM]
            self.draw_num(action[1])

            return True

        if action[0] == 'increase_normal_summons':
            # action: ['increase_normal_summons']
            if self.normal_summons[1] == 2:
                raise InvalidEffect("Cannot increase normal summons to more than 2")
            self.normal_summons[1] += 1

            return True

        if action[0] == 'play_spell':
            # action ['play_spell', card, zone], implied from hand
            try:
                card = self.get_card(action[1], self.hand)
                self._put_card(card, self.hand, -1, self.st_zone, action[2])
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'banish_zone':
            # action: ['banish', CARD, zone]
            if hasattr(self.m_zone[action[2]], 'name') and action[1] == self.m_zone[action[2]].name:
                pile = self.m_zone
            elif hasattr(self.st_zone[action[2]], 'name') and action[1] == self.st_zone[action[2]].name:
                pile = self.st_zone
            else:
                raise CardMissing("Card not in the Field", action[1], self.m_zone + self.st_zone)

            try:
                card = self.get_card(action[1], pile, action[2])
                self.field_to_pile(card, action[2], pile, self.banished)
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'banish_pile':
            # action: ['banish', CARD, pile]
            try:
                pile = self.get_pile(action[2])
                card = self.get_card(action[1], pile)
                self._move_card(card, pile, self.banished)
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'normal_summon':
            # action: ['normal_summon', CARD, pile, M_ZONE_LOC]
            if self.normal_summons[0] == self.normal_summons[1]:
                raise SummonError("Normal Summons used up")
            try:
                pile = self.get_pile(action[2])
                card = self.get_card(action[1], pile)
                self.summon(card, pile, action[3])
                self.normal_summons[0] += 1
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'special_summon':
            # action: ['special_summon', CARD, pile, M_ZONE_LOC]
            try:
                pile = self.get_pile(action[2])
                card = self.get_card(action[1], pile)
                self.summon(card, pile, action[3])
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'send_to_grave_pile':
            # action: ['send_to_grave_pile', CARD, pile]
            try:
                pile = self.get_pile(action[2])
                card = self.get_card(action[1], pile)
                self._move_card(card, pile, self.grave)
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'send_to_grave_zone':
            # action: ['send_to_grave', card, zone_location]
            if hasattr(self.m_zone[action[2]], 'name') and action[1] == self.m_zone[action[2]].name:
                pile = self.m_zone
            elif hasattr(self.st_zone[action[2]], 'name') and action[1] == self.st_zone[action[2]].name:
                pile = self.st_zone
            else:
                raise CardMissing("Card not in the Field", action[1], self.m_zone + self.st_zone)

            try:
                card = self.get_card(action[1], pile, action[2])
                self.field_to_pile(card, action[2], pile, self.grave)
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'TOKEN':
            # action: ['TOKEN', 'summon'/'remove', M_ZONE]
            if action[1] == 'summon':
                token_card = Card.Card('TOKEN', 'monster')
                try:
                    self._put_card(token_card, [token_card], -1, self.m_zone, action[2])
                except ZoneError:
                    raise

                return True

            if action[1] == 'remove':
                try:
                    token_card = self.get_card('TOKEN', self.m_zone, action[2])
                    self._put_card(token_card, self.m_zone, action[2], [], -1)
                except (ZoneError, CardMissing):
                    raise

                return True

            raise InvalidOption("Invalid option passed in for a token", action[1])

        if action[0] == 'discard':
            # action: ['discard', CARD/'random', NUM(IF RANDOM)]

            if action[1] == 'random':
                self.discard_rand(action[2])
            else:
                try:
                    card = self.hand[int(action[1])]
                except ValueError:
                    card = self.get_card(action[1], self.hand)

                try:
                    self.discard(card)
                except CardMissing:
                    raise

            return True

        if action[0] == 'add_to_hand':
            # action: ['add_to_hand', CARD, pile]
            try:
                pile = self.get_pile(action[2])
                card = self.get_card(action[1], pile)
                self._move_card(card, pile, self.hand)
            except CardMissing:
                raise

            return True

        raise InvalidOption("Invalid option passed into do_action", action)

    # combine two fields
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

    def print_zone(self, zone, name):
        l = []
        for card in zone:
            try:
                l.append(card.name)
            except AttributeError:
                l.append(card)
        print("{}:\n{}\n".format(name, l))


# Print the field state
    def print_field(self):
        self.print_zone(self.deck, "Deck")
        self.print_zone(self.hand, "Hand")
        self.print_zone(self.grave, "Grave")
        self.print_zone(self.banished, "Banished")
        self.print_zone(self.m_zone, "M_zone")
        self.print_zone(self.st_zone, "St_zone")
        self.print_zone(self.extra, "Extra")
