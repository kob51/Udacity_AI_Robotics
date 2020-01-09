from copy import deepcopy
import matplotlib.pyplot as plt

def printpaths(path,newpath):
    print()
    print("Original Waypoints -> Final Waypoints:")
    for old,new in zip(path,newpath):
        print('['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']')

path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)

    change = tolerance
    while change >= tolerance: 
        change = 0.0
        # don't perform smoothing on first or last waypoint
        print("Current Waypoints:")
        for i in range(1,len(path)-1):
            for j in range(len(path[0])):
                aux = newpath[i][j]
                # y --> newpath
                # x --> original path
                
                # (x[i] - y[i])^2 --> minimize
                # y[i] - (-2)*weight_data*(x[i] - y[i]) --> gradient descent
                # optimize the new path's distance from the original path
                newpath[i][j] += weight_data * (path[i][j] - aux)
                
                
                # (y[i] - y[i+1])^2 --> minimize
                # y[i] - (-2)*weight_smooth*(y[i] - y[i+1]) --> gradient descent
                
                # (y[i] - y[i-1])^2 --> minimize
                # y[i] - (-2)*weight_smooth*(y[i] - y[i-1]) --> gradient descent
                
                # optimize the distance from each point to its neighboring points
                newpath[i][j] += weight_smooth * (newpath[i-1][j] + newpath[i+1][j] - (2.0*aux))
                change += abs(aux - newpath[i][j])
            print(newpath[i])
        print("Loss:", change)
        
        # each block of output shows the current  set of waypoints along with 
        # the error/loss associated with that set
        if change >= tolerance:
            print("-----------------")
    
    return newpath

newpath = smooth(path)
printpaths(path,newpath)
x_orig = []
y_orig = []

x_smooth = []
y_smooth = []
for i in range(len(path)):
    x_orig.append(path[i][0])
    y_orig.append(path[i][1])
    x_smooth.append(newpath[i][0])
    y_smooth.append(newpath[i][1])

fig, ax = plt.subplots(1, 1)
ax.plot(x_orig,y_orig,label="original path")
ax.plot(x_smooth,y_smooth,label="smoothed path")
ax.legend()
