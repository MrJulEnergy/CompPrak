import numpy as np
import matplotlib.pyplot as plt

DT = 1e-3

def W():
    # sig ist standardabweichung der normalverteilung
    sig = np.sqrt(2 * 1 * 1 * 1 / DT) # geht leider nicht mir particle.mass hier :(
    w = np.random.uniform(-1,1, size=(10000)) * sig *np.sqrt(2) # sqrt(2) weil 2d 
    return w

a = W()
print(np.mean(a), np.std(a), np.sqrt(2 * 1 * 1 * 1 / DT))
plt.hist(W())
plt.show()