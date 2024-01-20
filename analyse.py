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

with open("checkpoints/N_49.save", 'rb') as fp:
    data = pickle.load(fp)

mean_conv_list = np.ndarray(shape = (data.shape[0], 2))
for t in range(data.shape[0]):
    mean_conv = np.mean([data[t, i].convinced for i in range(data.shape[1])], axis=0)
    mean_conv_list[t] = mean_conv

print(mean_conv_list.shape)
t = np.linspace(0, Variables.T, Variables.n_time_steps)
plt.plot(t, mean_conv_list[:, 0], color="red")
plt.plot(t, mean_conv_list[:, 1], color="blue")
plt.plot(t, np.sum(mean_conv_list, axis=1), color="black")

plt.xlabel("Time $t$ in s")
plt.ylabel("Convinced")
plt.title("Mean Convinced $C(t)$")


plt.tight_layout()
plt.savefig("plots/N_49.pdf")
plt.show()


