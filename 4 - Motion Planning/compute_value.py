# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def compute_value(grid,goal,cost):
    value = [[99 for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [['X' for col in range(len(grid[0]))] for row in range(len(grid))]
    
    change = True
    
    while change:
        change = False
        
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                
                # set goal value to 0 and iterate again
                if goal[0] == r and goal[1] == c:
                    if value[r][c] > 0:
                        value[r][c] = 0
                        policy[r][c] = '*'
                        change = True
                
                # if we're not at a goal cell
                elif grid[r][c] == 0:
                    
                    # project a potential next state
                    for a in range(len(delta)):
                        r2 = r + delta[a][0]
                        c2 = c + delta[a][1]
                        
                        # make sure these are legit states inside the grid and 
                        # on navigable grid cells (==0)
                        if (r2 >= 0 and r2 < len(grid) and c2 >= 0 and c2 < len(grid[0])
                            and grid[r2][c2] == 0):
                            
                                # compute the new cost
                                v2 = value[r2][c2] + cost
                                
                                # if the new cost is less than the current cost,
                                # replace that in the value grid and iterate again.
                                # also update the policy grid to show the move
                                # you just made
                                if v2 < value[r][c]:
                                    change = True
                                    value[r][c] = v2
                                    policy[r][c] = delta_name[a]                                 
    
    print("Policy Map:")
    for p in policy:
        print(p)
    print()
    
    return value 

test = compute_value(grid,goal,cost)

print("Value Map:")
for row in test:
    print(row)