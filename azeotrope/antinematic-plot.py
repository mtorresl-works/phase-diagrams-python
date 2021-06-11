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
            "xi": line[0],
            "xn": line[1],
            "ci": line[2],
            "cn": line[3],
            "pi": line[4],
            "ar": line[5],
            "ad": line[6],
            "mi": line[7],
            "mn": line[8]
        }
            for line in data]
    }
    dis.append(thisdis)
eb = data[0]
# general-graphs
fig = plt.figure(figsize=(4, 4), dpi=200)
gs = fig.add_gridspec(3, hspace=0)
ax = gs.subplots(sharex=True)

for item in dis:
    xi = [item["data"][i]["xn"] for i in range(len(item["data"]))]
    xn = [item["data"][i]["xn"] for i in range(len(item["data"]))]
    ar = [item["data"][i]["ar"] for i in range(len(item["data"]))]
    ad = [item["data"][i]["ad"] for i in range(len(item["data"]))]
    mi = [item["data"][i]["mi"] for i in range(len(item["data"]))]
    mn = [item["data"][i]["mn"] for i in range(len(item["data"]))]
    print(ar)
    ax[0].plot(xn, ar, linewidth=3.0, color="b", linestyle="-", label="ar")
    ax[0].set_yticks(np.arange(6.8, 7.4, 0.2))
    ax[0].set_ylim(6.82,7.2)
    ax[0].set_xlim(0,0.4)
    ax[0].set_xticks(np.arange(0, 0.5, 0.1))
    ax[0].set(xlabel='x', ylabel='$\\alpha_{r }$')

    ax[1].plot(xn, ad, linewidth=3.0, color="r", linestyle="-", label="ad")
    ax[1].set_yticks(np.arange(36, 92, 24))
    ax[1].set_ylim(30,90)
    ax[1].set(xlabel='x', ylabel='$\\alpha_{d }$')

    ax[2].plot(xn, mn, linewidth=3.0, color="k", linestyle="-", label="$N^+$")
    ax[2].plot(xi, mi, linewidth=3.0, color="k", linestyle=":", label="$I$")
    ax[2].set_yticks(np.arange(4.5, 11.5, 3.8))
    ax[2].set_ylim(2.8,11.5)
    ax[2].set(xlabel='x', ylabel='$m_{I,N^+}$')
    ax[2].legend(loc="upper right", prop={'size': 8.5})

# plt.xlabel('x')
# plt.yscale("log")
# plt.ylabel("COSAS")
# plt.axis([0, 0.4, 0.1, 100])


# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()                                         # Display the general-graphs



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""