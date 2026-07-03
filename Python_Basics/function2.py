# 3). Anonymous Functions lambda

# Syntax of lambda

# lambda arguments : expression 

def multiply(a , b):
    z = a  * b
    print("Multiplication",z)
    return z

multiply(12,35)

multi = lambda x ,y : x * y  # automatically return
print(type(multi))
print(multi(12,51))

var = "Python function"
upper_var = lambda x : x.upper()
print(upper_var(var))

multi_check = lambda x :"Positive" if x > 0 else "Negative" if x < 0 else "Zero"

print(multi_check(21))
print(multi_check(-21))
print(multi_check(0))

# map(function, iterable) --> Transform / modification
# filter(function , iterable) --> filteration

lst = [1,2,3,4,5,6,7]
# double = []
lst_comp = [val*2 for val in lst]
print(lst_comp)

def square(param):
    return param*2

squared = list(map(square, lst))
print(squared)

double = list(map(lambda x : x+x, lst))
print(double)

names = ['john',  'alina', 'amit', 'riya']
to_upper = list(map(lambda x : x.upper(), names))
print(to_upper)

lst = [1,2,3,4,5,6,7]
is_odd = tuple(filter(lambda x : x%2 != 0, lst))
print(is_odd)

values = ['Hello' ,"", "World", "", "ML", ""]
valid_val = list(filter(lambda x : x != '', values))
# valid_val = list(filter(lambda x : len(x)>0, values))
print(valid_val)


lst = ['Hello' ,2, "World", 12, "ML", -3.3]
is_str = list(filter(lambda x : type(x) == str, lst))
print(is_str)

# isinstance()
is_str = list(filter(lambda x : isinstance(x, str), lst))
print(is_str)


is_num = list(filter(lambda x : isinstance(x, (int, float)), lst))
print(is_num)