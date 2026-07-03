names = ['amit', 'tej', 'sachin', 'rohit']
# for x in names :
#     if 'i' in x:
#         print (x)
#         new_names.append(x)
# print (new_names)

#syntax
# [expression for item in iterable if condition == True]
output = [nam for nam in  names if 'i' in nam]
print(output)