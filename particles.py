import numpy as np
from variables import Variables


class Simulation:
    def __init__(self, x0, v0):
        self.x = x0
        self.v = v0

    def W(self):
        # sig ist standardabweichung der normalverteilung
        sig = np.sqrt(2*Variables.mass * Variables.k_B * Variables.gamma * Variables.Temp / Variables.dt)
        w = np.random.uniform(-1,1,(Variables.N, 2)) * sig *np.sqrt(2) # sqrt(2) weil 2d 
        return w

    def leader_force(self, x):
        #TODO Hier ist nur ein Lennard Jones Potential zur zeit
        def _lj_force(r_ij):
            r = np.linalg.norm(r_ij)
            fac = 4.0 * (12.0 * np.power(r, -13.) - 6.0 * np.power(r, -7.))
            return fac * r_ij / r
        
        f = np.zeros_like(x)
        pairs = [(i, j) for i in range(Variables.N) for j in range(i+1, Variables.N)]
        for pair in pairs:
            r_ij_vec = x[pair[0], :] - x[pair[1], :]
            f_ij = _lj_force(r_ij_vec)
            f[pair[0]] += f_ij
            f[pair[1]] -= f_ij # (Actio=reactio, was der leader aber warscheinlich nicht erfährt. vielleicht aber abgeschwächt) 
        return f
    
    def step_vv_langevin(self, x , v , f):
        x += v * Variables.dt * (1 - Variables.dt * Variables.gamma * 0.5) + 0.5 * f * Variables.dt * Variables.dt / Variables.mass
        v = (v * (1 - Variables.dt * Variables.gamma * 0.5) + 0.5 / Variables.mass * f * Variables.dt) / (1 + 0.5 * Variables.dt * Variables.gamma)

        f = self.leader_force(x) + self.W() # anstatt np.zeros_like(x) kommt hier die anziehung des leaders hin
        v = v + (0.5 / Variables.mass * f * Variables.dt) / (1 + 0.5 * Variables.dt * Variables.gamma)
        return x , v , f

    def run(self):
        traj = []
        t = 0
        x = self.x
        v = self.v
        f = np.zeros_like(x)
        while t < Variables.T:
            x, v, f = self.step_vv_langevin(x, v, f)
            #TODO Periodic Bounday Conditions
            traj.append(x.copy())
            t += Variables.dt
        
        #blöderweise ist traj in der from traj[i, j, k] i=timestep, j=particle, k=x/y aber wir brauchen [j, k, i]
        traj = np.transpose(np.array(traj), (1, 2, 0))
        return traj