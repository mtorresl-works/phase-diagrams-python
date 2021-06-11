import matplotlib.pyplot as plt
import numpy as np
import os

import config
plt.rcParams.update({'font.size': 15})

# Plot folder inside target
target_dir = config.plot_dir(__file__)
os.makedirs(target_dir, exist_ok=True)

data_dir = config.data_dir(__file__)
files = os.listdir(data_dir)

disfl = [data_dir + x for x in files if 'dat' in x]

NEMATIC="nematic"
ANTINEMATIC="antinematic"

# your dataset
colordata = []
dis = []

for disf in disfl :
    colordata.append(float(disf.split("_")[3]))
    data = np.loadtxt( disf )
    thisdis = {
        "q": float(disf.split("_")[1]),
        "z": float(disf.split("_")[2]),
        "lp": float(disf.split("_")[3]),
        "eb": float(disf.split("_")[4]),
        "data": [{
            "xi1": line[0],
            "xi2": line[1],
            "ci1": line[2],
            "ci2": line[3],
            "pi1": line[4],
            "ar": line[5],
            "ad": line[6],
            "mi1": line[7],
            "mi2": line[8]
        }
            for line in data]
    }
    dis.append(thisdis)
eb = data[0]
# general-graphs
fig, ax = plt.subplots(1, figsize=(4,3.5), dpi=200)

for item in dis:
    pi = [item["data"][i]["pi1"] for i in range(len(item["data"]))]
    mi1 = [item["data"][i]["mi1"] for i in range(len(item["data"]))]
    mi2 = [1/item["data"][i]["mi2"] for i in range(len(item["data"]))]

    ax.plot(mi1, pi, linewidth=3.0, color="k", linestyle="-", label="$I_1$")
    # ax.set_yticks(np.arange(6.8, 7.4, 0.1))
    # ax.set_ylim(6.82,7.2)
    # ax.set_xlim(0,3)
    # ax.set_xticks(np.arange(0, 0.5, 0.1))

    ax.plot(mi2, pi, linewidth=3.0, color="k", linestyle="--", label="$I_2$")
    # ax.set_yticks(np.arange(36, 92, 12))
    # ax.set_ylim(0,3)
    ax.set(xlabel='$m_{I}$', ylabel='P')

# plt.xlabel('x')
# plt.yscale("log")
# plt.ylabel("COSAS")
# plt.axis([0, 0.4, 0.1, 100])
plt.legend(loc='upper center')


# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()                                         # Display the general-graphs



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""