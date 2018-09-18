import cPickle as pickle
import Combo.Combo as combo

c = combo.Combo()
c.load("undine_bf_1", "World_Chalice")
pickle.dump(c, open('simple2.pkl', 'w'), protocol=pickle.HIGHEST_PROTOCOL)
t = pickle.load(open("simple2.pkl"))
print t.name