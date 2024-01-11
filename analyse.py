from visualize import Visualize
from variables import Variables
from particles import Simulation

import pickle
import numpy as np

x = np.random.random((Variables.N, 2))
v = np.zeros((Variables.N, 2))

sim = Simulation(x, v)
traj = sim.run()

with open(Variables.dumpfile, 'wb') as fp:
        pickle.dump(traj, fp)



with open(Variables.dumpfile, 'rb') as fp:
    data = pickle.load(fp)


#print(data[0, 0, :100])
bounds_max = max([np.max(data[:, 0, :]), np.max(data[:, 1, :]), np.abs(np.min(data[:, 0, :])), np.abs(np.min(data[:, 1, :]))])
bounds = [-bounds_max, bounds_max, -bounds_max, bounds_max]
vis = Visualize(data, bounds)
