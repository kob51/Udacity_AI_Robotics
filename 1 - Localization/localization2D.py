# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]

    for k in range(len(measurements)):
      p = move(p,motions[k],p_move,colors)
      p = sense(p,measurements[k],sensor_right,colors)
    
    return p

def move(p,U,p_move,colors):
    # no overshoot or undershoot here, but there's a possibility you stay put when you wanted to move
    p_stay = 1. - p_move
    q = [[0 for row in range(len(colors[0]))] for col in range(len(colors))]
    for x in range(len(q[0])):
        for y in range(len(q)):
            # i-U moves every element to the left by U
            # taking mod by length creates wraparound from low index to high index (0 -> end)

            # mod definition: a mod b = c --> x*b + c = a (useful for when i-U < 0)

            # calculate probability of landing at your desired location
            q[y][x] = p_move * p[(y-U[0]) % len(p)][(x-U[1]) % len(p[0])]
            
            # add probability of not moving (complement of moving in this case)
            q[y][x] += p_stay * p[y][x]
    
    return q

def sense(p,Z,pHit,colors):
    q = [[0 for row in range(len(colors[0]))] for col in range(len(colors))]
    pMiss = 1. - pHit
    for x in range(len(p[0])):
        for y in range(len(p)):
            # if Z == world[i], append p[i] * pHit
            # if Z != world[i], append p[i] * pMiss
            hit = (Z == colors[y][x])
            q[y][x] = p[y][x] * (hit * pHit + (1-hit) * pMiss)

    # map(func,list) returns a list where each element is func(list[i])
    s = sum(map(sum,q))

    # normalize new distribution
    for x in range(len(p[0])):
        for y in range(len(p)):
            q[y][x] /= s

    return q 

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)


# which testcase do we want to run
test_num = 5

if test_num == 1:
    # test 1
    colors = [['G', 'G', 'G'],
              ['G', 'R', 'G'],
              ['G', 'G', 'G']]
    measurements = ['R']
    motions = [[0,0]]
    sensor_right = 1.0
    p_move = 1.0
    correct_answer = (
        [[0.0, 0.0, 0.0],
         [0.0, 1.0, 0.0],
         [0.0, 0.0, 0.0]])

elif test_num == 2:
    # test 2
    colors = [['G', 'G', 'G'],
              ['G', 'R', 'R'],
              ['G', 'G', 'G']]
    measurements = ['R']
    motions = [[0,0]]
    sensor_right = 1.0
    p_move = 1.0
    correct_answer = (
        [[0.0, 0.0, 0.0],
         [0.0, 0.5, 0.5],
         [0.0, 0.0, 0.0]])

elif test_num == 3:
    # test 3
    colors = [['G', 'G', 'G'],
              ['G', 'R', 'R'],
              ['G', 'G', 'G']]
    measurements = ['R']
    motions = [[0,0]]
    sensor_right = 0.8
    p_move = 1.0
    correct_answer = (
        [[0.06666666666, 0.06666666666, 0.06666666666],
         [0.06666666666, 0.26666666666, 0.26666666666],
         [0.06666666666, 0.06666666666, 0.06666666666]])

elif test_num == 4:
    # test 4
    colors = [['G', 'G', 'G'],
              ['G', 'R', 'R'],
              ['G', 'G', 'G']]
    measurements = ['R', 'R']
    motions = [[0,0], [0,1]]
    sensor_right = 0.8
    p_move = 1.0
    correct_answer = (
        [[0.03333333333, 0.03333333333, 0.03333333333],
         [0.13333333333, 0.13333333333, 0.53333333333],
         [0.03333333333, 0.03333333333, 0.03333333333]])

elif test_num == 5:
    # test 5
    colors = [['G', 'G', 'G'],
              ['G', 'R', 'R'],
              ['G', 'G', 'G']]
    measurements = ['R', 'R']
    motions = [[0,0], [0,1]]
    sensor_right = 1.0
    p_move = 1.0
    correct_answer = (
        [[0.0, 0.0, 0.0],
         [0.0, 0.0, 1.0],
         [0.0, 0.0, 0.0]])

elif test_num == 6:
    # test 6
    colors = [['G', 'G', 'G'],
              ['G', 'R', 'R'],
              ['G', 'G', 'G']]
    measurements = ['R', 'R']
    motions = [[0,0], [0,1]]
    sensor_right = 0.8
    p_move = 0.5
    correct_answer = (
        [[0.0289855072, 0.0289855072, 0.0289855072],
         [0.0724637681, 0.2898550724, 0.4637681159],
         [0.0289855072, 0.0289855072, 0.0289855072]])

elif test_num == 7:
    # test 7
    colors = [['G', 'G', 'G'],
              ['G', 'R', 'R'],
              ['G', 'G', 'G']]
    measurements = ['R', 'R']
    motions = [[0,0], [0,1]]
    sensor_right = 1.0
    p_move = 0.5
    correct_answer = (
        [[0.0, 0.0, 0.0],
         [0.0, 0.33333333, 0.66666666],
         [0.0, 0.0, 0.0]])

elif test_num == 8:
    # test 8
    colors = [['R','G','G','R','R'],
              ['R','R','G','R','R'],
              ['R','R','G','G','R'],
              ['R','R','R','R','R']]
    measurements = ['G','G','G','G','G']
    motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
    sensor_right = 0.7
    p_move = 0.8
    correct_answer = [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
                     [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
                     [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
                     [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]


p = localize(colors,measurements,motions,sensor_right, p_move)
print("Calculated Distribution:")
show(p)
print()
print("Expected Distribution:")
show(correct_answer)
