import Field
import Deck.Deck as Deck
import Combo.Combo as Combo

d = Deck.Deck()
d.load("World_Chalice_Undine")
c1 = Combo.Combo()
c1.load("Venus_3", "World_Chalice")
c2 = Combo.Combo()
c2.load("Undine", "World_Chalice")
comboThere = False
i = 0
while (not comboThere):
    i += 1
    f = Field.Field(d)
    if c1.isCombo(f):
        comboThere = True
        print "Try {} C1: {}".format(i, f.hand)
    if c2.isCombo(f):
        comboThere = True
        print "Try {} C2: {}".format(i, f.hand)
