from logic import *

colors = ["red", "green", "blue", "uellow"]
symbols = []

for i in range(len(colors)):
    for color in colors:
        symbols.append(Symbol(f"{color}{i}"))

knowledge = And()   

#Each color has a unique position
for color in colors:
    knowledge.add(Or(
        Symbol(f"{color}0"),
        Symbol(f"{color}1"),
        Symbol(f"{color}2"),
        Symbol(f"{color}3")
    ))
    
# Only one position per color
for color in colors:
    for i in range(len(colors)):
        for j in range(len(colors)):
            if i != j:
                knowledge.add(Implication(Symbol(f"{color}{i}"), Not(Symbol(f"{color}{j}"))))


# only one position per color
for i in range(len(colors)):
    for c1 in colors:
        for c2 in colors:
            if c1 != c2:
                knowledge.add(Implication(Symbol(f"{c1}{i}"), Not(Symbol(f"{c2}{i}"))))

# print(knowledge.formula())

knowledge.add(Not(Symbol("green2")))
knowledge.add(Not(Symbol("yellow3")))
knowledge.add(And(
    Or(Symbol("red0"), Symbol("blue0")),
    Or(Symbol("red1"), Symbol("blue1"))
))

knowledge.add(Symbol("red0"))
# knowledge.add(Symbol("blue1"))

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)
        