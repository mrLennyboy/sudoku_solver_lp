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

# wrap loops for diagonal constraints within a functions
def add_default_sudoku_constraints(sudoku_problem, grid_variables, rows, cols, grids, values):
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

# wrap loops for diagonal constraints within a functions
def add_diagonal_sudoku_constraints(sudoku_problem, grid_variables, rows, cols, values):
  # Constraint 5: An additional constraint for diagonal should contain every number from 1 to 9 once.
  # Constraint from top-left to bottom-right
  for value in values:
    sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][row][value]*value  for row in rows]),
    sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_diag1_{value}"))

  # Constraint from top-right to bottom-left
  for value in values:
    sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][len(rows)-row-1][value]*value  for row in rows]),
    sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_diag2_{value}"))

# wrap loops for diagonal constraints within a functions
def add_prefilled_constraints(sudoku_problem, input_sudoku, grid_variables, rows, cols, values):
  # Constraint to initialize the input Sudoku puzzle, add prefilled values as constraints
  for row in rows:
    for col in cols:
      if(input_sudoku[row][col] != 0):
        sudoku_problem.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_variables[row][col][value]*value  for value in values]),
        sense=plp.LpConstraintEQ, 
        rhs=input_sudoku[row][col], 
        name=f"constraint_prefilled_{row}_{col}"))

# wrap in function
def extract_solution(grid_variables, rows, cols, values):
  # Code to extract the final solution grid
  solution = [[0 for col in cols] for row in rows]
  grid_list = []
  for row in rows:
    for col in cols:
      for value in values:
        if plp.value(grid_variables[row][col][value]):
          solution[row][col] = value
  return solution

# wrap in function
def print_solution(solution, rows, cols):
  # Step 7: Print the result
  # Print the final solution as a grid
  print(f"\nFinal result:")

  print("\n\n+ ----------- + ----------- + ----------- +",end="")
  for row in rows:
    print("\n",end="\n|  ")
    for col in cols:
      num_end = "  |  " if ((col+1)%3 == 0) else "   "
      print(solution[row][col],end=num_end)

    if ((row+1)%3 == 0):
      print("\n\n+ ----------- + ----------- + ----------- +\n",end="")


def solve_sudoku(input_sudoku, diagonal = False):
  # Step 1: Define the Linear Programming problem (variable to contain problem data)
  # create new variables
  sudoku_problem = plp.LpProblem("Sudoku_problem_solver")

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

  # Create the default constraints to solve sudoku
  add_default_sudoku_constraints(sudoku_problem, grid_variables, rows, cols, grids, values)

  # Add the diagonal constraints if flag is set
  if diagonal:
    add_diagonal_sudoku_constraints(sudoku_problem, grid_variables, rows, cols, values)

  # Constraint to initialize the input Sudoku puzzle, add prefilled values as constraints
  add_prefilled_constraints(sudoku_problem, input_sudoku, grid_variables, rows, cols, values)

  # Step 5: Solve the Sudoku puzzle
  # After the Objective function, decision variables, and constraints are set the sudoku solver can be invoked
  # Write to file instead of terminal
  sudoku_problem.solve(plp.PULP_CBC_CMD(logPath=r'path.lp'))

  # Step 6: Check if an optimal result is found
  solution_status = plp.LpStatus[sudoku_problem.status]
  print(f'Solution Status = {solution_status}')

  # extract the solution if an optimal solution has been identified
  if solution_status == 'Optimal':
    solution = extract_solution(grid_variables, rows, cols, values)
    print_solution(solution, rows, cols)

'''
normal_sudoku = [
                    [3,0,0,8,0,0,0,0,1],
                    [0,0,0,0,0,2,0,0,0],
                    [0,4,1,5,0,0,8,3,0],
                    [0,2,0,0,0,1,0,0,0],
                    [8,5,0,4,0,3,0,1,7],
                    [0,0,0,7,0,0,0,2,0],
                    [0,8,5,0,0,9,7,4,0],
                    [0,0,0,1,0,0,0,0,0],
                    [9,0,0,0,0,7,0,0,6]
                ]

solve_sudoku(input_sudoku=normal_sudoku, diagonal=False)
'''
diagonal_sudoku = [
                    [0,3,0,2,7,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [8,0,0,0,0,0,0,0,0],
                    [5,1,0,0,0,0,0,8,4],
                    [4,0,0,5,9,0,0,7,0],
                    [2,9,0,0,0,0,0,1,0],
                    [0,0,0,0,0,0,1,0,5],
                    [0,0,6,3,0,8,0,0,7],
                    [0,0,0,0,0,0,3,0,0]
                ]
solve_sudoku(input_sudoku=diagonal_sudoku, diagonal=True)