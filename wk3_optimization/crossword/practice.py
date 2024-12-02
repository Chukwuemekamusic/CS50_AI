variables = {
    "var1": {"words": {"boy", "girl", "broke", "rich"}, "length": 4},
    "var2": {"words": {"boy", "girl", "broke", "rich"}, "length": 3},
    "var3": {"words": {"boy", "girl", "broke", "rich"}, "length": 5}
}

variables = {
    var: {word for word in variables[var]["words"] if variables[var]["length"] == len(word)} for var in variables
}

print(variables)

def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        
        overlap = self.crossword.overlaps.get((x, y))
        if overlap is None:
            return revised
        x1, y1 = overlap
        
        words_to_remove = [
            wordX for wordX in self.domains[x] if not any(wordX[x1] == wordY[y1] for wordY in self.domains[y] if wordX != wordY)
        ]
        
        if words_to_remove:
            for word in words_to_remove:
                self.domains[x].remove(word)
                revised = True
        
        return revised

def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # return set(assignment.keys()) == self.crossword.variables
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True
    
    
def order_domain_values(self, var, assignment):
    """
    Return a list of values in the domain of var, in order by
    the number of values they rule out for neighboring variables.
    The first value in the list, for example, should be the one
    that rules out the fewest values among the neighbors of var.
    """
    neighbors = self.crossword.neighbors(var) - set(assignment)
    
    var_domains = self.domains[var]
    word_counts = {}
    for word in var_domains:
        count = 0
        for neighbor in neighbors:
            count += sum(1 for value in self.domains[neighbor] if value == word )
        word_counts[word] = count

        
    domain_list = sorted(var_domains, key=lambda word: word_counts[word])
    return domain_list
    

def select_unassigned_variable(self, assignment):
    unassigned_var = self.crossword.variables - set(assignment)

    return min(unassigned_var, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))