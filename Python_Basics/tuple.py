# tuple is a collection of items that are immutable
# indexed, ordered, allows duplicate values, heterogeneous data types, immutable, ()
tu=(23, False, "sahil", 23, 3.14, False, "bye")
print(tu)
print(type(tu))
print(tu[0]) # indexing
print(tu.count(23)) # count method
print(tu.index("sahil")) # index method
print(tu[1:5]) # slicing    

for i in tu: # looping through tuple
    print(i)

for i in range(len(tu)):
    print(tu[i])

    for i in tu:
        if type(i) == int or type(i) == float:
            print(i)