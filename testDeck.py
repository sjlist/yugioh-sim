import deck_analysis as DA
a = DA.Combo_Analyzer(deck_name="World_Chalice_2", \
                      MAX_TRIES=1000, \
                      combo="gumblar_4_undine_wl_1", \
                      time_combos=False, \
                      calculate_chances=True)
a.analyze_combos()
