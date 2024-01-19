import numpy as np
from variables import Variables
from particle import Particle
import copy
import tqdm

class Simulation:
    def __init__(self, particles):
        self.particles = particles
        self.leader_list = [i for i in range(Variables.N) if self.particles[i].leader]
        print(self.leader_list)
    def W(self):
        # sig ist standardabweichung der normalverteilung
        sig = np.sqrt(2*Variables.mass * Variables.k_B * Variables.gamma * Variables.Temp / Variables.dt) # geht leider nicht mir particle.mass hier :(
        w = np.random.uniform(-1,1,(Variables.N, 2)) * sig *np.sqrt(2) # sqrt(2) weil 2d 
        return w

    def leader_force(self):
        #TODO
        f = np.zeros(shape=(Variables.N, 2))
        for i in range(Variables.N):
            if not self.particles[i].leader:
                for j in range(Variables.N_leaders):
                    r_ij = self.particles[i].x - self.particles[self.leader_list[j]].x
                    r_ij = self.minimum_image_vector(r_ij)
                    r = np.linalg.norm(r_ij)
                    self.particles[i].update_convinced(r, j)
                    fac = Variables.leader_attraction * self.particles[i].convinced[j] * 4.0 * (12.0 * np.power(Variables.leader_position/r, 13.) - 6.0 * np.power(Variables.leader_position/r, 7.)) 
                    f_ij = fac * r_ij / r
                    f[i, :] += f_ij
                    f[j, :] = np.zeros(shape=2)
        return f

    def lj_force(self):
        f = np.zeros(shape=(Variables.N, 2))
        pairs = [(i, j) for i in range(Variables.N) for j in range(i+1, Variables.N)]
        for pair in pairs:
            r_ij_vec = self.particles[pair[0]].x - self.particles[pair[1]].x
            r_ij_vec = self.minimum_image_vector(r_ij_vec)
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
            p.x = self.periodic_boundarys(p.x)
            p.v = (p.v * (1 - Variables.dt * Variables.gamma * 0.5) + 0.5 / Variables.mass * p.f * Variables.dt) / (1 + 0.5 * Variables.dt * Variables.gamma)
        f = self.lj_force() + self.W() + self.leader_force() # anstatt np.zeros_like(x) kommt hier die anziehung des leaders hin
        for i, p in enumerate(self.particles):
            p.f = f[i, :]
            p.v = p.v + (0.5 / Variables.mass * p.f * Variables.dt) / (1 + 0.5 * Variables.dt * Variables.gamma)
        

    def run(self):
        state = []
        t = 0
        n_steps = int(Variables.T*Variables.fps)
        for _ in tqdm.tqdm(range(n_steps)):
            self.step_vv_langevin()
            copied_particles = copy.deepcopy(self.particles)
            state.append(copied_particles)
        return np.array(state)
    
    def minimum_image_vector(self, r_ij):
        r_ij -= np.rint(r_ij / Variables.box[0]) * Variables.box[0]
        return r_ij
    
    def periodic_boundarys(self, x: np.array):        
        for i in range(2):
            if x[i] > Variables.box[i]:
                x[i] = x[i]-Variables.box[i]
            if x[i] <= 0:
                x[i] = x[i]+Variables.box[i]
        return x
