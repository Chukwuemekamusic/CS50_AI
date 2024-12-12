piles = [1,3]

for i, pile in enumerate(piles):
    for j in range(1, pile + 1):
        print(i, j)
    print()
    
tuple_piles = (piles[0], piles[1])

my_dict = {
    ((1,2),(2)): 4,
    ((1,2),(3)): 5,
    ((2,4),(3)): 7,
    ((1,2),(5)): 0,
}

max_q = max([value for key, value in my_dict.items() if key[0] == (5,2)], default=0)
print(max_q)