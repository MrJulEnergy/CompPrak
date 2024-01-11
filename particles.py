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
        #TODO
        return np.zeros_like(x)
    
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
            traj.append(x.copy())
            t += Variables.dt
        
        #blöderweise ist traj in der from traj[i, j, k] i=timestep, j=particle, k=x/y aber wir brauchen [j, k, i]
        traj = np.transpose(np.array(traj), (1, 2, 0))
        return traj