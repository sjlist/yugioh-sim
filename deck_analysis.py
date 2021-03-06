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
from subprocess import call


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
        d.print_deck()
        combo_names = {}
        combo_chance = {}
        obsolete_combo_names = {}
        obsolete_combo_chance = {}
        if os.path.isfile("./combos/{}/{}.json".format(d.combo_folder, self.combo)):
            combo_names[self.combo] = Combo.Combo()
            combo_names[self.combo].load(self.combo, d.combo_folder)
            combo_chance[self.combo] = 0
        else:
            combo_names, combo_chance = self.load_combos(d)
            obsolete_combo_names, obsolete_combo_chance = self.load_combos(d, "obsolete")

        if self.time_combos:
            for value in combo_names.values():
                self.analyze_combo_timing(d, value)

        combo_chance["Brick"] = 0
        obsolete_combo_chance["Brick"] = 0

        if self.calculate_chances:
            if len(obsolete_combo_chance) > 1:
                self.calculate_combo_chances(obsolete_combo_names, obsolete_combo_chance, d, "Obsolete")
            if len(combo_chance) > 1:
                self.calculate_combo_chances(combo_names, combo_chance, d, "Combo")

    def print_chances(self, combo_chance, name):
        l = []
        sorted_chances = sorted(combo_chance, key=combo_chance.__getitem__)
        sorted_chances.reverse()
        for key in sorted_chances:
            if combo_chance[key] != 0 and key != 'Brick':
                l.append([key, combo_chance[key]*100])
        l.append(['Brick', combo_chance['Brick']*100])
        print(tabulate(l, headers=[name, '% Chance']))

    def load_combos(self, d, subfolder=""):
        combo_names = {}
        combo_chance = {}
        for element in os.listdir("./combos/{}/{}".format(d.combo_folder, subfolder)):
            if os.path.isfile("./combos/{}/{}/{}".format(d.combo_folder, subfolder, element)):
                name = element.split(".")[0]
                c = Combo.Combo()
                c.load(name, "{}/{}".format(d.combo_folder, subfolder))
                if self.can_combo(d, c):
                    combo_names[name] = deepcopy(c)
                    combo_chance[name] = 0
                    
        return combo_names, combo_chance

    def can_combo(self, d, c):
        for subcombo in c.subcombos:
            if subcombo[1] == 'r':
                sc = Combo.Combo()
                sc.load(subcombo[0], "{}/subcombos".format(c.folder))
                if not self.can_combo(d, sc):
                    return False
        for req in c.combo_reqs:
            for key in req.keys():
                card_found = False
                for type in d.main_deck:
                    if key in d.main_deck[type]:
                        if d.main_deck[type][key] < req[key]:
                            return False
                        else:
                            card_found = True

                for type in d.extra_deck["monster"]:
                    if key in d.extra_deck["monster"][type]:
                        if d.extra_deck["monster"][type][key] < req[key]:
                            return False
                        else:
                            card_found = True

                if key[:3] != "ANY" and not card_found:
                    return False

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

            try:
                f.do_action(action)
            except (CardMissing, ValueError, InvalidOption, ZoneError, PileError, SummonError):
                raise

            pr.disable()
            s = StringIO.StringIO()
            sortby = 'tottime'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)

            move_times[action_number] = ps.total_tt

            action_number += 1

        return move_times

    def analyze_combo_timing(self, d, c):
        move_times = {}
        for tries in range(0, len(c.movement)):
            move_times[tries] = 0

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
            print(tabulate(sorted_list, headers=['Move', 'Movement Time']))

        else:
            print("No timing data for combo {}".format(c.name))

    def calculate_combo_chances(self, combo_names, combo_chance, d, name):
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
            state = random.getstate()

            for key in combo_names.keys():
                random.setstate(state)
                f = Field.Field(d)
                f.draw_num(5)
                if combo_names[key].is_combo(f, True):
                    combo_chance[key] += 1
                    was_combo = True

            call("rm temp/*", shell=True)

            if not was_combo:
                combo_chance["Brick"] += 1

        pr.disable()
        s = StringIO.StringIO()
        sortby = 'tottime'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(20)

        print("")

        for key in combo_chance.keys():
            combo_chance[key] = combo_chance[key] / self.MAX_TRIES
        self.print_chances(combo_chance, name)

        print(s.getvalue())
