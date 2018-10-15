import cPickle as pickle
import Combo.Combo as combo

import Field.Field as F
import Deck.Deck as D
import Deck.Card as C
import Deck.Effect as E

d = D.Deck("World_Chalice_3")
d.load(d.deck_name)

f = F.Field(d)

e = E.Effect(cost=[['lifepoints', -500]], actions=[['special_summon', 'Mystical Shine Ball', 'deck', 'OPTION0']], activation={'deck': {'Mystical Shine Ball': 1}, 'lifepoints': 500})

c = C.Card("The Agent of Creation - Venus")
c.load()
f.hand.append(c)

f.do_action(['special_summon', 'The Agent of Creation - Venus', 'hand', 0])
# f.print_field()

f.do_action(['activate_effect', 'The Agent of Creation - Venus', 'm_zone', 0, [1], 0])

f.print_field()
