#exception handling

#syntax

# try:
#     code
# except:
#     code
# finally:     optional
#     code



a= int(input("Enter a: "))
b = int(input("Enter b: "))

try: 
    print(a/b)
# except:
#     print("Not divisible by 0.")
except Exception as e:
    print(e)