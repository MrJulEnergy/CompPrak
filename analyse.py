from visualize import Visualize
from variables import Variables
from particles import Simulation

import pickle
import numpy as np


def lattice_grid() -> np.ndarray:
    # Square Lattice als anfangsposition aller Teilchen
    x = np.zeros((Variables.N, 2))
    particles = []
    for row in range(Variables.N_PER_SIDE):
        for col in range(Variables.N_PER_SIDE):
            particles.append(np.array([Variables.box[0]/Variables.N_PER_SIDE * col, Variables.box[1]/Variables.N_PER_SIDE * row]))
    for j in range(Variables.N):
        x[j, :] = particles[j]
    return x

x = lattice_grid()
v = np.zeros((Variables.N, 2))

sim = Simulation(x, v)
traj = sim.run()

with open(Variables.dumpfile, 'wb') as fp:
        pickle.dump(traj, fp)

with open(Variables.dumpfile, 'rb') as fp:
    data = pickle.load(fp)

bounds_max = max([np.max(data[:, 0, :]), np.max(data[:, 1, :]), np.abs(np.min(data[:, 0, :])), np.abs(np.min(data[:, 1, :]))])

bounds = [-0.5*Variables.box[0], Variables.box[0]+0.5*Variables.box[0], -0.5*Variables.box[1], Variables.box[1]+0.5*Variables.box[1]]

vis = Visualize(data, bounds)
