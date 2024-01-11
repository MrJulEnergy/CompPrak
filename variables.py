from dataclasses import dataclass


@dataclass
class Variables:
    # Animation
    fps = 60 # Bilder pro Sekunde in der Animation
    T = 10 # Zeit der Animation
    dt = 1/fps

    window_size = (500, 500)
    window_title = "Particle Simulation"
    particle_radius = 10

    # Partikel
    N = 100 # anzahl der Partikel
    mass = 1 # ist eigentlich egal hier
    k_B = 1 # ist auch eigentlich egal hier
    gamma = 1 # reibungsfaktor für die bewegung
    Temp = 1 # wie sehr zapplen die leute im raum

    # Simulation
    dumpfile = "checkpoints/cp1.save"