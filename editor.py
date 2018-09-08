import Combo.ComboEditor as ComboEditor
import Combo.Combo as Combo
import Deck.DeckEditor as DeckEditor
import Deck.Deck as Deck
import Common.Common as Common
import os

state = 'none'
states = ['deck', 'combo', 'done']

while state != 'done':
    if state == 'none':
        state = raw_input("What would you like to edit?\n")

    while state not in states:
        print 'Error {} is not a valid part of the deck'.format(state)
        print 'deck or combo are the valid parts of the deck'
        state = raw_input("What would you like to edit?\n")

    if state == 'deck':
        name = raw_input("What deck would you like to edit?\n")
        if name in states:
            state = 'none'
        elif not Common.fileExists("decks", "{}.txt".format(name)):
            print('{} is not a deck'.format(name))
            ans = raw_input("Would you like to make it?\n")
            if ans == 'y':
                DeckEditor.create_deck(name)
        else:
            d = Deck.Deck(name)
            d.load(name)
            DeckEditor.edit_deck(d)

    if state == 'combo':
        name = raw_input("What combo would you like to edit?\n")
        if name in states:
            state = 'none'
        else:
            (exists, folder) = Common.parentFolder("combos", "{}.txt".format(name))
            if not exists:
                print('{} is not a combo'.format(name))
                ans = raw_input("Would you like to make it?\n")
                if ans == 'y':
                    ComboEditor.create_combo(name)
            else:
                c = Combo.Combo()
                c.load(name, folder)
                ComboEditor.edit_combo(c)
