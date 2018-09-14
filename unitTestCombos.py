import os
import pathlib
import UnitTest.ComboTest as CT
import sys

print
for path, subdirs, files in os.walk("./combos/"):
    for name in files:
        p = pathlib.Path(os.path.join(path))
        folder = pathlib.Path(*p.parts[1:])
        print "Next Combo: {}".format(name)
        ct = CT.ComboTest(name.split(".")[0], folder)
        res, _ = ct.testCombo()
        if not res:
            sys.exit()
        print
