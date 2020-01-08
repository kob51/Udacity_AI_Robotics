from math import *
import numpy as np


def filter(x,P):
    for n in range(len(measurements)):
        
        # prediction
        x = (F @ x) + u
        P = F @ P @ F.T
        
        # measurement update
        z = np.array([measurements[n]]).T
        y = z - (H @ x)
        S = (H @ P @ H.T) + R
        K = P @ H.T @ np.linalg.inv(S)
        x = x + (K @ y)
        P = (I - (K @ H)) @ P

    return x,P

########################################

print("### 4-dimensional example ###")
print()

unc = 0.1 # measurement uncertainty
dt = 0.1 # timestep btwn measurements

#Uncomment one set of measurements and initial_xy

measurements = [[5., 10.], [6., 8.], [7., 6.], [8., 4.], [9., 2.], [10., 0.]]
initial_xy = [4., 12.]

#measurements = [[1., 4.], [6., 0.], [11., -4.], [16., -8.]]
#initial_xy = [-4., 8.]

#measurements = [[1., 17.], [1., 15.], [1., 13.], [1., 11.]]
#initial_xy = [1., 19.]

# initial state [x,y,xdot,ydot]
x = np.array([[initial_xy[0]],[initial_xy[1]],[0.],[0.]])

# external motion
u = np.zeros((4,1))

# initial uncertainty: 0 for positions x and y, 1000 for the two velocities
P =  np.array([[0.,0.,0.,0.],
               [0.,0.,0.,0.],
               [0.,0.,1000.,0.],
               [0.,0.,0.,1000.]])

# next state function
# x' = x + xdot*dt, y' = y + ydot*dt, xdot' = xdot, ydot' = ydot
F =  np.array([[1.,0.,dt,0.],
               [0.,1.,0.,dt],
               [0.,0.,1.,0.],
               [0.,0.,0.,1.]])

# measurement function: reflect the fact that we observe x and y but not the two velocities
H =  np.array([[1.,0.,0.,0.],
               [0.,1.,0.,0.]])

# measurement uncertainty: use 2x2 matrix with 0.1 as main diagonal
R =  np.eye(2)*0.1

I =  np.eye(4)


x,P = filter(x, P)
print("State [x y xdot ydot]^T")
print(x)
print()
print("Covariance Uncertainty")
print(P)
