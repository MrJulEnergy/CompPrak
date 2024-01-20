from dataclasses import dataclass
import numpy as np

@dataclass
class Variables:
    # Animation
    fps = 60 # Bilder pro Sekunde in der Animation
    T = 20 # Zeit der Animation
    dt = 1/fps # time step 
    n_time_steps = int(T*fps)

    window_size = (500, 500)
    background_color = (32, 32, 32)
    window_title = "Particle Simulation"
    particle_leader_radius = 7
    particle_follower_radius = 5
    particle_starting_color = np.array([0, 0, 0])

    # Partikel
    mass = 1 # ist eigentlich egal hier
    k_B = 1 # ist auch eigentlich egal hier
    gamma = 4 # reibungsfaktor für die bewegung
    Temp = 1 # wie sehr zapplen die leute im raum

    # lattice grid
    DENSITY = 0.3 # Anfangsdichte
    N_PER_SIDE = 7
    N = N_PER_SIDE**2
    VOLUME = N / DENSITY
    box = np.ones(2) * VOLUME**(1. / 2) # für periodic boundarys sollte das hier als box verwendet werden

    # Particles
    N_leaders = 2 # anzahl an leader (aktuell nur 2 möglich solange die farben manuell gewählt werden.)
    loss_factor = 1 # verlust an convincedheit pro sekunde
    
    # leader force
    leader_attraction = 40 # potentialtopf tiefe (anziehungsstärke zwischen leader und follower)
    leader_position = 1.2 # potentialtopf position (normaler abstand zwischen leader und follower)

    # Simulation
    dumpfile = "checkpoints/N_49.save"


