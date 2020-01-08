from math import *
import numpy as np


def kalman_filter(x,P):
    for n in range(len(measurements)):
        
        # prediction
        z = np.array([measurements[n]])
        y = z - (H @ x)
        S = (H @ P @ H.T) + R
        K = P @ H.T @ np.linalg.inv(S)
        x = x + (K @ y)
        P = (I - (K @ H)) @ P
        
        # measurement update
        x = (F @ x) + u
        P = F @ P @ F.T
        
    return x,P

# assume dt between each of these measurements is 1
measurements = [1, 2, 3]

# initial state [x,xdot]
x = np.array([[0.],
              [0.]]) 
    
# initial uncertainty
P = np.array([[1000., 0.],
              [0.,1000.]]) 
    
# external motion
u = np.array([[0.],
              [0.]]) 
    
# next state function (x' = x + xdot*dt, xdot' = xdot)
F = np.array([[1.,1.],
              [0.,1.]]) 
    
# measurement function (can only measure position)
H = np.array([[1.,0.]]) 

# measurement uncertainty
R = np.array([[1.]]) 

I = np.eye(2) # identity matrix

x,P = kalman_filter(x, P)

print("Estimated State [x, xdot]^T")
for row in x:
    print(row)
print()
print("Uncertainty Covariance:")
print(P)
# output should be:
# x: [[3.9996664447958645], [0.9999998335552873]]
# P: [[2.3318904241194827, 0.9991676099921091], [0.9991676099921067, 0.49950058263974184]]
