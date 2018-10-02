from __future__ import division
import Field.Field as Field
import os
import Deck.Deck as Deck
import Combo.Combo as Combo
from Common.Errors import *
from copy import deepcopy
from tabulate import tabulate
import cProfile
import pstats
import StringIO
import random

class Combo_Analyzer():
    def __init__(self, deck_name, MAX_TRIES, combo="", time_combos=False, calculate_chances=True):
        self.deck_name = deck_name
        self.MAX_TRIES = MAX_TRIES
        self.combo = combo
        self.time_combos = time_combos
        self.calculate_chances = calculate_chances

    def analyze_combos(self):
        d = Deck.Deck()
        d.load(self.deck_name)
        combo_names = {}
        combo_chance = {}
        if os.path.isfile("./combos/{}/{}.json".format(d.combo_folder, self.combo)):
            combo_names[self.combo] = Combo.Combo()
            combo_names[self.combo].load(self.combo, d.combo_folder)
            combo_chance[self.combo] = 0
        else:
            for element in os.listdir("./combos/{}".format(d.combo_folder)):
                if os.path.isfile("./combos/{}/{}".format(d.combo_folder, element)):
                    name = element.split(".")[0]
                    c = Combo.Combo()
                    print name
                    c.load(name, d.combo_folder)
                    if self.can_combo(d, c):
                        print name
                        combo_names[name] = deepcopy(c)
                        combo_chance[name] = 0

        if self.time_combos:
            for value in combo_names.values():
                self.analyze_combo_timing(d, value)

        combo_chance["Brick"] = 0

        if self.calculate_chances:
            self.calculate_combo_changes(combo_names, combo_chance, d)

    def print_chances(self, combo_chance):
        l = []
        sorted_chances = sorted(combo_chance, key=combo_chance.__getitem__)
        sorted_chances.reverse()
        for key in sorted_chances:
            if combo_chance[key] != 0 and key != 'Brick':
                l.append([key, combo_chance[key]*100])
        l.append(['Brick', combo_chance['Brick']*100])
        print tabulate(l, headers=['Combo', '% Chance'])

    def can_combo(self, d, c):
        for req in c.combo_reqs:
            for key in req.keys():
                card_found = False
                for type in d.main_deck:
                    if key in d.main_deck[type]:
                        if d.main_deck[type][key] < req[key]:
                            print 1
                            return False
                        else:
                            card_found = True

                for type in d.extra_deck:
                    if key in d.extra_deck[type]:
                        if d.extra_deck[type][key] < req[key]:
                            print 2
                            return False
                        else:
                            card_found = True

                if key != "ANYCARD" and not card_found:
                    print 3
                    return False
        print 4
        return True

    def time_combo(self, c, d):
        f = Field.Field(d)
        f.draw_num(5)

        move_times = {}
        if not c.is_combo(f, False):
            return move_times

        action_number = 0
        for action in c.movement:
            if not action:
                break

            pr = cProfile.Profile()
            pr.enable()


            # Hacky way to do discarding... maybe handle in field?
            # Trying to not discard a card that is in the combo if the discarding is a choice
            if action[0] == 'discard' and action[1] == 'ANYCARD':
                count = 0
                while action[1] == 'ANYCARD':
                    if count == len(f.hand):
                        return move_times

                    if not c.in_combo(f.hand[count]) or f.hand[count] == 'ANYCARD':
                        action[1] = f.hand[count]
                        break

                    count += 1

            try:
                f.do_action(action)
            except (CardMissing, ValueError, InvalidOption, ZoneError, PileError, SummonError):
                raise

            # Undoing hacky discard
            if len(action) == 2 and action[0] == 'discard':
                action[1] = 'ANYCARD'

            pr.disable()
            s = StringIO.StringIO()
            sortby = 'tottime'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)

            move_times[action_number] = ps.total_tt

            action_number += 1

        return move_times

    def analyze_combo_timing(self, d, c):
        move_times = {}
        t = {}
        tries = 0
        for element in c.movement:
            move_times[tries] = 0
            tries += 1

        tries = 0
        successes = 0
        while tries < self.MAX_TRIES:
            tries += 1
            t = self.time_combo(c, d)
            if t:
                for key in t.keys():
                    move_times[key] = move_times.get(key) + t[key]
                    successes += 1

        sorted_chances = sorted(move_times, key=move_times.__getitem__)
        sorted_chances.reverse()

        sorted_list = []
        total_time = 0
        if len(move_times) != 1 and move_times[0] != 0:
            for element in sorted_chances:
                sorted_list.append([c.movement[element], move_times[element]/ move_times[sorted_chances[0]]])
                total_time += move_times[element]

            for key in move_times.keys():
                move_times[key] = move_times[key] / move_times[sorted_chances[0]]

            sorted_list.append(['Total Time for {}'.format(c.name), total_time])
            print tabulate(sorted_list, headers=['Move', 'Movement Time'])

        else:
            print "No timing data for combo {}".format(c.name)

    def calculate_combo_changes(self, combo_names, combo_chance, d):
        pr = cProfile.Profile()
        pr.enable()

        i = 0
        percent = 0
        percent_increment = 10
        while i < self.MAX_TRIES:
            if i > (self.MAX_TRIES - 2) * percent * percent_increment / 100:
                total_done = percent_increment * percent
                print("{}% Done".format(total_done))
                percent += 1
            i += 1
            was_combo = False
            f = Field.Field(d)
            f.draw_num(5)

            for key in combo_names.keys():
                f = Field.Field(d)
                f.draw_num(5)
                if combo_names[key].is_combo(f, True):
                    combo_chance[key] += 1
                    was_combo = True

            if not was_combo:
                combo_chance["Brick"] += 1


        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumtime'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(20)

        for key in combo_chance.keys():
            combo_chance[key] = combo_chance[key] / self.MAX_TRIES

        self.print_chances(combo_chance)
        print s.getvalue()
