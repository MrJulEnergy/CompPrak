import numpy as np
from variables import Variables
import colorsys
import seaborn as sns
from matplotlib.colors import to_rgb

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

    def set_leader(self, i, leader_path):
        #TODO bei mehr leadern überlegen
        self.leader = True

        colors = 255 * np.array(sns.color_palette("bright", Variables.N_leaders))
        self.color = colors[i]

        if Variables.N_leaders == 2:
            if i == 0:
                self.color = (0, 0, 255)
            else:
                self.color = (255, 0, 0)
        self.radius = Variables.particle_leader_radius
        self.leader_path = leader_path
    
    def update_leader_pos(self, idx):
        # shift the leader position into the right direction to follow a path
        self.x += self.leader_path[:, idx]
        

    def update_convinced(self, r: float, i: int, leader_list):
        change_rate = (1/r - self.convinced[i] * Variables.loss_factor) 
        self.convinced[i] += change_rate / (Variables.fps) # durch N_leaders geteilt

        #TODO Test if 1/fps is the right choice so that this is unabhängig von fps 
        self.convinced = np.where(self.convinced > 1, 1, self.convinced)
        self.update_color(i, leader_list)
    
    def update_color(self, i, leader_list):
        #TODO Verwende self.convinced zum anpassen der Farbe
        r = round(sum(leader.color[0] * convinced for leader, convinced in zip(leader_list, self.convinced)))
        r = round(sum(leader_list[i].color[0] * self.convinced[i] for i in range(len(leader_list))))
        r = np.where(r > 255, 255, r)
        g = round(sum(leader.color[1] * convinced for leader, convinced in zip(leader_list, self.convinced)))
        g = round(sum(leader_list[i].color[1] * self.convinced[i] for i in range(len(leader_list))))
        g = np.where(g > 255, 255, g)
        b = round(sum(leader.color[2] * convinced for leader, convinced in zip(leader_list, self.convinced)))
        b = round(sum(leader_list[i].color[2] * self.convinced[i] for i in range(len(leader_list))))
        b = np.where(b > 255, 255, b)


        self.color = np.array([r, g, b])

        if Variables.N_leaders == 2:
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