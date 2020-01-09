# -----------
# User Instructions:
#
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
#
# Your function should return the expanded grid
# which shows, for each element, the count when
# it was expanded or -1 if the element was never expanded.
# 
# If there is no path from init to goal,
# the function should return the string 'fail'
# ----------

grid = [[0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0]]
heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]

#heuristic = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost,heuristic):
    # ----------------------------------------
    # modify the code below
    # ----------------------------------------
    closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
    closed[init[0]][init[1]] = 1

    expand = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]

    c = init[0]
    r = init[1]
    
    # number of steps taken
    g = 0
    
    # heuristic (distance to goal)
    h = heuristic[r][c]
    
    # f is the amount of steps I've already taken + the heuristic (distance to goal)
    f = g + h

    open = [[f, g, h, r, c]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand
    count = 0
    
    
    
    while not found and not resign:
        
        # if there are no more unexplored open nodes, we've failed
        if len(open) == 0:
            resign = True
            return "Fail"
        
        # sort all nodes based on f metric described above
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            r = next[3]
            c = next[4]
            f = next[0]
            
            # insert number of steps taken into current gridspace
            expand[r][c] = count
            count += 1
            
            # if we're at the goal, we're finished!
            if r == goal[0] and c == goal[1]:
                found = True
                policy[r][c] = '*'
            
            # if we're not at the goal
            else:
                
                # project a potential next state
                for i in range(len(delta)):
                    c2 = c + delta[i][0]
                    r2 = r + delta[i][1]
                    
                    # make sure these are legit states inside the grid, and 
                    # on navigable grid cells (grid == 0), and we haven't visited that 
                    # node already (closed == 0)
                    if r2 >= 0 and r2 < len(grid) and c2 >=0 and c2 < len(grid[0]):
                        if closed[r2][c2] == 0 and grid[r2][c2] == 0:
                            
                            # update heuristic values
                            g2 = g + cost
                            h2 = heuristic[r2][c2]
                            f2 = h2 + g2
                            
                            # add new node to the open list
                            open.append([f2, g2, h2, r2, c2])
                            closed[r2][c2] = 1

    return expand

result = search(grid,init,goal,cost,heuristic)

print("Final path taken")
for i in range(len(result)):
    print(result[i])