import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from variables import Variables
from particle import Particle

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 15}

matplotlib.rc('font', **font)
plt.rcParams['text.usetex'] = True

with open("checkpoints/dump.save", 'rb') as fp:
    data = pickle.load(fp)

# mean_conv_list = np.ndarray(shape = (data.shape[0], 2))
# std_conv_list = np.ndarray(shape = (data.shape[0], 2))
# for t in range(data.shape[0]):
#     mean_conv = np.mean([data[t, i].convinced for i in range(data.shape[1])], axis=0)
#     mean_conv_list[t] = mean_conv
#     std_conv = np.std([data[t, i].convinced for i in range(data.shape[1])], axis=0)
#     std_conv_list[t] = std_conv

# print(mean_conv_list.shape)



# Potentielle Energie aus dem LJ-Potential:
def lj_potential(p1: Particle, p2: Particle):
    energy = 0
    if not p1.leader and not p2.leader:
        r_ij = p2.x-p1.x
        r = np.linalg.norm(r_ij)
        energy += 4*( 1/r**12 - 1/r**6 )
        return energy
    if p1.leader or p2.leader:
        if p1.leader is not p2.leader:
            r_ij = p2.x-p1.x
            r = np.linalg.norm(r_ij)
            energy += 4*Variables.leader_attraction*((Variables.leader_position/r)**12 - (Variables.leader_position/r)**6)
        return energy
    else:
        return energy


kin_energys = np.ndarray(shape = (data.shape[0]))
pot_energys = np.ndarray(shape = (data.shape[0]))
for t in range(data.shape[0]):
    kin_energy = 1/2 * Variables.mass *  np.sum([np.linalg.norm(data[t, i].v)**2 for i in range(data.shape[1])])
    kin_energys[t] = kin_energy
    energy = 0
    for i in range(Variables.N):
        for j in range(Variables.N):
            if i != j:
                energy += lj_potential(data[t, i], data[t, j])
    pot_energys[t] = energy


    


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(9, 3))
t = np.linspace(0, Variables.T, Variables.n_time_steps)
ax1.plot(t, pot_energys+kin_energys, color="black", label="Total Energy")
ax2.plot(t, kin_energys, color="blue", label="Kinetic Energy")
ax3.plot(t, pot_energys, color="red", label="Potential Energy")
for a in [ax1, ax2, ax3]:
    a.set_xlabel("Time $t$ in s")
    a.set_ylabel("Energy")
fig.suptitle("Energy $E(t)$")

plt.tight_layout()
fig.legend(bbox_to_anchor=(0, 0, 1, 0), loc='center', ncol=4, fontsize=12, frameon=False)

plt.savefig("plots/N_17x17_energy.pdf", bbox_inches='tight')
plt.show()




