import itertools

def powerset(s):
    s = list(s)
    result = []
    
    # First, create all combinations for each length
    all_combinations = []
    for r in range(len(s) + 1):
        combinations_of_length_r = itertools.combinations(s, r)
        all_combinations.append(combinations_of_length_r)
    
    # Chain/flatten all combinations into one sequence
    flattened_combinations = itertools.chain.from_iterable(all_combinations)
    
    # Convert each combination to a set and add to result
    for combination in flattened_combinations:
        result.append(set(combination))
    
    return result

people = {
    'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None}, 
    'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True}, 
    'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}}

for person, values in people.items():
    print(f"{person}'s mother is: {values['mother']}")
    

names = set(people) # set of the keys
result = powerset(people)

print('names', names)
print('result', result)
print('people', people)


PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    }}

print(PROBS['gene'].values())
