Pass = {}
with open("login.txt") as file:
    for line in file:
        key, value = line.split()
        Pass[key] = value
