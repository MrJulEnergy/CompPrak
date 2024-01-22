import sys
sys.path.append('../CP') 

from variables import Variables
from particle import Particle
import numpy as np

class Setup:
    def __init__(self):
        pass

    def lattice_grid(self) -> np.ndarray:
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

    def choose_leader(self, particles: list[Particle], leader_paths) -> None:
        """Choose a random leader from a set of particles

        Parameters
        ----------
        particles : list[Particle]
        """
        leaders = np.random.choice(particles, size=Variables.N_leaders)
        leaders = sorted(leaders, key=lambda x: x.idx, reverse=True)
        for i, particle in enumerate(leaders):
            particle.set_leader(i, leader_paths[i])

    def leader_paths(self):
        # Kreisbahn:
        t = np.linspace(0, 20, Variables.n_time_steps+1)
        x_1 = 3*np.cos(t)
        y_1 = 3*np.sin(t)

        x_2 = np.linspace(0, 30, Variables.n_time_steps+1)
        y_2 = x_2

        x_1 = np.diff(x_1)
        y_1 = np.diff(y_1)
        x_2 = np.diff(x_2)
        y_2 = np.diff(y_2)
        
        leader_paths = np.array([[x_2, y_2], [x_2, y_2], [x_2, y_2], [x_2, y_2]])
        leader_paths = np.zeros(shape=(Variables.N_leaders, 2, Variables.n_time_steps))
        return leader_paths

    def setup(self):
        particles = self.lattice_grid()
        self.choose_leader(particles, self.leader_paths())
        return particles
    
