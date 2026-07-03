#set() colllection of unique elements
#unordered, mutable, no indexing, no slicing, {}, heterogeneous data types, allows duplicate values but only one will be stored
# s={1, 4, "hello", 1,3, 45.3, "hello"}
# print(s)
# print(type(s))
# print(len(s))
# s.add(3.14) # add method
# print(s)
# s.remove(1) # remove method
# print(s)
# s.discard(4) # discard method
# print(s)
# s.clear() # clear method
# print(s)
# s.pop()
# print(s)
s={1, 2, 3, 4, 5, 6, 7, 8, 9}
s1= {1,2,3,4,5,6}
s2= {4,5,6,7,8,9}
print(s1.union(s2)) # union method
print(s1.intersection(s2)) # intersection method
print(s1.difference(s2)) # difference method
print(s1.symmetric_difference(s2)) # symmetric difference method

print(s1.issubset(s)) # subset method
print(s.issuperset(s1)) # superset method