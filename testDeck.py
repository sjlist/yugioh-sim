import deck_analysis as DA
a = DA.Combo_Analyzer(deck_name="World_Chalice_Undine_Watapon", \
                      MAX_TRIES=1000, \
                      combo="", \
                      time_combos=False, \
                      calculate_chances=True)
a.analyze_combos()
