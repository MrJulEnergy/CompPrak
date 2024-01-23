from visualize import Visualize
from variables import Variables
from simulation import Simulation
from particle import Particle

import pickle
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import curve_fit

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 15}

matplotlib.rc('font', **font)
plt.rcParams['text.usetex'] = True

with open("checkpoints/times.save", 'rb') as fp:
        data = pickle.load(fp)

t = data
N = np.arange(2, 11, 1)**2

def lin_fit(x, a, b):
        return a*x+b


log_t = np.log(t)
log_N = np.log(N)
p0 = [2, -1]
popt, pcov = curve_fit(lin_fit, log_N, log_t, p0)
print(popt)
fit_log_N = np.linspace(min(log_N), max(log_N))
fit_log_t = lin_fit(fit_log_N, *popt)

fit_N = np.exp(fit_log_N)
fit_t = np.exp(fit_log_t)


fig, ax = plt.subplots(1)

ax.scatter(N, t, color="black", label="Measurements", linewidth=3)
ax.plot(fit_N, fit_t, color="red", label="Linear-Fit", linewidth=3) 

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlabel("Particles $N$")
ax.set_ylabel("Time $t$ in s")

fig.suptitle("Time Scaling")

plt.tight_layout()
fig.legend(bbox_to_anchor=(0, 0, 1, 0), loc='center', ncol=3, fontsize=15, frameon=False)
plt.savefig("plots/times.pdf", bbox_inches='tight')
plt.show()