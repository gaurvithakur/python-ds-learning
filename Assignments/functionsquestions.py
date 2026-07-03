# 
# 1. Sum of Digits in a Number
a= int(input("Enter the digits: "))
def sum_of_digit(a):
    s=0
    while a>0:
        digit=a%10
        s+=digit
        a=a//10
    return s
print("Sum of digits:", sum_of_digit(a))


# 2.Count Occurrences of a Character

str = input("Enter the string: ")
char = input("Enter the char: ")
def count_char(str, char):
    c=0
    for i in str:
        if i==char:
            c+=1
    return c
print(count_char(str,char ))



# 3. Generate a List of Prime Numbers.
n = int(input("Enter the integer: "))
def prime_numbers(n):
    primes = []

    for num in range(2, n + 1):
        is_prime = True

        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(num)

    return primes
print("Prime numbers:", prime_numbers(n))


# 4. Implement a Basic Calculator
def calculator(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    else:
        return "Invalid Operator"

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
op = input("Enter operator (+, -, *, /): ")

print("Result:", calculator(a, b, op))




# 5. Check Anagram
a = input("Enter the string1: ")
b = input("Enter the string2: ")

def is_anagram(a, b):
    if len(a) != len(b):
        return False

    for ch in a:
        if a.count(ch) != b.count(ch):
            return False

    return True

print(is_anagram(a, b))

# 6.Find the Second Largest Number in a List
a = list(map(int, input("Enter the numbers separated by space: ").split()))
def second_largest(l):
    l.sort()
    return l[-2]
res = second_largest(a)
print("second largest number of the list: ", res)

# 7. Validate a Password 
password = input("Enter the password: ")

def validate_password(s):
    has_upper = False
    has_lower = False
    has_digit = False

    for ch in s:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True

    return len(s) >= 8 and has_upper and has_lower and has_digit

print(validate_password(password))


#8. Find the GCD of Two Numbers
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Input
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

print("GCD =", gcd(num1, num2))

# 9. Sort Words in Alphabetical Order
def sort_words(sentence):
    words = sentence.split()
    words.sort()
    return words

sentence = input("Enter a sentence: ")
print(sort_words(sentence))