# read

with open("abc.txt","r")as f:
    print(f.read())
    f.close()
    # print(f.read())


# write

with open("abc.txt", "w") as f:
    f.write("Welcome to python ds class.")
    f.close()

# append

with open("abc.txt", "a") as f:
    f.write("\n yup yup")

with open("abc.txt","r")as f:
    print(f.read())
    f.close()
    # print(f.read())
