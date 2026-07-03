#dictionary collection of key value pairs
# {key:value}, Mutable, ordered, indexed, allows duplicate values but not duplicate keys, heterogeneous

# d= {"name": "sahib", 45: "age", "marks": 23, "pass":True, "roll":23, "name":"ram"}
# print(d)
# print(d["name"])
# print(type(d))
# print(len(d))


# d.update({45:"AGE"})
# print(d)
# d.update({23421:"contact"})
# print(d)
# d["pass"] = False
# print(d)

# d.pop("roll")
# print(d)

# d.get("name")
# print(d.get("name"))

# print(d.keys())
# print(d.values())
# print(d.items())

# for i in d:
#     print(i)  # prints key


d = {}
# for i in range(5):
#     k = input("Enter key: ")
#     v = input("Enter value: ")
#     if v.isdigit():
#         v= int(v)
#     d[k] = v
# print(d)

d["name"] = input("Enter name: ")
d["age"] = int(input("Enter age: "))
d["marks"] = float(input("Enter marks: "))
d["pass"] = bool(input("Enter pass status: "))
print(d)
