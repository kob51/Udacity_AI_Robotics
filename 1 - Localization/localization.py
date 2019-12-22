def sense(p, Z):
    q=[]
    for i in range(len(p)):
        # if Z == world[i], append p[i] * pHit
        # if Z != world[i], append p[i] * pMiss
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)

    # normalize new distribution
    for i in range(len(q)):
        q[i] = q[i] / s

    return q

def move(p, U):
    q = []
    for i in range(len(p)):
        # i-U moves every element to the left by U
        # taking mod by length creates wraparound from low index to high index (0 -> end)

        # mod definition: a mod b = c --> x*b + c = a (useful for when i-U < 0)

        # calculate probability of landing at your desired location
        s = pExact * p[(i-U) % len(p)]

        # add probabilities of overshooting or undershooting your desired location
        s += pOvershoot * p[(i-U-1) % len(p)]
        s += pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
        
    return q

##SCRIPT STARTS HERE##
if __name__ == "__main__":
    # p represents the probability that we are at the given index of p in the world.
    # start with a uniform distribution, we have no info about the world yet
    p=[0.2, 0.2, 0.2, 0.2, 0.2]

    # the environment that we are sensing/traversing (assuming a circular 1D array, 
    # ie. world[5] = world[0])
    world=['green', 'red', 'red', 'green', 'green']

    # what we get back for measurements
    measurements = ['red', 'green']

    # the steps we take thru the environment
    motions = [1,1]

    # probability of a hit or miss in measurement (sense fxn)
    # if we have a hit, multiply by a large #
    pHit = 0.6
    # if we have a miss, multiply by a smaller #
    pMiss = 0.2

    # probability of exact movement, overshoot movement, or undershoot movement (move fxn)
    pExact = 0.8
    pOvershoot = 0.1
    pUndershoot = 0.1

    # loop thru measurements and motions, printing the updated distribution after
    # each action
    print()
    print("Action Performed -> Resulting Distribution")
    print()
    for k in range(len(measurements)):
        p = sense(p, measurements[k])
        print("Measure",measurements[k],"->",'['+ ', '.join('%.3f'%j for j in p) + ']')
        print()
        p = move(p, motions[k])
        print("Move",motions[k],"->",'['+ ', '.join('%.3f'%j for j in p) + ']')
        print()
