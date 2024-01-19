import numpy as np
from variables import Variables

class Particle:
    def __init__(self, x0, v0, f0, color, mass):
        self.leader: bool = False
        self.convinced: np.array = np.zeros(Variables.N_leaders)
        self.radius = Variables.particle_follower_radius

        self.x: np.array = x0
        self.v: np.array = v0
        self.f: np.array = f0

        self.mass: float = mass
        self.color = color

    def set_leader(self):
        self.leader = True
        self.color = (255, 0, 0) # bei mehr leadern überlegen
        self.radius = Variables.particle_leader_radius
        #TODO wähle farbe aus farben-set

    def update_convinced(self, change: np.array):
        self.convinced += change
        np.where(self.convinced > 1, 1, self.convinced)  
        self.update_color()
    
    def update_color():
        #TODO Verwende self.convinced zum anpassen der Farbe
        pass

    # def __setattr__(self, name, value):
    #     # Setzte alle Kräfte, die auf den Leader wirken, auf Null.
    #     if name == 'f':
    #         if self.leader == True:
    #             val = 0
    #             super().__setattr__("f", val)
    #         else:
    #             super().__setattr__("f", value)
    #     else:
    #         super().__setattr__(name, value)

if __name__ == "__main__":
    p1 = Particle(0, 0, 1, 0, 0)
    p2 = Particle(0, 0, 1, 0, 0)

    p2.leader = True
    p1.f = 5
    p2.f = 5

    print(p1.f, p2.f)