import Field.Field as F
import Deck.Deck as D
import Deck.Card as C

if __name__ == '__main__':
    d = D.Deck("World_Chalice_3")
    d.load(d.deck_name)

    f = F.Field(d)

    c_venus = C.Card("The Agent of Creation - Venus")
    c_venus.load()
    f.hand.append(c_venus)

    c_lee = C.Card("Lee the World Chalice Fairy")
    c_lee.load()
    f.hand.append(c_lee)

    f.print_field()

    c_bf = C.Card("Brilliant Fusion")
    c_bf.load()

    f.hand.append(c_bf)

    f.do_action(['activate_effect', 'Brilliant Fusion', 'hand', 0, ['Gem-Knight Seraphinite', 6, 'Gem-Knight Garnet', 'Lee the World Chalice Fairy', 0]])
    f.do_action(['increase_normal_summons'])
    f.do_action(['normal_summon', 'The Agent of Creation - Venus', 'hand', 0])
    f.do_action(['activate_effect', 'The Agent of Creation - Venus', 'm_zone', 0, ['deck', 1], 0])
    f.do_action(['activate_effect', 'The Agent of Creation - Venus', 'm_zone', 0, ['deck', 3], 0])
    f.do_action(['activate_effect', 'The Agent of Creation - Venus', 'm_zone', 0, ['deck', 4], 0])
    f.do_action(['normal_summon', 'Lee the World Chalice Fairy', 'hand', 2])
    f.do_action(['activate_effect', 'Lee the World Chalice Fairy', 'm_zone', 0, ['World Legacy - \"World Chalice\"'], 2])
    f.do_action(['link_summon', 'Summon Sorceress', 6, [['Lee the World Chalice Fairy', 2], ['Mystical Shine Ball', 1], ['Gem-Knight Seraphinite', 6]]])
    f.do_action(['activate_effect', 'Lee the World Chalice Fairy', 'grave', 1, ['World Legacy - \"World Chalice\"']])
    f.do_action(['link_summon', 'Firewall Dragon', 6, [['Summon Sorceress', 6], ['Mystical Shine Ball', 4]]])
    f.do_action(['activate_effect', 'Firewall Dragon', 'm_zone', 0, ['Lee the World Chalice Fairy', 4], 6])

    f.print_field()
