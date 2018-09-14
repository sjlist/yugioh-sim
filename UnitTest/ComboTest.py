import Combo.Combo as Combo
import Deck.Deck as Deck
import Field.Field as Field
import Common.Common as Common
from Common.Common import bcolors
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
                    return False, list(p)

                if not result and i == len(req_list):
                    return False, list(p)

        return True, []

    def testCombo(self):
        print("{}Testing {}/{} requirements{}".format(bcolors.OKBLUE, self.combo.folder, self.combo.name, bcolors.ENDC))
        for requirement in self.combo.combo_reqs:
            (result, error_state) = self.testReq(requirement)
            if not result:
                print("{}Failed testing {}/{} on requirement {} with error state {}{}".format(bcolors.FAIL, self.combo.folder, self.combo.name, requirement, error_state, bcolors.ENDC))
                sys.exit()

        print("{}{}/{} passed requirement check{}".format(bcolors.OKGREEN, self.combo.folder, self.combo.name, bcolors.ENDC))

        deck = Deck.Deck("UnitTest_{}".format(self.combo.name))
        f = Field.Field(deck)
        for subcombo in self.combo.subcombos:
            if subcombo:
                print("{}Setting up Subcombo {}{}".format(bcolors.OKBLUE, subcombo[0], bcolors.ENDC))
                sc = Combo.Combo()
                sc.load(subcombo[0], "{}/subcombos".format(self.combo.folder))

                f.hand = f.hand + Common.dict2List(sc.hand)
                f.deck = f.deck + Common.dict2List(sc.deck) + Common.dict2List(sc.hand_or_deck)
                f.extra = f.extra + Common.dict2List(sc.extra)
                f.grave = f.grave + Common.dict2List(sc.grave)
                result, error_state = sc.playCombo(f)
                if not result:
                    print("{}Failed testing {}/{} on subcombo {}'s movement check, action {}{}".format(bcolors.FAIL, self.combo.folder, self.combo.name, sc.name, error_state, bcolors.ENDC))
                    sys.exit()
                print("{}Subcombo {} set up{}".format(bcolors.OKGREEN, subcombo[0], bcolors.ENDC))

        f.hand = f.hand + Common.dict2List(self.combo.hand)
        f.deck = f.deck + Common.dict2List(self.combo.deck) + Common.dict2List(self.combo.hand_or_deck)
        f.extra = f.extra + Common.dict2List(self.combo.extra)
        f.grave = f.grave + Common.dict2List(self.combo.grave)

        result, error_state = self.combo.playCombo(f)
        if not result:
            print("{}Failed testing {}/{} on movement check, action {}{}".format(bcolors.FAIL, self.combo.folder, self.combo.name, error_state, bcolors.ENDC))
            sys.exit()
        f.print_field()

        print("{}{}/{} passed movement check{}".format(bcolors.OKGREEN, self.combo.folder, self.combo.name, bcolors.ENDC))
