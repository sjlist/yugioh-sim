import Combo.Combo as Combo
import Deck.Deck as Deck
import Field.Field as Field
import Common.Common as Common
import Deck.Card as Card
from Common.Common import bcolors
from itertools import combinations
import cPickle as pickle


class ComboTest:
    def __init__(self, name, folder):
        self.combo = Combo.Combo()
        self.combo.load(name, folder)

    def testReq(self, req):
        req_list = Common.dict2List(req)
        for i in xrange(1, len(req_list) + 1):
            perms = list(combinations(req_list, i))
            for p in perms:
                card_list = Common.list2card(list(p), "COMBO")
                result = self.combo.all_there(req, card_list)
                if result and i < len(req_list):
                    return False, card_list

                if not result and i == len(req_list):
                    return False, card_list

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
            if subcombo[1]:
                subcombo_test = ComboTest(subcombo[1], "{}/subcombos".format(self.combo.folder))
                pickle.dump(field, open('field_temp.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
                result, error_state = subcombo_test.testCombo(field)
                if result:
                    if subcombo[0] == 'o':
                        print("{}Ignoring field state from {}/{} due to optional subcombo{}".format(bcolors.WARNING, subcombo_test.combo.folder, subcombo_test.combo.name, bcolors.ENDC))
                        field = pickle.load(open("field_temp.pkl"))
                    else:
                        field = error_state
                elif subcombo[0] == 'o':
                    print("{}Failed movement check on {}/{} ignoring due to optional subcombo{}".format(bcolors.WARNING, self.combo.folder, self.combo.name, bcolors.ENDC))
                elif subcombo[0] == 'r':
                    print("{}Failed testing {}/{} on movement check, action {}{}".format(bcolors.FAIL, self.combo.folder, self.combo.name, error_state, bcolors.ENDC))
                    return False, field

        field.hand = Common.dict2card(self.combo.hand, "COMBO") + field.hand
        field.deck = field.deck + Common.dict2card(self.combo.deck, "COMBO") + Common.dict2card(self.combo.hand_or_deck, "COMBO")
        field.extra = field.extra + Common.dict2card(self.combo.extra, "COMBO")
        field.grave = field.grave + Common.dict2card(self.combo.grave, "COMBO")

        if self.combo.movement != [[]]:
            result, error_state = self.combo.play_combo(field)
            if not result:
                print("{}Failed testing {}/{} on movement check, action {}{}".format(bcolors.FAIL, self.combo.folder, self.combo.name, error_state, bcolors.ENDC))
                return False, field

            print("{}{}/{} passed movement check{}".format(bcolors.OKGREEN, self.combo.folder, self.combo.name, bcolors.ENDC))
            return True, field
        else:
            print("{}{}/{} skipped movement check{}".format(bcolors.WARNING, self.combo.folder, self.combo.name, bcolors.ENDC))
            return True, field
