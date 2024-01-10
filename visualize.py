import pygame
import numpy as np

class Visualize:
    def __init__(self, trajectory: np.array, bounds: np.array, particle_radius=10, fps=60):
        self.trajectory = trajectory  #trajectory[i, j, k]; i=particle, j=x/y, k=timestep
        self.fps = fps
        self.bounds = bounds
        self.window_size = (700, 500) 
        self.window_title = "Population Simulation"
     
        self.background_color = (32, 32, 32)

        self.particle_color = (150, 150, 150)
        self.particle_radius = particle_radius
        
        self.aspect_ratio = self.window_size[0]/self.window_size[1]

        self.n_particles = self.trajectory.shape[0]
        self.n_timesteps = self.trajectory.shape[2]

        self.setup_window()
        self.run()

    def transform_coords(self, point: tuple):
        x = (point[0] - self.bounds[0]) / (self.bounds[1] - self.bounds[0]) * self.window_size[0]
        y = (point[1] - self.bounds[2]) / (self.bounds[3] - self.bounds[2]) * self.window_size[1]
        return x, self.window_size[1]-y


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
    x = np.linspace(0, 2*np.pi, 250)
    y1 = np.sin(x)
    y2 = np.cos(x)

    traj = np.array([[x, y1], [x, y2]])
    bounds = np.array([-0.5, 2*np.pi+0.5, -1.5, 1.5])
    
    vis = Visualize(traj, fps=100, bounds=bounds)