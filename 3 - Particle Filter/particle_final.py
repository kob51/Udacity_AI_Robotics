from math import *
import random

# --------
# 
# some top level parameters
#

max_steering_angle = pi / 4.0 # You do not need to use this value, but keep in mind the limitations of a real car.
bearing_noise = 0.1 # Noise parameter: should be included in sense function.
steering_noise = 0.1 # Noise parameter: should be included in move function.
distance_noise = 5.0 # Noise parameter: should be included in move function.

tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.


# --------
# 
# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
#
# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks in (y, x) format.
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"

# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------
    # init: 
    #    creates robot and initializes location/orientation 
    #

    def __init__(self, length = 20.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero

    # --------
    # set: 
    #    sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise(ValueError, 'Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    # --------
    # set_noise: 
    #    sets the noise parameters
    #
    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # measurement_prob
    #    computes the probability of a measurement
    #  

    def measurement_prob(self, measurements):

        # calculate the correct measurement
        predicted_measurements = self.sense() # Our sense function took 0 as an argument to switch off noise.


        # compute errors
        error = 1.0
        for i in range(len(measurements)):
            error_bearing = abs(measurements[i] - predicted_measurements[i])
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate
            

            # update Gaussian
            error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /  
                      sqrt(2.0 * pi * (self.bearing_noise ** 2)))

        return error
    
    def __repr__(self): #allows us to print robot attributes.
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), 
                                                str(self.orientation))
       
    def move(self, motion):
        
        # turning tolerance. below this turning angle, assume straight line motion
        tolerance = 0.001 
        
        alpha = motion[0] # steering angle
        d = motion[1] # distance
        
        x = self.x
        y = self.y
        
        length = self.length
        theta = self.orientation
        
        # turning angle
        beta =  tan(alpha) * d / length

        if abs(beta) < tolerance:
            # approximate straight line motion
            x1 = x + (d * cos(theta))
            y1 = y + (d * sin(theta))
        else:
            # approximate bicycle model for motion
            radius = d / beta
            cx = x - (sin(theta) * radius)
            cy = y + (cos(theta) * radius)
            x1 = cx + (sin(theta + beta) * radius)
            y1 = cy - (cos(theta + beta) * radius)
        
        theta1 = (theta + beta) % (2.0 * pi)
        
        # add noise to distance and heading measurements
        x1 += random.gauss(0,self.distance_noise)
        y1 += random.gauss(0,self.distance_noise)
        theta1 += random.gauss(0, self.steering_noise)
        theta1 %= (2*pi)
        
        # initialize new robot class with new location
        result = robot(length)
        result.set(x1,y1,theta1)
        result.set_noise(self.bearing_noise, self.steering_noise, self.distance_noise)

        return result 

    def sense(self,add_noise=1):
        Z = []
        
        # build a list of bearing errors to each landmark
        for l in landmarks:
            dy = l[0] - self.y
            dx = l[1] - self.x
            
            bearing = atan2(dy,dx) - self.orientation
            bearing %= 2*pi
                            
            if add_noise:
                bearing += random.gauss(0.0,self.bearing_noise)
                
            Z.append(bearing)

        return Z 

# --------
#
# extract position from a particle set
# 


# takes the average position of all particles and returns that as our estimated position
def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi)) 
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]

# --------
#
# The following code generates the measurements vector
# You can use it to develop your solution.
# 


def generate_ground_truth(motions):

    myrobot = robot()
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

    Z = []
    T = len(motions)

    for t in range(T):
        myrobot = myrobot.move(motions[t])
        Z.append(myrobot.sense())
    #print 'Robot:    ', myrobot
    return [myrobot, Z]

# --------
#
# The following code prints the measurements associated
# with generate_ground_truth
#

def print_measurements(Z):

    T = len(Z)

    print('measurements = [[%.8s, %.8s, %.8s, %.8s],' % \
        (str(Z[0][0]), str(Z[0][1]), str(Z[0][2]), str(Z[0][3])))
    for t in range(1,T-1):
        print('                [%.8s, %.8s, %.8s, %.8s],' % \
            (str(Z[t][0]), str(Z[t][1]), str(Z[t][2]), str(Z[t][3])))
    print('                [%.8s, %.8s, %.8s, %.8s]]' % \
        (str(Z[T-1][0]), str(Z[T-1][1]), str(Z[T-1][2]), str(Z[T-1][3])))

# --------
#
# The following code checks to see if your particle filter
# localizes the robot to within the desired tolerances
# of the true position. The tolerances are defined at the top.
#

def check_output(final_robot, estimated_position):

    error_x = abs(final_robot.x - estimated_position[0])
    error_y = abs(final_robot.y - estimated_position[1])
    error_orientation = abs(final_robot.orientation - estimated_position[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tolerance_xy and error_y < tolerance_xy \
              and error_orientation < tolerance_orientation
    return correct



def particle_filter(motions, measurements, N=500):
    # --------
    #
    # Make particles
    # 

    p = []
    for i in range(N):
        r = robot()
        r.set_noise(bearing_noise, steering_noise, distance_noise)
        p.append(r)

    # --------
    #
    # Update particles
    #     

    for t in range(len(motions)):
    
        # motion update (prediction)
        p2 = []
        for i in range(N):
            p2.append(p[i].move(motions[t]))
        p = p2

        # measurement update
        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(measurements[t]))

        # resampling wheel
        # youtube.com/watch?v=wNQVo6uOgYA
        p3 = []
        index = int(random.random() * N)
        beta = 0.0
        mw = max(w)
        for i in range(N):
            beta += random.random() * 2.0 * mw
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p3.append(p[index])
        p = p3
    
    return get_position(p)
 
# --------
# TEST CASES:
# 
#1) Calling the particle_filter function with the following
#    motions and measurements should return a [x,y,orientation]
#    vector near [x=93.476 y=75.186 orient=5.2664], that is, the
#    robot's true location.
#
motions = [[2. * pi / 10, 20.] for row in range(8)]

#measurements are bearing errors to the 4 "landmarks" in the map
measurements = [[4.746936, 3.859782, 3.045217, 2.045506],
                [3.510067, 2.916300, 2.146394, 1.598332],
                [2.972469, 2.407489, 1.588474, 1.611094],
                [1.906178, 1.193329, 0.619356, 0.807930],
                [1.352825, 0.662233, 0.144927, 0.799090],
                [0.856150, 0.214590, 5.651497, 1.062401],
                [0.194460, 5.660382, 4.761072, 2.471682],
                [5.717342, 4.736780, 3.909599, 2.342536]]

result = particle_filter(motions,measurements)

print("Estimated pose")
print("x =", result[0])
print("y =", result[1])
print("theta =", result[2])

print()
print("Ground truth pose")
print("x = 93.476")
print("y = 75.186")
print("theta = 5.2664")

# 2) You can generate your own test cases by generating
#    measurements using the generate_ground_truth function.
#    It will print the robot's last location when calling it.
#
#


#number_of_iterations = 18
#motions = [[2. * pi / 20, 12.] for row in range(number_of_iterations)]
#
#x = generate_ground_truth(motions)
#final_robot = x[0]
##measurements are bearing errors to the 4 "landmarks" in the map
#measurements = x[1]
#estimated_position = particle_filter(motions, measurements)
#print_measurements(measurements)
#print('Ground truth:    ', final_robot)
#print('Particle filter: ', estimated_position)
#print('Code check:      ', check_output(final_robot, estimated_position))


