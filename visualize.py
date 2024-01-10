import pygame
import numpy as np
import math

class Visualize:
    def __init__(self, trajectory: np.array, bounds: np.array, particle_radius=10, fps=60):
        self.trajectory = trajectory  #trajectory[i, j, k]; i=particle, j=x/y, k=timestep
        self.fps = fps
        self.bounds = bounds
        self.window_size = (500, 300) 

        self.window_title = "Population Simulation"
     
        self.background_color = (32, 32, 32)

        self.particle_color = (150, 150, 150)
        self.particle_radius = particle_radius
        
        self.n_particles = self.trajectory.shape[0]
        self.n_timesteps = self.trajectory.shape[2]

        self.bounds_center = [self.bounds[1]+self.bounds[0]/2, self.bounds[3]+self.bounds[2]/2]
        self.bounds_width = self.bounds[1]-self.bounds[0]
        self.bounds_height = self.bounds[3]-self.bounds[2]
        self.bounds_aspect = self.bounds_width / self.bounds_height
        self.relevant_window_size_index = np.argmin(self.window_size)
        print(self.relevant_window_size_index)
       
        self.setup_window()
        self.run()

        
    def transform_coords(self, point: np.array):
        # relativ zur box mitte
        rel_point = point-self.bounds_center
        # jetzt von 0 bis bounds_width/height 
        new_point = rel_point + np.array([self.bounds_width, self.bounds_height])/2
        # an auflösung anpassen:
        new_new_point = new_point * np.array([self.window_size[self.relevant_window_size_index]/self.bounds_width, self.window_size[self.relevant_window_size_index]/self.bounds_height])
        # in die mitte schieben:
        new_new_new_point = new_new_point + np.array([self.window_size[self.relevant_window_size_index-1]/2, self.window_size[self.relevant_window_size_index]/2])
        return new_new_new_point
    

    def draw_grid(self):
        grid_color = (100, 100, 100)
        grid_size = 1.0

        # Calculate grid bounds in world coordinates
        grid_x_min, grid_x_max = math.floor(self.bounds[0] / grid_size) * grid_size, math.ceil(self.bounds[1] / grid_size) * grid_size
        grid_y_min, grid_y_max = math.floor(self.bounds[2] / grid_size) * grid_size, math.ceil(self.bounds[3] / grid_size) * grid_size

        # Draw vertical lines
        for x in np.arange(grid_x_min, grid_x_max + grid_size, grid_size):
            grid_pos = self.transform_coords(np.array([x, self.bounds[2]]))
            pygame.draw.line(self.screen, grid_color, (grid_pos[0], 0), (grid_pos[0], self.window_size[1]))

        # Draw horizontal lines
        for y in np.arange(grid_y_min, grid_y_max + grid_size, grid_size):
            grid_pos = self.transform_coords(np.array([self.bounds[0], y]))
            pygame.draw.line(self.screen, grid_color, (0, grid_pos[1]), (self.window_size[0], grid_pos[1]))

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
            self.draw_grid()
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
    x = np.linspace(0, 2*np.pi, 550)
    y = np.sin(x)
    traj = np.array([[x, y]])
    bounds = np.array([0, 2*np.pi, -1, 1])

    vis = Visualize(traj, fps=100, bounds=bounds)