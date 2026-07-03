# 1. Write a Python Program that take two string input `s1` and `s2` from user, and return a string
# containing the appear in both string.
s1= input("Enter s1: ")
s2= input("Enter s2: ")
string = ""
for i in s1 :
    for j in s2 :
        if i==j:
            string+=i
            break
print(string)


# 2.Write a Python Program that takes sentence as a input and returns the numbers of word in sentence. Words are separated by spaces.

sen = input("Enter sentence: ")
count = 1
for i in sen :
    if i ==" " :
        count+=1
        
print("Total count: ", count)



# Alternative method
sen2 = input("Enter sentence: ")
words = sen2.split( )
print("Number of words: ", len(words))

# 3. Write a python program that checks if two strings `s1` and `s2` are rotations of each other.
s1 = input("Enter the first string: ")
s2 = input("Enter the second string: ")

if len(s1)==len(s2) and s2 in (s1 +s2): 
    print("true")
else:
    print("false")

# ALTERNATE METHOD
s1 = input("Enter the first string: ")
s2 = input("Enter the second string: ")


if len(s1) == len(s2):
    for i in range(len(s1)):
        rotation = s1[i:] + s1[:i]

        if rotation == s2:
            flag = True
            break
        else:
            flag = False
print(flag)


# 4. Write a Python Program that takes a string as input and returns the character that appears most frequently. If there are multiple characters with the same maximum frequency, return any one of them.
s= input("Enter the string: ")
count_max= 0
ch = ""

for i in s:
    count=0
    for j in s:
        if i==j:
            count+=1
    if count_max<count:
        count_max=count
        ch=i

print("The character that appears most frequently: ",ch)
print("The maximum frequency: ", count_max)


# 5. Write a Python Program that converts a string from snake_case to CamelCase.
s = input("Enter snake_case string: ")

words = s.split("_")

camel = ""

for word in words:
    camel += word.capitalize()

print(camel)

# Basic Question
# 1.
string= input("Enter the string: ")
print(len(string))   #length
print(string[0])      #first character
print(string[-1])     #last character
rev = ""
for i in string:
    rev = i + rev
print("The string in reverse order: ", rev)

# 2.
a= input("Enter the string: ")
b = a.isdigit()
print(b)


# 3.
c = input("Enter the string: ")
count = 0

for i in c:
    if i == "a":
        count += 1
    elif i == "e":
        count += 1
    elif i == "i":
        count += 1
    elif i == "o":
        count += 1
    elif i == "u":
        count += 1

print("The number of vowels:", count)


# 4.
d = input("Enter the string: ")
char = input("Enter the character to count: ")

ch = d.count(char)

print("The number of occurrences of a given character in a string:", ch)


# INTERMEDIATE QUESTION
# 5.
g= input("Enter the string: ")
old = input("Enter the substring: ")
new = input("Enter the substring: ")
result = g.replace(old, new)
print("The new string: ", result)

# 6. 
j = input("Enter the string: ")
print(j.upper())
print(j.lower())
print(j.title())

# 7. 
s1 = input("Enter the string1: ")
s2 = input("Enter the string2: ")

flag = True

if len(s1) == len(s2):
    for i in s1:
        if s1.count(i) != s2.count(i):
            flag = False
            break
else:
    flag = False

if flag:
    print("Strings are anagrams")
else:
    print("Strings are not anagrams")


k = input("Enter the string: ")

if k == k[::-1]:
    print("It is a palindrome.")
else:
    print("It is not a palindrome.")