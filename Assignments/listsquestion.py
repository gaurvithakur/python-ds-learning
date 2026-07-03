# Basic Practice Questions
# 1.
a=list(range(1,11))
print("List of the first 10 natural numbers: ",a)

# 2
b= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
len= 0
for i in b:
    len+=1
print("Length of list: ",len) 

# 3.
lst = [10, 20, 30, 40, 50]

if 25 in lst:
    print("Number found")
else:
    print("Number not found")


# 4.
lst = [1, 2, 3, 4, 5]
rev = lst[::-1]
print(rev)

# ALTERNATE 
lst = [1, 2, 3, 4, 5]
rev = []

for i in range(len(lst)-1, -1, -1):
    rev.append(lst[i])

print(rev)


# 5.
list = [1, 3, 3, 5, 3, 7, 3]
count= 0
print(list)
for i in  list:
    if i==3:
        count+=1
print(count)

# 6.
lst = []
for i in range(1,11):
    lst.append(i**2)
print(lst)


# Intermediate Practice Questions
# 7.
lst = [1, 5, 2, 3, 4, 5, 5, 3, 1, 22, 3, 5 ,4]
lst =[ x for x in lst if x!=5]
print(lst)

# 8.
lst = [1, 2, 3, 4, 5, 6]
mid = len(lst)/2
first_lst= lst[:mid]
sec_lst= lst[mid:]

# 9.
lst = [1, 2, 3, 4, 5]
lst =[ x**2 for x in lst]
print(lst)

# 10.
# lst = [1, 3, 7, 8, 7, 10]
# for i in lst:
#     if i==7:
#         lst.remove(i)

# print(lst.index(1))

lst = [1, 3, 7, 8, 7, 10]

first = lst.index(7)
second = lst.index(7, first + 1)

print(second)



# 11.
lst = [5, 3, 8, 6, 1]

for x in range(len(lst)):
    for y in range(len(lst) - 1 - x):
        if lst[y] > lst[y + 1]:
            temp = lst[y]
            lst[y] = lst[y + 1]
            lst[y + 1] = temp

print(lst)



# Advanced Practice Questions
# 12.
nested = [[1, 2], [3, 4], [5]]

flat = []

for sublist in nested:
    for item in sublist:
        flat.append(item)

print(flat)



# 13.
lst = [1, 2, 3, 2, 4, 1, 5]
result =[]
for x in lst:
    if x not in result:
        result.append(x)
print(result)


# 14.
lst1 = ['hello', 'o7']
lst2 =['world', 'services']

final= []

for x in lst1:
    for y in lst2:
        result.append(x+ " "+y)
print(result)