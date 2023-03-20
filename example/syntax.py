# das ist ein Kommentar

a: int = 1

b
b = 2

if a == 1:
    print("a ist 1")

# while a == 1:   # wiederholt sich bis a nicht mehr 1 ist
#     ...
#
#     if b == 1:
#         break   # unterbricht die schleife sofort

for c in ["hi", 5, "banana"]:   # iteriert ueber die Werte der Liste
    print(c)    # gibt den Wert der Variable c aus

def to_string(arg: int) -> str:
    return str(arg)