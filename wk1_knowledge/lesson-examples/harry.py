from logic import *

rain = Symbol("Rain") # it is raining
hagrid = Symbol("Hagrid") # Harry visited Hagrid
dumbledore = Symbol("Dumbledore") # Harry visited Dumbledore

knowledge = And(
    Implication(Not(rain), hagrid),
    Or(hagrid, dumbledore),
    Not(And(hagrid, dumbledore)),
    dumbledore
)

print(model_check(knowledge, rain))

symbols = set(knowledge.symbols())

print(knowledge.formula())
print(symbols)
print(knowledge.symbols())