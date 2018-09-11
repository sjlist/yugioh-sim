from __future__ import division
import Field.Field as Field
import os
import Deck.Deck as Deck
import Combo.Combo as Combo
import sys

class ComboAnalyzer():
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
                if os.path.isfile("./combos/{}/{}".format(d.combo_folder,element)):
                    name = element.split(".")[0]
                    combo_names[name] = Combo.Combo()
                    combo_names[name].load(name, d.combo_folder)
                    combo_chance[name] = 0

        combo_chance["Brick"] = 0

        i = 0
        while (i < self.MAX_TRIES):
            i += 1
            wasCombo = False
            f = Field.Field(d)
            f.draw_num(5)

            for key in combo_names.keys():
                f = Field.Field(d)
                f.draw_num(5)
                if combo_names[key].isCombo(f):
                    combo_chance[key] += 1
                    wasCombo = True

            if not wasCombo:
                combo_chance["Brick"] += 1

        for key in combo_chance.keys():
            combo_chance[key] = combo_chance[key] / self.MAX_TRIES

        self.print_chances(combo_chance)

    def print_chances(self, combo_chance):
        for key in combo_chance.keys():
            if combo_chance[key] != 0 and key != 'Brick':
                print ("The chance of opening {} is {}%".format(key, combo_chance[key]*100))
        print ("The chance of opening {} is {}%".format('Brick', combo_chance['Brick']*100))
