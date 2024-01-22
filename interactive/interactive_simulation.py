import sys
sys.path.append('../CP') 

import numpy as np
from variables import Variables
from particle import Particle
import copy
import tqdm

class Simulation:
    def __init__(self, particles):
        self.particles = particles
        self.leader_list = [i for i in range(Variables.N) if self.particles[i].leader]
        self.leaders = [particles[i] for i in self.leader_list]

    # Alle Kräfte ----------------------------------------
    def lennard_jones_pair_force(self, r_ij: np.array, a: float, b: float):
        # Calculate the LJ-Force acting on the particles
        r_ij = self.minimum_image_vector(r_ij)
        r = np.linalg.norm(r_ij)    
        r = self.check_zero(r)
        fac = 4.0 * a * (-12.0 * np.power(b/r, 13.) + 6.0 * np.power(b/r, 7.))
        f_ij = fac * r_ij / r
        return f_ij

    def W(self):
        # sig ist standardabweichung der normalverteilung
        sig = np.sqrt(2*Variables.mass * Variables.k_B * Variables.gamma * Variables.Temp / Variables.dt) # geht leider nicht mir particle.mass hier :(
        w = np.random.uniform(-1,1,(Variables.N, 2)) * sig *np.sqrt(2) # sqrt(2) weil 2d 
        return w

    def leader_force(self):
        f = np.zeros(shape=(Variables.N, 2))
        for i in range(Variables.N): # iterieren über alle teilchen
            if not self.particles[i].leader: # schauen ob teilchen leader ist
                for j in range(Variables.N_leaders): # iterieren über alle leader
                    p = self.particles[i]
                    l = self.particles[self.leader_list[j]]
                    
                    a = Variables.leader_attraction * p.convinced[j]
                    b = Variables.leader_position
                    r_ij = l.x - p.x 
                    f_ij = self.lennard_jones_pair_force(r_ij, a, b)
                    
                    r = np.linalg.norm(r_ij)
                    r = self.check_zero(r)
                    p.update_convinced(r, j, self.leaders)

                    f[i, :] += f_ij
                    f[j, :] = np.zeros(shape=2)
        return f

    def simple_interaction(self):
        f = np.zeros(shape=(Variables.N, 2))
        pairs = [(i, j) for i in range(Variables.N) for j in range(i+1, Variables.N)]
        for pair in pairs:
            r_ij = self.particles[pair[1]].x - self.particles[pair[0]].x
            f_ij = self.lennard_jones_pair_force(r_ij, 1, 1)
            f[pair[0], :] += f_ij
            f[pair[1], :] -= f_ij
        return f
    
    def mouse_force(self, pos: np.array):
        for leader in self.leaders:
            r_ij = pos-leader.x
            r = np.linalg.norm(r_ij)
            r = self.check_zero(r)
            fac = 100 / np.sqrt(r)
            leader.f = fac * r_ij / r

    # Integrator  ----------------------------------------
    def step_vv_langevin(self) -> None:
        # Führe einen Velocity-Verlet Schritt für ein Langevin System aus
        for p in self.particles:
            # Update alle positionen und geschwindigkeiten aller(!!) Teilchen
            p.x += p.v * Variables.dt * (1 - Variables.dt * Variables.gamma * 0.5) + 0.5 * p.f * Variables.dt * Variables.dt / Variables.mass
            p.x = self.periodic_boundarys(p.x)
            if p.leader:
                p.update_leader_pos(self.run_index)
            p.v = (p.v * (1 - Variables.dt * Variables.gamma * 0.5) + 0.5 / Variables.mass * p.f * Variables.dt) / (1 + 0.5 * Variables.dt * Variables.gamma)
        
        f = self.simple_interaction() + self.leader_force() + self.W() # anstatt np.zeros_like(x) kommt hier die anziehung des leaders hin
        
        for i, p in enumerate(self.particles):
            p.f = f[i, :]
            p.v = p.v + (0.5 / Variables.mass * p.f * Variables.dt) / (1 + 0.5 * Variables.dt * Variables.gamma)
        self.cap_velocities()
        
    # Alles wird hier ausgeführt ----------------------------------------
    def run(self):
        self.run_index = 0
        while True:
            self.step_vv_langevin()
            self.run_index = 0
            yield np.array(self.particles)
    


    # Tools ----------------------------------------
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
    
    def check_zero(self, r: float):
        if 0 <= r and r <=0.1:
            r = 0.1
            print("[WARNUNG] check_zero: System ist instabil")
            return r
        else:
            return r
        
    def cap_velocities(self):
        for p in self.particles:
            if np.linalg.norm(p.v) >= 30:
                p.v = np.random.random(size=2)-.5