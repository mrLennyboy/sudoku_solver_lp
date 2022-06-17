# Steps to solve the Sudoku problem:
# Step 1: Define the Linear Programming problem
# Step 2: Set the objective function
# Step 3: Define the decision variables
# Step 4: Set the constraints
# Step 5: Solve the Sudoku puzzle
# Step 6: Check if an optimal result is found
# Step 7: Print the result

# Import PuLP, python linear programming modeller function as alias plp
import pulp as plp

# Step 1: Define the Linear Programming problem (variable to contain problem data)
# Use LpVariable() to create new variables. ie variable 0 <= x <= 3 --> x = LpVariable("x", 0, 3)
sudoku_problem = plp.LpVariable("Sudoku_problem")

# Step 2: Set the objective function
# An objective function is a linear function whose values generally need to be either min or max based on
# the problem to be solved.
# With sudoku there is no solution that is better than another solution, since a sudoku's solution isn't 
# min max'd. The sudoku's solution is defined by it completing the constraints of the problem, 1-9 of row,
# column, and grids. In some cases diagonal to if it is also a diagonal sudoku.
# Set dummy objective
objective = plp.lpSum(0)
sudoku_problem.setObjective(objective)

# Step 3: Define the Linear Programming problem
# Sudoku grid is 9 x 9 grid and consists of 81 cells. Each cell can take a value between 1 - 9.
# Since each cell can only have one value set bool value.
rows = range(0, 9)
cols = range(0, 9)
grids = range(0, 9)
values = range(1, 10)

# Decision Variable/Target Variable
grid_variables = plp.LpVariable.dicts("grid_value", (rows,cols,values), cat = 'Binary')

# Step 4: Set the constraints
# Step 5: Solve the Sudoku puzzle
# Step 6: Check if an optimal result is found
# Step 7: Print the result