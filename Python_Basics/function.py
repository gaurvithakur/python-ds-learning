# types of functions
# 1. pre define functions
# 2. user defined functions
# 3. Anonymous functions

#  syntax of user function
#  def function_name(params1, params2, params3 ) :
#  statement of function/ logic
#  return statement
#  pass

# function_name(agrument1, argument2, argument3)

# Type of argument

def hello() :
    print("Welcome to Python class.")
hello()


def even_odd(num) :
    if num%2 == 0 :
        print("num is even")
    else :
        print("num is odd")
even_odd(233)

# 4. arbitary arguments *args and *kwargs


def total_sales(*args) :
    print(type(args))

total_sales()

def employee(**kwargs) :
    print(type(kwargs))

employee()