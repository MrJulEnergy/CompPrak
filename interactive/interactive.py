import sys
sys.path.append('../CP') 
import pygame
import numpy as np
from variables import Variables
from interactive_simulation import Simulation
from setup_system import Setup




class Visualize:
    def __init__(self, particles: np.array, bounds: np.array):
        self.particles = particles  #particles[i, j]; i=timestep, j=particle
        self.fps = Variables.fps
        self.bounds = bounds

        self.window_size = Variables.window_size
        self.window_title = Variables.window_title
        self.background_color = Variables.background_color

        self.n_timesteps = Variables.n_time_steps
        
        self.setup_window()
        self.run()

    def transform_coords(self, point):
        x, y = point

        norm_x = (x - self.bounds[0]) / (self.bounds[1] - self.bounds[0])
        norm_y = (y - self.bounds[2]) / (self.bounds[3] - self.bounds[2])
    
        scaled_x = norm_x * self.window_size[1]
        scaled_y = norm_y * self.window_size[1]
        return scaled_x, self.window_size[1]-scaled_y
    
    def inverse_transform_coords(self, screen_point):
        scaled_x, scaled_y = screen_point

        norm_x = scaled_x / self.window_size[1]
        norm_y = (self.window_size[1] - scaled_y) / self.window_size[1]

        x = norm_x * (self.bounds[1] - self.bounds[0]) + self.bounds[0]
        y = norm_y * (self.bounds[3] - self.bounds[2]) + self.bounds[2]

        return np.array([x, y])

    def setup_window(self):
        self.running = True
        self.clock = pygame.time.Clock()    
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_title)
        
        self.screen.fill(self.background_color)
        pygame.display.update()

    def show_fps(self):
        fps_font = pygame.font.Font(None, 36)
        fps_text = fps_font.render(f"FPS: {round(self.clock.get_fps())}", True, pygame.Color("white"))
        self.screen.blit(fps_text, (10, 10))

    def run(self):
        sim = Simulation(self.particles)
        integrator_generator = sim.run()
        while self.running:
            pos = self.check_events()
            if pos is not None:
                pos = self.inverse_transform_coords(pos)
                sim.mouse_force(pos)
                
            self.screen.fill(self.background_color)
            self.particles = next(integrator_generator)
            self.draw_particles()
            self.show_fps()
            pygame.display.update()
            dt = self.clock.tick(self.fps) / 1000
        pygame.quit()

    def check_events(self):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Return the mouse click position
                    return event.pos
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button is held down
                    # Return the mouse position during drag
                    return event.pos
        return None  # Return None if no relevant event is detected


    def draw_particles(self):
        for particle in range(Variables.N):
            pos = self.particles[particle].x
            transformed_pos = self.transform_coords(pos)
            pygame.draw.circle(self.screen, self.particles[particle].color, transformed_pos, self.particles[particle].radius)

if __name__ == "__main__":
    print("[LOG] Setup: Erstellen der Teilchen")
    sys = Setup()
    particles = sys.setup()

    bounds = [0, Variables.box[0], 0, Variables.box[1]]
    vis = Visualize(particles, bounds)
