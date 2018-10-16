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
        self.lifepoints = 8000

    def check_activation(self, effect, location):
        activation_location = effect["location"]
        if activation_location != location:
            return False

        for field_element in effect["activation"]:
            pile = self.get_field_element(field_element)

            if field_element == 'lifepoints':
                 if pile < effect["activation"][field_element]:
                    return False

            else:
                for req in effect["activation"][field_element]:
                    count = 0
                    for card in pile:
                        if card.name == req:
                            count += 1
                    if count < effect["activation"][field_element][req]:
                        return False

        return True

    def pay_cost(self, effect):
        for element in effect["cost"]:
            try:
                self.do_action(element)
            except (ZoneError, CardMissing, PileError, InvalidOption, SummonError):
                return False

        return True

    # Run the effect, raise any errors
    def do_effect(self, effect, options):
        option=0
        for element in effect["actions"]:
            try:
                searching = True
                found_indexes = []
                while searching:
                    if "OPTION{}".format(option) in element:
                        option_index = element.index("OPTION{}".format(option))
                        found_indexes.append(option_index)
                        element[option_index] = options[option]
                        option += 1
                    else:
                        searching = False
                self.do_action(element)

                for count in range(0, len(found_indexes)):
                    element[found_indexes[count]] = 'OPTION{}'.format(option - (len(found_indexes) - count))

            except (ZoneError, CardMissing, SummonError):
                raise

    def activate_effect(self, card, location, effect_number, options=[]):
        effect = card.effects[effect_number]
        if not self.check_activation(effect, location):
            return False
        can_pay = self.pay_cost(effect)
        if not can_pay:
            return False

        try:
            self.do_effect(effect, options)
        except (ZoneError, CardMissing, SummonError):
            raise

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

    def get_field_pile(self, name, zone):
        try:
            if hasattr(self.m_zone[zone], 'name') and name == self.m_zone[zone].name:
                return self.m_zone
            elif hasattr(self.st_zone[zone], 'name') and name == self.st_zone[zone].name:
                return self.st_zone
            else:
                raise CardMissing("Card not in the Field", name, self.m_zone + self.st_zone)
        except IndexError:
            raise CardMissing("Card not in the Field", name, self.m_zone + self.st_zone)

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

    # returns first card of ANY* type in given pile
    def get_any_type_card(self, card, pile, zone):
        if zone == -1:
            if card == "ANYCARD":
                return pile[0]

            type = card[3:].lower()
            for card in pile:
                if card.type == type:
                    return card
        else:
            type = card[3:].lower()
            if type == self.m_zone[zone].type:
                return self.m_zone[zone]
            elif type == self.st_zone[zone].type:
                return self.st_zone[zone]
            else:
                raise CardMissing("Missing {} from zone {}".format(card, zone), Card.Card(card, type), self.st_zone + self.m_zone)

    # get the pile from a pile name
    def get_field_element(self, pile):
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
        if pile == 'lifepoints':
            return self.lifepoints

        raise PileError(pile)

    # get the card from the field
    def get_card(self, name, pile, zone=-1):
        if name[:3] == "ANY":
            try:
                return self.get_any_type_card(name, pile, zone)
            except CardMissing:
                raise

        if zone == -1:
            for element in pile:
                if element.name == name:
                    return element
        elif 0 <= zone <= len(pile) and pile[zone].name == name:
            return pile[zone]
        else:
            raise ZoneError("Zone {} does not exist".format(zone), zone, pile)

        raise CardMissing("Could not find card {}".format(name), name, pile)

    # do an action
    def do_action(self, action):
        if action[0] == "pause":
            # action: ["pause"]
            raw_input()
            return True

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
            try:
                pile = self.get_field_pile(action[1], action[2])
                card = self.get_card(action[1], pile, action[2])
                self.field_to_pile(card, action[2], pile, self.banished)
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'banish_pile':
            # action: ['banish', CARD, pile]
            try:
                pile = self.get_field_element(action[2])
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
                pile = self.get_field_element(action[2])
                card = self.get_card(action[1], pile)
                self.summon(card, pile, action[3])
                self.normal_summons[0] += 1
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'special_summon':
            # action: ['special_summon', CARD, pile, M_ZONE_LOC]
            # TOKEN action: ['special_summon', 'TOKEN', M_ZONE_LOC]

            try:
                if action[1] == "TOKEN":
                    self.do_action([action[1], "summon", action[2]])
                    return True
                pile = self.get_field_element(action[2])
                card = self.get_card(action[1], pile)
                self.summon(card, pile, action[3])
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'send_to_grave_pile':
            # action: ['send_to_grave_pile', CARD, pile]
            try:
                pile = self.get_field_element(action[2])
                card = self.get_card(action[1], pile)
                self._move_card(card, pile, self.grave)
            except (ZoneError, CardMissing):
                raise

            return True

        if action[0] == 'send_to_grave_zone':
            # action: ['send_to_grave', card, zone_location]
            try:
                if action[1] == "TOKEN":
                    self.do_action([action[1], "remove", action[2]])
                    return True
                if action[1][:3] != "ANY":
                    pile = self.get_field_pile(action[1], action[2])
                    card = self.get_card(action[1], pile, action[2])
                else:
                    card = self.get_card(action[1], [], action[2])
                    pile = self.get_field_pile(card.name, action[2])

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
                pile = self.get_field_element(action[2])
                card = self.get_card(action[1], pile)
                self._move_card(card, pile, self.hand)
            except CardMissing:
                raise

            return True

        if action[0] == 'tribute_summon':
            # action ['tribute_summon', CARD, pile, zone, (tributes)[[CARD, zone]]]
            try:
                for tribute in action[4]:
                    self.do_action(['send_to_grave_zone', tribute[0], tribute[1]])
                self.do_action(['normal_summon', action[1], action[2], action[3]])
            except (ZoneError, CardMissing, SummonError):
                raise

            return True

        if action[0] == "link_summon":
            # action: ['link_summon', CARD, zone, (materials)[[CARD, zone]]]
            card = self.get_card(action[1], self.extra)
            if card.type != "link":
                raise SummonError("{} is not a link monster, cannot link summon".format(action[1]))
            try:
                for material in action[3]:
                    self.do_action(['send_to_grave_zone', material[0], material[1]])
                self.do_action(['special_summon', action[1], 'extra', action[2]])
            except (ZoneError, CardMissing, SummonError):
                raise

            return True

        if action[0] == "fusion_summon":
            # action: ['fusion_summon', CARD, zone, (materials)[[CARD, zone]]]
            card = self.get_card(action[1], self.extra)
            if card.type != "fusion":
                raise SummonError("{} is not a fusion monster, cannot fusion summon".format(action[1]))
            try:
                self.do_action(['special_summon', action[1], 'extra', action[2]])
            except (ZoneError, CardMissing, SummonError):
                raise

            return True

        if action[0] == "lifepoints":
            # action: ['lifepoints', LP_CHANGE]
            if self.lifepoints + action[1] < 0:
                raise InvalidEffect("Can't pay cost of {} LP".format(action[1]))

            self.lifepoints += action[1]

            return True

        if action[0] == "activate_effect":
            # action: ['activate_effect', CARD, pile, effect_number, [OPTIONS], zone]
            pile = self.get_field_element(action[2])

            try:
                if len(action) == 6:
                    card = self.get_card(action[1], pile, action[5])
                    self.activate_effect(card, action[2], action[3], action[4])
                else:
                    card = self.get_card(action[1], pile)
                    self.activate_effect(card, action[2], action[3], action[4])
            except (ZoneError, CardMissing, SummonError):
                raise

            return True

        raise InvalidOption("Invalid option passed into do_action", action)

# Print the field state
    def print_field(self):
        self.print_zone(self.deck, "Deck")
        self.print_zone(self.hand, "Hand")
        self.print_zone(self.grave, "Grave")
        self.print_zone(self.banished, "Banished")
        self.print_zone(self.m_zone, "M_zone")
        self.print_zone(self.st_zone, "St_zone")
        self.print_zone(self.extra, "Extra")
        print("Lifepoints: {}".format(self.lifepoints))

    def print_zone(self, zone, name):
        l = []
        for card in zone:
            try:
                l.append(card.name)
            except AttributeError:
                l.append(card)
        print("{}:\n{}\n".format(name, l))
