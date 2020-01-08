# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):
    
    closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
    closed[init[0]][init[1]] = 1
    
    expand = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
    action = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
    
    x = init[0]
    y = init[1]
    
    # g is the cost value (here each navigable step is cost 1)
    g = 0
    
    # list of nodes we haven't visited yet
    open_nodes = [[g,x,y]]
    
    found = False # found goal pose
    resign = False # can't navigate any further
    
    count = 0
    while not found and not resign:
        # if there are no more open nodes to explore, we've failed
        if len(open_nodes) == 0:
            resign = True
            print('FAIL')
            path = 'fail'
            
        else:
            # sort the nodes in descending order based on cost and pop the
            # last (smallest) element. that's the next node we want to evaluate
            open_nodes.sort()
            open_nodes.reverse()
            next_node = open_nodes.pop()
            
            x = next_node[1]
            y = next_node[2]
            g = next_node[0]
            
            expand[x][y] = count
            count += 1
            
            
        # if next_node matches the goal, we've succeeded
        if x == goal[0] and y == goal[1]:
            found = True
            path = next_node
            print('SUCCESS')
            print()
            print("Number of steps:", path[0])
            print("Delta x:", path[1])
            print("Delta y:", path[2])
            print()
            
        else:
            # go thru all valid new spaces from current space, and add them
            # to the open_nodes list, provided we haven't already visited them 
            # (not already closed) and that they fall within the grid
            for i in range(len(delta)):
                x2 = x + delta[i][0]
                y2 = y + delta[i][1]
                if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                    if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                        g2 = g + cost
                        open_nodes.append([g2,x2,y2])
                        closed[x2][y2] = 1
                        action[x2][y2] = i
      
    # work backwards and build the "policy" array to visualize the path
    policy = [[' ' for col in range(len(grid[0]))] for row in range (len(grid))]
    x = goal[0]
    y = goal[1]
    policy[x][y] = '*'
    while x != init[0] or y != init[1]:
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        policy[x2][y2] = delta_name[action[x][y]]
        x = x2
        y = y2
        
    print("PATH TAKEN")
    for i in range(len(policy)):
        print(policy[i])
    print()
        
    print("Final grid (numbers represent the order in which nodes were examined)")
    for i in range(len(expand)):
        print(expand[i])
                
    return path

search(grid,init,goal,cost)