import numpy as np
from variables import Variables

class Particle:
    def __init__(self, x0, v0, f0, color, idx):
        self.leader: bool = False
        self.convinced: np.array = np.zeros(Variables.N_leaders)
        self.radius = Variables.particle_follower_radius

        self.x: np.array = x0
        self.v: np.array = v0
        self.f: np.array = f0
        
        self.idx = idx
        self.color = color

    def set_leader(self, i, leader_path: np.array):
        #TODO bei mehr leadern überlegen
        self.leader = True
        self.leader_path = leader_path # leader_path[i, j] mit i=time, j=position (x,y)
        if i == 0:
            self.color = (0, 0, 255)
        else:
            self.color = (255, 0, 0)
        self.radius = Variables.particle_leader_radius
        #TODO wähle farbe aus farben-set

    def update_convinced(self, r: float, i: int):
        change_rate = (1/r - self.convinced[i] * Variables.loss_factor) 
        self.convinced[i] += change_rate / Variables.fps

        #TODO Test if 1/fps is the right choice so that this is unabhängig von fps 
        self.convinced = np.where(self.convinced > 1, 1, self.convinced)  
        self.update_color(i)
    
    def update_color(self, i):
        #TODO Verwende self.convinced zum anpassen der Farbe
        # Es kann sein, dass blau und rot vertauscht sind (follower und leader unterschiedlich), weil vielleicht leader zufällig falsch herum gezogen (zuerst hoch dann niedriger index)
        self.color = np.array([round((255) * self.convinced[0]), 0, round((255) * self.convinced[1])])


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