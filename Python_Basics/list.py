# Datatype list 
""" [], Hetrogeneous , muttable (that can be change), ordered , 
indexed (slicing) , allow duplicates values"""

lst = ['Hello', 345, -34.1111, False, 0, True, "Hello", 1]
print(type(lst))
print(lst)

print(lst[1])
print(lst[-4])
print(len(lst))
# print(lst[8])
print(lst[:10])
print(lst[10:])
print(lst[-5:-1])
print(lst[-2:-6:-1])

lst = ['Hello', 345, -34.1111, False, 0, True, "Hello", 1]
for x in lst :
    # print(x)
    if x == 1:  # True
        break
    print(x)

# print(1 == True)

print("Hello" in lst)

lst1 = ["aman", 21, 'ravi', 35, 'yuvraj', 27, 'priya', 25]
# Methods of list 
# append(ele)
lst1.append("tushar")
print(lst1)
# lst1.append(1100,21)  # error only single element

# insert()
lst1.insert(3, "apple")
print(lst1)
lst1.insert(0,"World")
print(lst1)

# extend() +
# lst1 = ['a','b','c','d']
# lst2 = [1,2,3,4]
# lst1.extend(lst2)
# print(lst1)
# lst2.extend(lst1)
# print(lst2)

# remove()
print(lst1)
lst1.remove("ravi")
print(lst1)

# Question
lst = ['a','b','c','a','a','d','e']
# lst.remove('ab')  # gives error if element if not present in list.
# print(lst)
# for x in lst :
#     # print(x)
#     if x == 'a':
#         print(f"{x} found !!")
#         lst.remove(x)
# print(lst)

# pop()
pop_value = lst.pop(3) # default -1
print(pop_value)
print(lst)

# clear()
# lst.clear()
# print(lst)

# copy()
my_copy = lst.copy()
print(my_copy)

# counts()
print(lst.count('ab'))

# index()
print(lst.index('a'))

lst  = [100,120,20,70,5,0,10]
lst  = ['b','e','z','a']
lst.sort(reverse=True)
print(lst)