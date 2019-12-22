# update step --> merge two distributions
def update(mean1, var1, mean2, var2):
    new_mean = float(var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1./(1./var1 + 1./var2)
    return [new_mean, new_var]


# prediction step --> add two distributions
def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

# measurements and motions to go thru
measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]

# variance associated with measurement update
measurement_sig = 4.

# variance associated with motion 
motion_sig = 2.

# initial mean and variance
mu = 0.
sig = 10000.


print()
print("Action --> [Position Estimate, Variance]")
print()
for n in range(len(measurements)):
    [mu,sig] = update(mu, sig, measurements[n], measurement_sig)
    print("Update -->",[mu,sig])
    [mu,sig] = predict(mu, sig, motion[n], motion_sig)
    print("Predict -->",[mu,sig])

