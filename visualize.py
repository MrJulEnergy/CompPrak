import pygame
import numpy as np
from variables import Variables

class Visualize:
    def __init__(self, trajectory: np.array, bounds: np.array):
        self.trajectory = trajectory  #trajectory[i, j, k]; i=particle, j=x/y, k=timestep
        self.fps = Variables.fps
        self.bounds = bounds

        self.window_size = Variables.window_size
        self.window_title = Variables.window_title
     
        self.background_color = (32, 32, 32)

        self.particle_color = (150, 150, 150)
        self.particle_radius = Variables.particle_radius
        
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

    def transform_coords(self, point):
        x, y = point

        norm_x = (x - self.bounds[0]) / (self.bounds[1] - self.bounds[0])
        norm_y = (y - self.bounds[2]) / (self.bounds[3] - self.bounds[2])
        
        if self.bounds_aspect > self.window_aspect:
            scaled_x = norm_x * self.window_size[0]
            scaled_y = norm_y * self.window_size[0]

        else:
            scaled_x = norm_x * self.window_size[1]
            scaled_y = norm_y * self.window_size[1]
        
        return scaled_x, self.window_size[1]-scaled_y

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
    x = np.linspace(0, 1, 250)
    y = x
    traj = np.array([[x, y]])
    bounds = np.array([0, 1, 0, 1])
    print(traj.shape)
    vis = Visualize(traj, bounds=bounds)