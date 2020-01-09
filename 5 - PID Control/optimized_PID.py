# -----------
# User Instructions
#
# Implement a P controller by running 100 iterations
# of robot motion. The desired trajectory for the 
# robot is the x-axis. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau * crosstrack_error
#
# You'll only need to modify the `run` function at the bottom.
# ------------
 
import random
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------
# 
# this is the Robot class
#

class Robot(object):
    def __init__(self, length=20.0):
        """
        Creates robot and initializes location/orientation to 0, 0, 0.
        """
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation):
        """
        Sets a robot coordinate.
        """
        self.x = x
        self.y = y
        self.orientation = orientation % (2.0 * np.pi)

    def set_noise(self, steering_noise, distance_noise):
        """
        Sets the noise parameters.
        """
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

    def set_steering_drift(self, drift):
        """
        Sets the systematical steering drift parameter
        """
        self.steering_drift = drift

    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        """
        steering = front wheel steering angle, limited by max_steering_angle
        distance = total distance driven, most be non-negative
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = np.tan(steering2) * distance2 / self.length

        if abs(turn) < tolerance:
            # approximate by straight line motion
            self.x += distance2 * np.cos(self.orientation)
            self.y += distance2 * np.sin(self.orientation)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.orientation) * radius)
            self.y = cy - (np.cos(self.orientation) * radius)

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.orientation)

def run(robot, params, n=100, speed=1.0):
    x_trajectory = []
    y_trajectory = []
    kp,kd,ki = params
    
    # reference trajectory is a horizontal line along y=0
    y_ref = 0
    
    # positional error
    error_prev = 0
    
    # error integral
    error_int = 0
    
    # error value to be returned
    err = 0
    for i in range(n*2):
        error = robot.y - y_ref
        error_dot = error - error_prev
        error_int += error
        error_prev = error
        
        steer = -(kp * error) - (kd * error_dot) - (ki * error_int)
        
        robot.move(steer,speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
        
        # only keep track of error after we've done n iterations. basically
        # give it a chance to converge before evaluating 
        if i >= n:
            err += error ** 2
        
    return x_trajectory, y_trajectory, err

def make_robot():
    """
    Resets the robot back to the initial position and drift.
    You'll want to call this after you call `run`.
    """
    robot = Robot()
    robot.set(0.0, 1.0, 0.0)
    robot.set_steering_drift(10.0 / 180.0 * np.pi)
    return robot

# optimize PID constants
def twiddle(tol=0.001):
    p = [0.0,0.0,0.0]
    dp = [1.0,1.0,1.0]
    robot = make_robot()
    x_trajectory, y_trajectory, best_err = run(robot,p)
    
    
    # this loop will result in a convergence of all the parameters to yield an
    # optimal error value from the PID controller
    while (sum(dp) > tol):
        # for each parameter
        for i in range(len(p)):
            # add dp
            p[i] += dp[i]
            robot = make_robot()
            _,_,err = run(robot,p)
            
            
            if err < best_err:
                # if we've improved the error, save this error and increase dp
                best_err = err
                dp[i] *= 1.1
            else:
                # if we haven't improved the error, try subtracting dp (have to 
                # subtract 2*dp because you added it earlier) 
                p[i] -= 2 * dp[i]
                robot = make_robot()
                _,_,err = run(robot,p)
                
                if err < best_err:
                    # if we've improved the error, save this error and increase dp
                    best_err = err
                    dp[i] *= 1.1
                else:
                    # if we haven't improved the error, try decreasing dp
                    p[i] += dp[i]
                    dp[i] *= 0.9
                    
    return p, best_err
    
# get the optimal PID values
params, err = twiddle()
print("Final twiddle error = {}".format(err))
print("Optimal Kp:",params[0])
print("Optimal Kd:",params[1])
print("Optimal Ki:",params[2])
# run the PID controller with the optimal constants
robot = make_robot()
x_trajectory, y_trajectory,_ = run(robot, params)
n = len(x_trajectory)

fig, ax1 = plt.subplots(1, 1, figsize=(8, 8))
ax1.plot(x_trajectory, y_trajectory, 'g', label='P controller')
ax1.plot(x_trajectory, np.zeros(n), 'r', label='reference')
ax1.legend()
plt.show()