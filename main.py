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
# Add generic constraints to solve the sudoku problem. 
# Constraint 1: Each cell should be filled with a single value between 1 and 9.
# Constraint 2: Each row should contain every number from 1 to 9 once.
# Constraint 3: Each col should contain every number from 1 to 9 once.
# Constraint 4: Each 3 x 3 grid should contain every number from 1 to 9 once.

# Constraint 1: Each cell should be filled with a single value between 1 and 9.
for row in rows:
  for col in cols:
    sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][col][value] for value in values]),
    sense=plp.LpConstraintEQ, rhs=1, name=f"constraint_sum_{row}_{col}"))

# Constraint 2: Each row should contain every number from 1 to 9 once.
for row in rows:
  for value in values:
    sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][col][value]*value for col in cols]),
    sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_row_{row}_{value}"))

# Constraint 3: Each col should contain every number from 1 to 9 once.
for col in cols:
  for value in values:
    sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][col][value]*value for row in rows]),
    sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_col_{col}_{value}"))

# Constraint 4: Each 3 x 3 grid should contain every number from 1 to 9 once.
for grid in grids:
  grid_row  = int(grid/3)
  grid_col  = int(grid%3)

  for value in values:
    sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[grid_row*3+row][grid_col*3+col][value]*value for col in range(0,3) for row in range(0,3)]),
    sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_grid_{grid}_{value}"))

# Constraint 5: An additional constraint for diagonal should contain every number from 1 to 9 once.
# Constraint from top-left to bottom-right
for value in values:
  sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][row][value]*value  for row in rows]),
  sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_diag1_{value}"))

# Constraint from top-right to bottom-left
for value in values:
  sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][len(rows)-row-1][value]*value  for row in rows]),
  sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_diag2_{value}"))

# Constraint to initialize the input Sudoku puzzle, add prefilled values as constraints
for row in rows:
  for col in cols:
    if(input_sudoku[row][col] != 0):
      sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][col][value]*value  for value in values]),
      sense=plp.LpConstraintEQ, 
      rhs=input_sudoku[row][col], 
      name=f"constraint_prefilled_{row}_{col}"))

# Step 5: Solve the Sudoku puzzle
# Step 6: Check if an optimal result is found
# Step 7: Print the result