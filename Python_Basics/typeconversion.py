# basic conversion
a= 5
print(type(a))
print(float(a))
print(int(a))


# string to number
b = "234" 
print(int(b))
sq_b = int(b)**2
print(sq_b)


# Mix and Match
c = "3.14"
print(float(c))
d= 98
print(str(d))
e= True
print(int(e))
f = "Hello"
print(bool(f))


# TypeError Practice:
input1= input("Enter first number : ")
input2= int(float(input1))
print(input2)


# //////input function ///

# basic input
user_name = input("Enter your name : ")
age = input("Enter your age : ")
print("Hello"+ " " + user_name +"!" + " " +"You are "+ age + " " + "years old.")

# sum of numbers
num1 = int(input("Enter first number : "))
num2 = int(input("Enter second number : "))
sum = num1 +num2
print(sum)
print("The sum of the two numbers is : " + str(sum) )

# Type-Casting in Input:
num1 = input("Enter first number : ")
num2 = input("Enter second number : ")
num11 = int(num1)
num22 = int(num2)
pro= num11 * num22
print("The product of the two numbers is : " + str(pro) )
print(pro)

# Custom Conversion
temincel = float(input("Enter temperature in Celsius : "))
teminfah = (temincel * 9/5) + 32
print("Temperature in Fahrenheit is : " + str(teminfah) )
print(teminfah)




# ///// operators practice questions //////

a= float(input("Enter first number : "))
b = float(input("Enter second number : "))
print("The sum of the two numbers is : " + str(a+b) )
print("The difference of the two numbers is : " + str(a-b) )
print("The product of the two numbers is : " + str(a*b) )
print("The quotient of the two numbers is : " + str(a/b) )
print("The floor division of the two numbers is : " + str(a//b) )
print("The modulus of the two numbers is : " + str(a%b) )
print("The exponentiation of the two numbers is : " + str(a**b) )

print(a > b) # Greater than
print(a < b) # Less than
print(a >= b) # Greater than or equal to
print(a <= b) # Less than or equal to
print(a == b) # Equal to
print(a != b) # Not equal to

print(a > 0 and b > 0) # Logical AND
print(a > 0 or b > 0) # Logical OR
print(not a) # Logical NOT

num = 10
print("Initial value of num : " + str(num))    
num += 5 # num = num + 5
print("After addition : " + str(num))
num -= 3 # num = num - 3
print("After subtraction : " + str(num))
num *= 2 # num = num * 2
print("After multiplication : " + str(num))
num /= 4 # num = num / 4
print("After division : " + str(num))

# odd even check

input_num = int(input("Enter a number : "))
if input_num %2 ==0:
    print(str(input_num) + " is an even number.")
else:    print(str(input_num) + " is an odd number.")
