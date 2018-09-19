from __future__ import division
import Field.Field as Field
import os
import Deck.Deck as Deck
import Combo.Combo as Combo
from copy import deepcopy
from tabulate import tabulate


class Combo_Analyzer():
    def __init__(self, deck_name, MAX_TRIES, combo=""):
        self.deck_name = deck_name
        self.MAX_TRIES = MAX_TRIES
        self.combo = combo

    def analyze_combos(self):
        d = Deck.Deck()
        d.load(self.deck_name)
        combo_names = {}
        combo_chance = {}
        if os.path.isfile("./combos/{}/{}.txt".format(d.combo_folder, self.combo)):
            combo_names[self.combo] = Combo.Combo()
            combo_names[self.combo].load(self.combo, d.combo_folder)
            combo_chance[self.combo] = 0
        else:
            for element in os.listdir("./combos/{}".format(d.combo_folder)):
                if os.path.isfile("./combos/{}/{}".format(d.combo_folder, element)):
                    name = element.split(".")[0]
                    c = Combo.Combo()
                    c.load(name, d.combo_folder)
                    if self.can_combo(d, c):
                        combo_names[name] = deepcopy(c)
                        combo_chance[name] = 0

        combo_chance["Brick"] = 0

        i = 0
        while i < self.MAX_TRIES:
            i += 1
            was_combo = False
            f = Field.Field(d)
            f.draw_num(5)

            for key in combo_names.keys():
                f = Field.Field(d)
                f.draw_num(5)
                if combo_names[key].is_combo(f, False):
                    combo_chance[key] += 1
                    was_combo = True

            if not was_combo:
                combo_chance["Brick"] += 1

        for key in combo_chance.keys():
            combo_chance[key] = combo_chance[key] / self.MAX_TRIES

        self.print_chances(combo_chance)

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
                if key in d.main_deck:
                    if d.main_deck[key] < req[key]:
                        return False
                elif key in d.extra_deck:
                    if d.extra_deck[key] < req[key]:
                        return False
                elif key != "ANYCARD":
                    return False

        return True