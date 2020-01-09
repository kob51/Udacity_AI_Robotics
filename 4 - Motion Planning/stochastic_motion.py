delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.


def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    
    
    change = True
    while change:
        change = False
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if goal[0] == r and goal[1] == c:
                    if value[r][c] > 0:
                        value[r][c] = 0
                        policy[r][c] = '*'
                        change = True
                        
                elif grid[r][c] == 0:
                    
                    # try each movement (up,left,down,right)
                    for a in range(len(delta)):
                        v2 = cost_step


                        # explore different action outcomes. there are 3 total:
                        # the desired one and the two undesired ones. as an example
                        # if you want to move forward, if i is zero that is the desired one,
                        # but there is also a chance of moving to either side instead
                        for i in range(-1, 2):
                            a2 = (a + i) % len(delta)
                            r2 = r + delta[a2][0]
                            c2 = c + delta[a2][1]
                            if i == 0:
                                p2 = success_prob
                            else: 
                                p2 = failure_prob
                            
                            # if we're moving to a valid space, add the expected value of the next
                            # space to the current value
                            if 0 <= r2 < len(grid) and 0 <= c2 < len(grid[0]) and grid[r2][c2] == 0:
                                v2 += p2 * value[r2][c2]
                                
                            # if we're moving to an invalid space, add the expeced value
                            # of the collision to the current value
                            else:
                                v2 += p2 * collision_cost

                        if v2 < value[r][c]:
                            change = True
                            value[r][c] = v2
                            policy[r][c] = delta_name[a]

    return value, policy



grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 1000
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)

print("Value Map:")
for row in value:
    print(row)
    
print()
print("Optimal Policy Grid:")
for row in policy:
    print(row)

# Expected outputs:
#
#[471.9397246855924, 274.85364957758316, 161.5599867065471, 0],
#[334.05159958720344, 230.9574434590965, 183.69314862430264, 176.69517762501977], 
#[398.3517867450282, 277.5898270101976, 246.09263437756917, 335.3944132514738], 
#[700.1758933725141, 1000, 1000, 668.697206625737]

#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']

print()
print("Expected policy doesn't lead to goal b/c of high cost associated with failing along the boundaries")
print("Reduce collision cost or increase success probability to see a better optimal policy grid")

