# if, elif, else statements
# Syntax 
# if expression :
#     statement
# else :
#     statement

age = int(input("Enter your age :"))

if age >= 18 : # True False
    print("Eligible for vote !!")  # execute
else :
    print("Not Eligible for vote !!")  # execute

# Short handed if/else
print("Eligible") if age >= 18 else print("Not Eligible")


# if expression :
#     statement
# elif expression 1 :
#     statement
# elif expression 2 :
#     statement
# elif expression 3 :
#     staement
# else :
#     statement

age = int(input("Enter your age :"))
if age >= 1 and age <= 12 :
    print("Child")
elif age >= 13 and age <= 19 :
    print("Teen")
elif age >= 20 and age <= 35 :
    print("Young Adults")
else :
    print("Adult")

a = 7
b = 13
c = 21
# if a > b :
#     print("A is greater to B")
# elif b < c :
#     print("B is smaller to C")
# elif c > a:
#     print("C is greater to A")
# else :
#     print("Else..")


if a > b :
    print("A is greater to B")
if b < c :
    print("B is smaller to C")
if c > a:
    print("C is greater to A")
else :
    print("Else..")


# Nested if/else
# if expression :   # True False
#     statement 
#     if expression :
#         statement 
#     elif expression 1:
#         statement
#     else :
#         statement
# elif expression :
#     statement 
# else :
#     statement

# Army 
# Male / Female 
# 17 - 23
# 18 - 24

gender = input("Enter your gender (M / F)")
age = int(input("Enter your age :"))

if gender == 'M':
    print("-------Male------")
    if age >= 17 and age <= 23 :
        print("Eligible for Army ..")
    else :
        print("Not Eligible")

elif gender == 'F' :
    print("-------Female-----")
    if age >= 18 and age <= 24 :
        print("Eligible for Army ..")
    else :
        print("Not Eligible")

else :
    print("Please Enter a Correct Input !!")