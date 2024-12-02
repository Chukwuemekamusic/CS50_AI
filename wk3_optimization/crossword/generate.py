import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        self.domains = {
            var: {word for word in self.domains[var] if var.length == len(word) } for var in self.crossword.variables
        }
        

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
        consistent_values = {
            wordX for wordX in self.domains[x]
            if len(wordX) > x1 and  # Check length of wordX
            any(
            len(wordY) > y1 and wordX[x1] == wordY[y1]  # Check length of wordY
            for wordY in self.domains[y]
            if wordX != wordY
        )
    }
        
        # update domain of x if needed
        if consistent_values != self.domains[x]:
            self.domains[x] = consistent_values
            revised = True
        
        return revised
            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # arcs = set()
            # for var in self.crossword.variables:
            #     neighbors = self.crossword.neighbors(var)
            #     arcs.update((var, a) for a in neighbors)
            arcs = {
                (var, neighbor) for var in self.crossword.variables 
                for neighbor in self.crossword.neighbors(var)
            }
            
        while arcs:
            (x, y) = arcs.pop()
            
            if self.revise(x,y):
                if len(self.domains[x]) == 0: return False
                neighbors = self.crossword.neighbors(x)
                for neighbor in neighbors - {y}:
                    arcs.add((neighbor, x))
       
        return True
        
     # variables = {
        # v1 = Variable(0, 0, "across", 3)  # CAT
        # v2 = Variable(0, 0, "down", 3)    # COW
        # v3 = Variable(0, 2, "down", 4)    # TREE
        # # }
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(var in assignment for var in self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        words = {}
        
        for var, word in assignment.items():
            # length correct
            if var.length != len(word):
                return False
            
            # values distinct
            if word in words:
                return False
            words[word] = True
            
            # no conflict with neighbors
            neighbors =  self.crossword.neighbors(var)
            for neighbor in neighbors:
                if neighbor in assignment:
                    overlap = self.crossword.overlaps.get((var, neighbor))
                    if overlap is not None:
                        i, j = overlap
                        if word[i] != assignment[neighbor][j]:
                            return False
       
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, ordered by
        least-constraining values heuristic (fewest conflicts first).
        """
        # Get unassigned neighbors
        neighbors = self.crossword.neighbors(var) - set(assignment)
        
        # Calculate how many values each word rules out
        word_counts = {}
        for word in self.domains[var]:
            eliminated = 0
            for neighbor in neighbors:
                if overlap := self.crossword.overlaps.get((var, neighbor)):
                    i, j = overlap
                    # Count how many words in neighbor's domain would be eliminated
                    eliminated += sum(1 for n_word in self.domains[neighbor] 
                                    if word[i] != n_word[j])
            word_counts[word] = eliminated
        
        # Return words sorted by how many values they eliminate (ascending)
        return sorted(self.domains[var], 
                    key=lambda word: (word_counts[word], word))  # Added word as secondary sort
        
 
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_var = self.crossword.variables - set(assignment)
        
        minimum_value = min(len(self.domains[var]) for var in unassigned_var)
        candidates = [var for var in unassigned_var if len(self.domains[var]) == minimum_value]
        
        if len(candidates) == 1:
            return candidates[0]
        
        maximum_degree = max(len(self.crossword.neighbors(var)) for var in candidates)
        return next(var for var in candidates if len(self.crossword.neighbors(var)) == maximum_degree)
            
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment) 
        var_list = self.order_domain_values(var, assignment)
        for value in var_list:
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
