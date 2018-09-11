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
                    return (False , list(p))

                if not result and i == len(req_list):
                    return (False, list(p))

        return (True, [])

    def testCombo(self):
        for requirement in self.combo.combo_reqs:
            (result, error_state) = self.testReq(requirement)
            if not result:
                print("Failed testing {}/{} on requirement {} with error state {}".format(self.combo.folder, self.combo.name, requirement, error_state))
                sys.exit()

        #TODO add movement tests, that at least the actions are all legal

        print("{}/{} passed".format(self.combo.folder, self.combo.name))
