from Common.Common import string2TupleList

d = [['1', '2', '3', '1'], ['4', '5', '6'], ['7', '8', '9'], ['10', '11', '12']]
ds = str(d)
a = string2TupleList(ds)
print d
print a
print a == d
