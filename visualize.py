import pygame
import numpy as np
import math

class Visualize:
    def __init__(self, trajectory: np.array, bounds: np.array, particle_radius=10, fps=60):
        self.trajectory = trajectory  #trajectory[i, j, k]; i=particle, j=x/y, k=timestep
        self.fps = fps
        self.bounds = bounds
        self.window_size = (800, 300) 

        self.window_title = "Population Simulation"
     
        self.background_color = (32, 32, 32)

        self.particle_color = (150, 150, 150)
        self.particle_radius = particle_radius
        
        self.n_particles = self.trajectory.shape[0]
        self.n_timesteps = self.trajectory.shape[2]

        self.bounds_center = np.array([(self.bounds[1]+self.bounds[0])/2, (self.bounds[3]+self.bounds[2])/2])
        self.bounds_width = self.bounds[1]-self.bounds[0]
        self.bounds_height = self.bounds[3]-self.bounds[2]
        self.bounds_aspect = self.bounds_width / self.bounds_height
        self.window_aspect = self.window_size[0] / self.window_size[1]
        self.min_idx = np.argmin(self.window_size)
        
        self.setup_window()
        self.run()

        

    
    def transform_coords(self, point: np.array):
        rel_point = (point - self.bounds_center) * np.array([1, -1]) + np.array([self.bounds_width/2, self.bounds_height/2])
        
        
        if self.min_idx == 0:
            rel_point *= np.array([self.window_size[0]/self.bounds_width, self.window_size[0]/self.bounds_height*self.window_aspect])
        else:
            rel_point *= np.array([self.window_size[1]/self.bounds_width*self.window_aspect, self.window_size[1]/self.bounds_height])
            print(rel_point)

        return rel_point

    def setup_window(self):
        self.running = True
        self.clock = pygame.time.Clock()    
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_title)
        
        self.screen.fill(self.background_color)
        pygame.display.update()
    
    def run(self):
        i = 0
        while self.running:
            self.check_events()
            self.screen.fill(self.background_color)
            self.draw_particles(i)
            i+=1
            pygame.display.update()
            dt = self.clock.tick(self.fps) / 1000
        pygame.quit()

    def check_events(self):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                self.running = False

    def draw_particles(self, time):
        if time >= self.n_timesteps:
            self.running = False
            return
        for particle in range(self.n_particles):
            pos = self.transform_coords(self.trajectory[particle, :, time])
            pygame.draw.circle(self.screen, self.particle_color, pos, self.particle_radius)


if __name__ == "__main__":
    #x = np.linspace(0, 2*np.pi, 550)
    #y = np.sin(x)
    #traj = np.array([[x, y]])
    #bounds = np.array([0, 2*np.pi, -1, 1])

    x = np.linspace(0, 1, 250)
    y = x
    traj = np.array([[x, y]])
    bounds = np.array([0, 1, 0, 1])
    vis = Visualize(traj, fps=100, bounds=bounds)