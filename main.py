import pygame
import numpy as np

class Visualize:
    def __init__(self, trajectory: np.array, circle_radius=10, fps=60):
        self.trajectory = trajectory  #trajectory[i, j, k]; i=particle, j=x/y, k=timestep
        self.fps = fps

        #TODO Adjust trajectory to windowsize (extent)
        #TODO periodic boundary conds.

        self.n_particles = self.trajectory.shape[0]
        self.n_timesteps = self.trajectory.shape[2]

        self.background_color = (32, 32, 32)
        self.circle_color = (150, 150, 150)
        self.circle_radius = circle_radius
        self.window_size = (700, 400)
        self.window_title = "Population Simulation"

        self.setup_window()
        self.run()

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
            pygame.draw.circle(self.screen, self.circle_color, self.trajectory[particle, :, time], self.circle_radius)

if __name__ == "__main__":
    traj = np.random.random(size=(10, 2, 500))
    traj[:, 0, :] = 700*traj[:, 0, :]
    traj[:, 1, :] = 400*traj[:, 1, :]
    vis = Visualize(traj, fps=100)