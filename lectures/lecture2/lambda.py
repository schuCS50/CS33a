people = [
    {"name": "Harry", "house": "G"},
    {"name": "Cho", "house": "R"},
    {"name": "Draco", "house": "S"}
]

def f(person):
    return person["name"]

people.sort(key=lambda person: person["name"])
#Lambda input: output

print(people)