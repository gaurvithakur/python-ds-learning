# 1.
a = ['a', 'b', 'c']
b = ['d', 'e', 'f']

d = dict(zip(a, b))

result = []

for key, value in d.items():
    result.append(key + value)

print(result)

# 2.
colors = ["Black", "Red", "Maroon", "Yellow"]
codes = ["#000000", "#FF0000", "#800000", "#FFFF00"]

result = []

for i in range(len(colors)):
    d = {
        "color_name": colors[i],
        "color_code": codes[i]
    }
    result.append(d)

print(result)

# 3.
d = {'eng': 100, 'hindi': 20, 'social': 45, 'punjabi': 85}

l = list(d.items())
l.sort(key=lambda x: x[1], reverse=True)

print("The subject with second highest marks:", l[1][0])