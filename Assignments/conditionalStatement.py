# Write a program that asks the user to input a number and then the month name corresponding to that number.

month_no = int(input("Enter the month number: "))

if month_no == 1:
    print("The month name is January.")
elif month_no == 2:
    print("The month name is February.")
elif month_no == 3:
    print("The month name is March.")
elif month_no == 4:
    print("The month name is April.")
elif month_no == 5:
    print("The month name is May.")
elif month_no == 6:
    print("The month name is June.")
elif month_no == 7:
    print("The month name is July.")
elif month_no == 8:
    print("The month name is August.")
elif month_no == 9:
    print("The month name is September.")
elif month_no == 10:
    print("The month name is October.")
elif month_no == 11:
    print("The month name is November.")
elif month_no == 12:
    print("The month name is December.")
else:
    print("Invalid month number! Please enter a number between 1 and 12.")

# 2.  Write a program Ask user to input 2 numbers.
# Tell the followings
#1. Are both numbers equal or not
a= int(input("Enter first number: "))
b= int(input("Enter second number:"))
if a==b:
    print("Both numbers are equal. ")
else :
    print("Both number are not equal.")
#2. Which is Bigger in both
if a>b:
    print("first number is bigger.")
else :
    print("second number is bigger.")
# 3. Either the first number is smaller or equal to the second number
if a <= b:
    print("The first number is smaller than or equal to the second number.")
else:
    print("The first number is greater than the second number.")
#4. Print your first name 5 times if the first number is greater than the second and print your surname 3 times if the 1st number is less than the second.
if a<b :
    for i in range(5):
        print("Gaurvi")
else :
    for i in range(3):
        print("Thakur")