'''
use learned function to solve diag_sudoku
#constraint propagation
1. Elimination: include single num and twins
2. Only Choice: peers include column row square and diag

#search
Use BFS to iterate the final anwser

'''

rows = 'ABCDEFGHI'
cols = '123456789'
assignments = []


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    pass

#add diagonal_units here to 
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + column_units + square_units + diagonal_units
twins_unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)	
twins_units = dict((s, [u for u in twins_unitlist if s in u]) for s in boxes)
twins_peers = dict((s, set(sum(twins_units[s],[]))-set([s])) for s in boxes)	
	
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    new_grid=[]
    for i in grid:
        if i=='.':
            new_grid.append('123456789')
        elif i in '123456789':
            new_grid.append(i)
    return dict(zip(boxes, new_grid))
    pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')for c in cols))
        if r in 'CF': print(line)
    print
    pass

def eliminate(values):
    #print("-----------------elimate benging---------------------------")
    #display(values)
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values
    pass

def only_choice(values):
    #print("-----------------only benging---------------------------")
    #display(values)
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    pass


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    #print("-----------------twins benging---------------------------")
    #display(values)
    two_values=[]
    twins_values=[]
    same_peers=[]
    for keys in values:
        if len(values[keys])==2:
            two_values.append(keys)
    for v1 in two_values:
    	for v2 in two_values:
	        if v2 in peers[v1]:
	            if values[v2]==values[v1] and (v2,v1) not in twins_values:
	    	        twins_values.append((v1,v2))

    for i in range(len(twins_values)):
        peers1 = peers[twins_values[i][0]]
        peers2 = peers[twins_values[i][1]]
        for peer in peers1:
            if peer in peers2:
                #this is important, because if the elements are less than 2, it will be disappear eventually
                if len(values[peer]) > 2:
                    for element in values[twins_values[i][0]]:
                        values[peer] = values[peer].replace(element, '')
    return values


    
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
	#get the values
    values=grid_values(grid)
	#constraint propagation 
    reduce_puzzle(values)
	
    #search
    return search(values)
	
	#display
    #display(values)
	
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
