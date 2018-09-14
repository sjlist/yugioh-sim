import Combo.Combo as Combo
import Deck.Deck as Deck
import Field.Field as Field
import Common.Common as Common
from Common.Common import bcolors
from itertools import combinations
from copy import deepcopy


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

    def testCombo(self, field=None):
        print("{}Testing {}/{} requirements{}".format(bcolors.OKBLUE, self.combo.folder, self.combo.name, bcolors.ENDC))
        for requirement in self.combo.combo_reqs:
            (result, error_state) = self.testReq(requirement)
            if not result:
                print("{}Failed testing {}/{} on requirement {} with error state {}{}".format(bcolors.FAIL, self.combo.folder, self.combo.name, requirement, error_state, bcolors.ENDC))
                return False, field

        print("{}{}/{} passed requirement check{}".format(bcolors.OKGREEN, self.combo.folder, self.combo.name, bcolors.ENDC))

        deck = Deck.Deck("UnitTest_{}".format(self.combo.name))
        if field is None:
            field = Field.Field(deck)

        for subcombo in self.combo.subcombos:
            if subcombo[0]:
                subcombo_test = ComboTest(subcombo[0], "{}/subcombos".format(self.combo.folder))
                result, res_field = subcombo_test.testCombo(deepcopy(field))
                if result:
                    if subcombo[1] == 'o':
                        print("{}Ignoring field state from {}/{} due to optional subcombo{}".format(bcolors.WARNING, subcombo_test.combo.folder, subcombo_test.combo.name, bcolors.ENDC))
                    if subcombo[1] == 'r':
                        field = res_field
                elif subcombo[1] == 'o':
                    print("{}Failed movement check on {}/{} ignoring due to optional subcombo{}".format(bcolors.WARNING, self.combo.folder, self.combo.name, bcolors.ENDC))
                elif subcombo[1] == 'r':
                    print("{}Failed testing {}/{} on movement check, action {}{}".format(bcolors.FAIL, self.combo.folder, self.combo.name, error_state, bcolors.ENDC))
                    return False, field

        if self.combo.movement != [[]]:
            field.hand = field.hand + Common.dict2List(self.combo.hand)
            field.deck = field.deck + Common.dict2List(self.combo.deck) + Common.dict2List(self.combo.hand_or_deck)
            field.extra = field.extra + Common.dict2List(self.combo.extra)
            field.grave = field.grave + Common.dict2List(self.combo.grave)

            result, error_state = self.combo.playCombo(field)
            if not result:
                print("{}Failed testing {}/{} on movement check, action {}{}".format(bcolors.FAIL, self.combo.folder, self.combo.name, error_state, bcolors.ENDC))
                return False, field

            print("{}{}/{} passed movement check{}".format(bcolors.OKGREEN, self.combo.folder, self.combo.name, bcolors.ENDC))
            return True, field
        else:
            print("{}{}/{} skipped movement check{}".format(bcolors.WARNING, self.combo.folder, self.combo.name, bcolors.ENDC))
            return True, field
