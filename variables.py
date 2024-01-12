from dataclasses import dataclass
import numpy as np

@dataclass
class Variables:
    # Animation
    fps = 60 # Bilder pro Sekunde in der Animation
    T = 20 # Zeit der Animation
    dt = 1/fps # time step 

    window_size = (500, 500)
    window_title = "Particle Simulation"
    particle_radius = 10

    # Partikel
    mass = 1 # ist eigentlich egal hier
    k_B = 1 # ist auch eigentlich egal hier
    gamma = 1 # reibungsfaktor für die bewegung
    Temp = 1 # wie sehr zapplen die leute im raum

    # lattice grid
    DENSITY = 0.3 # Anfangsdichte
    N_PER_SIDE = 10
    N = N_PER_SIDE**2
    VOLUME = N / DENSITY
    box = np.ones(2) * VOLUME**(1. / 2) # für periodic boundarys sollte das hier als box verwendet werden


    # Simulation
    dumpfile = "checkpoints/dump.save"


