from visualize import Visualize
from variables import Variables
from simulation import Simulation
from particle import Particle

import pickle
import numpy as np
import time

def lattice_grid() -> np.ndarray:
    # Setze alle partikel auf ein 2D grid, sodass sie sich nicht überlappen
    particles = np.zeros(shape=Variables.N, dtype=Particle)
    i = 0
    for row in range(Variables.N_PER_SIDE):
        for col in range(Variables.N_PER_SIDE):
            x0 = np.array([Variables.box[0]/Variables.N_PER_SIDE * col, Variables.box[1]/Variables.N_PER_SIDE * row])
            v0 = np.zeros_like(x0)
            f0 = np.zeros_like(x0)

            particles[i] = Particle(x0, v0, f0, Variables.particle_starting_color, i)
            i+=1
    return particles

def choose_leader(particles: list[Particle], leader_paths) -> None:
    """Choose a random leader from a set of particles

    Parameters
    ----------
    particles : list[Particle]
    """
    leaders = np.random.choice(particles, size=Variables.N_leaders)
    leaders = sorted(leaders, key=lambda x: x.idx, reverse=True)
    for i, particle in enumerate(leaders):
        particle.set_leader(i, leader_paths[i])

leader_paths = np.zeros(shape=(Variables.N_leaders, 2, Variables.n_time_steps))
particles = lattice_grid()
choose_leader(particles, leader_paths)



N_arr = np.arange(2, 11, 1)
times = []
for N in N_arr:
    Variables.N_PER_SIDE = int(N)
    print(Variables.N)
    leader_paths = np.zeros(shape=(Variables.N_leaders, 2, Variables.n_time_steps))
    particles = lattice_grid()
    choose_leader(particles, leader_paths)
    sim = Simulation(particles)
    start = time.time()
    state = sim.run()
    times.append(time.time()-start)
    with open("checkpoints/times.save", 'wb') as fp:
        pickle.dump(times, fp)


