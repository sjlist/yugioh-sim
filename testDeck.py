import cProfile, pstats, StringIO

pr = cProfile.Profile()
pr.enable()

import deck_analysis as DA
a = DA.Combo_Analyzer("World_Chalice_Undine_Watapon", 1000)
a.analyze_combos()

pr.disable()
s = StringIO.StringIO()
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
