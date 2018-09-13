import Combo.Combo as Combo
import Deck.Deck as Deck
import Field.Field as Field
import Common.Common as Common
from itertools import combinations
import sys


class ComboTest:
    def __init__(self, name, folder):
        self.combo = Combo.Combo()
        self.combo.load(name, folder)

    def testReq(self, req):
        req_list = Common.dict2List(req)
        for i in xrange(1, len(req_list) + 1):
            perms = list(combinations(req_list, i))
            for p in perms:
                result = self.combo.allThere(req, list(p))
                if result and i < len(req_list):
                    return False , list(p)

                if not result and i == len(req_list):
                    return False, list(p)

        return True, []

    def testCombo(self):
        print("Testing {}/{} requirements".format(self.combo.folder, self.combo.name))
        for requirement in self.combo.combo_reqs:
            (result, error_state) = self.testReq(requirement)
            if not result:
                print("Failed testing {}/{} on requirement {} with error state {}".format(self.combo.folder, self.combo.name, requirement, error_state))
                sys.exit()

        print("{}/{} passed requirement check".format(self.combo.folder, self.combo.name))

        deck = Deck.Deck("UnitTest_{}".format(self.combo.name))
        f = Field.Field(deck)
        for subcombo in self.combo.subcombos:
            if subcombo:
                print "Setting up Subcombo {}".format(subcombo)
                sc = Combo.Combo()
                sc.load(subcombo, "{}/subcombos".format(self.combo.folder))
                f.hand = f.hand + Common.dict2List(sc.hand)
                f.deck = f.deck + Common.dict2List(sc.deck) + Common.dict2List(sc.hand_or_deck)
                f.extra = f.extra + Common.dict2List(sc.extra)
                f.grave = f.grave + Common.dict2List(sc.grave)
                sc.playCombo(f)
                print "Subcombo {} set up".format(subcombo)

        f.hand = f.hand + Common.dict2List(self.combo.hand)
        f.deck = f.deck + Common.dict2List(self.combo.deck) + Common.dict2List(self.combo.hand_or_deck)
        f.extra = f.extra + Common.dict2List(self.combo.extra)
        f.grave = f.grave + Common.dict2List(self.combo.grave)

        self.combo.playCombo(f)
        print("{}/{} passed movement check".format(self.combo.folder, self.combo.name))

