import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from variables import Variables

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 15}

matplotlib.rc('font', **font)
plt.rcParams['text.usetex'] = True

with open("checkpoints/dump.save", 'rb') as fp:
    data = pickle.load(fp)

mean_conv_list = np.ndarray(shape = (data.shape[0], 2))
std_conv_list = np.ndarray(shape = (data.shape[0], 2))
for t in range(data.shape[0]):
    mean_conv = np.mean([data[t, i].convinced for i in range(data.shape[1])], axis=0)
    mean_conv_list[t] = mean_conv
    std_conv = np.std([data[t, i].convinced for i in range(data.shape[1])], axis=0)
    std_conv_list[t] = std_conv

print(mean_conv_list.shape)



fig, ax = plt.subplots(1)
t = np.linspace(0, Variables.T, Variables.n_time_steps)
ax.plot(t, mean_conv_list[:, 0], color="red", label="Leader 1 $\mu$")
ax.plot(t, mean_conv_list[:, 1], color="blue", label="Leader 2 $\mu$")

ax.fill_between(t, mean_conv_list[:, 0] - std_conv_list[:, 0], mean_conv_list[:, 0] + std_conv_list[:, 0], alpha=0.3, color="red", label="Leader 1 $\sigma$")
ax.fill_between(t, mean_conv_list[:, 1] - std_conv_list[:, 1], mean_conv_list[:, 1] + std_conv_list[:, 1], alpha=0.3, color="blue", label="Leader 2 $\sigma$")


ax.set_xlabel("Time $t$ in s")
ax.set_ylabel("Convinced")
fig.suptitle("Mean Convinced $C(t)$")

plt.tight_layout()
fig.legend(bbox_to_anchor=(0, 0, 1, 0), loc='center', ncol=4, fontsize=12, frameon=False)

plt.savefig("plots/N_17x17.pdf", bbox_inches='tight')
plt.show()




