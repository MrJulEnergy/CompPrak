import numpy as np
from variables import Variables
import copy
import tqdm

class Simulation:
    def __init__(self, particles):
        self.particles = particles

    def W(self):
        # sig ist standardabweichung der normalverteilung
        sig = np.sqrt(2*Variables.mass * Variables.k_B * Variables.gamma * Variables.Temp / Variables.dt) # geht leider nicht mir particle.mass hier :(
        w = np.random.uniform(-1,1,(Variables.N, 2)) * sig *np.sqrt(2) # sqrt(2) weil 2d 
        return w

    def lj_force(self):
        #TODO Hier ist nur ein Lennard Jones Potential zur zeit
        
        f = np.zeros(shape=(Variables.N, 2))
        pairs = [(i, j) for i in range(Variables.N) for j in range(i+1, Variables.N)]
        for pair in pairs:
            r_ij_vec = self.particles[pair[0]].x - self.particles[pair[1]].x
            r = np.linalg.norm(r_ij_vec)
            fac = 4.0 * (12.0 * np.power(r, -13.) - 6.0 * np.power(r, -7.)) 
            f_ij = fac * r_ij_vec / r
            f[pair[0], :] += f_ij
            f[pair[1], :] -= f_ij # (Actio=reactio, was der leader aber warscheinlich nicht erfährt. vielleicht aber abgeschwächt) 
        return f
    
    def step_vv_langevin(self) -> None:
        # Führe einen Velocity-Verlet Schritt für ein Langevin System aus
        for p in self.particles:
            # Update alle positionen und geschwindigkeiten aller(!!) Teilchen
            p.x += p.v * Variables.dt * (1 - Variables.dt * Variables.gamma * 0.5) + 0.5 * p.f * Variables.dt * Variables.dt / Variables.mass
            p.v = (p.v * (1 - Variables.dt * Variables.gamma * 0.5) + 0.5 / Variables.mass * p.f * Variables.dt) / (1 + 0.5 * Variables.dt * Variables.gamma)
        f = self.lj_force() + self.W() # anstatt np.zeros_like(x) kommt hier die anziehung des leaders hin
        for i, p in enumerate(self.particles):
            p.f = f[i, :]
            p.v = p.v + (0.5 / Variables.mass * p.f * Variables.dt) / (1 + 0.5 * Variables.dt * Variables.gamma)
        

    def run(self):
        state = []
        t = 0
        n_steps = int(Variables.T*Variables.fps)
        for _ in tqdm.tqdm(range(n_steps)):
            self.step_vv_langevin()
            #TODO Periodic Bounday Conditions
            copied_particles = copy.deepcopy(self.particles)
            state.append(copied_particles)
        return np.array(state)