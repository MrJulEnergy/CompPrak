from dataclasses import dataclass
import numpy as np

@dataclass
class Variables:
    # Animation
    fps = 60 # Bilder pro Sekunde in der Animation
    T = 10 # Zeit der Animation
    dt = 1/fps # time step 

    window_size = (500, 500)
    window_title = "Particle Simulation"
    particle_leader_radius = 10
    particle_follower_radius = 5
    particle_starting_color = (150, 150, 150)

    # Partikel
    mass = 1 # ist eigentlich egal hier
    k_B = 1 # ist auch eigentlich egal hier
    gamma = 2 # reibungsfaktor für die bewegung
    Temp = 1 # wie sehr zapplen die leute im raum

    # lattice grid
    DENSITY = 0.3 # Anfangsdichte
    N_PER_SIDE = 10
    N = N_PER_SIDE**2
    VOLUME = N / DENSITY
    box = np.ones(2) * VOLUME**(1. / 2) # für periodic boundarys sollte das hier als box verwendet werden

    # Particles
    N_leaders = 4

    # Simulation
    dumpfile = "checkpoints/dump.save"


