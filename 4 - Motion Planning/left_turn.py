# You are given a car in grid with initial state
# init. Your task is to compute and return the car's
# optimal path to the position specified in goal;
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a
# right turn.

forward = [[-1,  0],  # go up
           [0, -1],  # go left
           [1,  0],  # go down
           [0,  1]]  # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0]  # given in the form [row,col,direction]
# direction = 0: up
#             1: left
#             2: down
#             3: right

goal = [2, 0]  # given in the form [row,col]

cost = [2, 1, 20]  # cost has 3 values, corresponding to making
# a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------


def optimum_policy2D(grid, init, goal, cost):
  value = [[[999 for col in range(len(grid[0]))] for row in range(len(grid))],
           [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
           [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
           [[999 for col in range(len(grid[0]))] for row in range(len(grid))]]

  policy = [[[' ' for col in range(len(grid[0]))] for row in range(len(grid))],
           [[' ' for col in range(len(grid[0]))] for row in range(len(grid))],
           [[' ' for col in range(len(grid[0]))] for row in range(len(grid))],
           [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]]

  policy2D = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]

  change = True

  while change:
    change = False
    
    for r in range(len(grid)):
      for c in range(len(grid[r])):
        for orientation in range(4):
            
            # if we're at the goal
            if goal[0] == r and goal[1] == c:
              if value[orientation][r][c] > 0:
                value[orientation][r][c] = 0
                policy[orientation][r][c] = '*'
                change = True
                
            # if we're at a navigable space 
            elif grid[r][c] == 0:
                # try each orientation
                for i in range(len(action)):
                    o2 = (orientation + action[i]) % 4
                    r2 = r + forward[o2][0]
                    c2 = c + forward[o2][1]
                    
                    # valid gridspace
                    if r2 >= 0 and r2 < len(grid) and c2 >= 0 and c2 < len(grid[0]) and grid[r2][c2] == 0:
                       
                        # if value is less than current value, update value and policy grids
                        v2 = value[o2][r2][c2] + cost[i]
                        if v2 < value[orientation][r][c]:
                          policy[orientation][r][c] = action_name[i]
                          value[orientation][r][c] = v2
                          change = True

  r = init[0]
  c = init[1]
  
  # orientation (either up, left, down, or right)
  o = init[2]
  
  # build 2D version of policy (each layer is an orientation)
  policy2D[r][c] = policy[o][r][c]
  
  while policy[o][r][c] != '*':
    
    # heading forward --> no change needed in orientation
    if policy[o][r][c] == '#':
        o = o
    
    # turn right
    elif policy[o][r][c] == 'R':
        o = (o - 1) % 4
        
    # turn left
    elif policy[o][r][c] == 'L':
        o = (o + 1) % 4
        
    r = r + forward[o][0]
    c = c + forward[o][1]

    policy2D[r][c] = policy[o][r][c]

  return policy2D


print("Optimal Policy:")
p = optimum_policy2D(grid, init, goal, cost)
for i in p:
  print(i)