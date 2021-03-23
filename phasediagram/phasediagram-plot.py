import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import matplotlib.cm as cm
import numpy as np
import os

import config
from utils import roddisk_utils as utils
plt.rcParams.update({'font.size': 15})


# Plot folder inside target
target_dir = config.plot_dir(__file__)
os.makedirs(target_dir, exist_ok=True)

data_dir = config.data_dir(__file__)
files = os.listdir(data_dir)

disfl = [data_dir + x for x in files if 'dat' in x]

# your dataset
i = 0
eb = []
ar = []
mn = []
lp = []
dis = []
for disf in disfl:
    print(disf)
    eb.append(float(disf.split("_")[4]))
    data = np.loadtxt(disf)
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
            "mn": line[7]
        }
            for line in data]
    }
    dis.append(thisdis)

# general-graphs
for set in dis:
    fig, ax = plt.subplots(1, figsize=(6, 6), dpi=200)  # , figsize=(10, 10)
    xi = [item["xi"] for item in set["data"][:]]
    xn = [item["xn"] for item in set["data"][:]]
    pi = [item["pi"] for item in set["data"][:]]
    ax.plot(xi, pi, "b.", markersize=1,
            label="I - (I + N)")  # linestyle="--", color=colormap(normalize(item["eb"]))
    ax.plot(xn, pi, "b.", markersize=1, label="(I + N) - N")
    plt.xlabel("x")
    # plt.xscale("logit")
    plt.ylabel("P(x)")
    ax.axis([0, 1, 3, 8])
    # ax.axis([-0.001, 2-0.999, 0, 8])
    plt.title("q =" + str(utils.specialRound(set["q"])) + ", z = " + str(utils.specialRound(set["z"])) + ", l$_p$ = " +
              str(int(set["lp"])) + ", $\epsilon$$_b$ = " + str(utils.specialRound(set["eb"])))
    # plt.legend()
    i = i + 1
    x = set["data"][5]["xi"]
    q = set["q"]
    z = set["z"]
    lp = set["lp"]
    ar.append(set["data"][5]["ar"])
    mn.append(set["data"][5]["mn"])

"""
print(eb, ar)

plt.plot(eb, ar, "r.", markersize=6,
         label="$\u03B1$$_r$")  # linestyle="--", color=colormap(normalize(item["eb"]))
plt.plot(eb, mn, "b.", markersize=6, label="m$_N$")
plt.xlabel("$\epsilon$$_b$")
# plt.xscale("logit")
plt.title("q =" + str(q) + ", z = " + str(z) + ", l$_p$ = " +
          str(lp) + ", x$_i$ = " + str(x))
plt.legend()
"""
# for eb = 1
# P = 12.463

# for eb = 1, ratio=100
# P = 0.4

# for eb = -1
# P = 5.305

# for eb = -1, ratio=25
# P = 1.59

# for eb = -1.403
# P = 4.7014531873310546

# for eb = -3
# P = 3.733

# for eb = -3, ratio=100
# P = 0.357

# for eb = 5, q=z=1
# P = 31.76

# for quadruple point
P = 4.2909

ax.hlines(P, 1e-9, 1-1e-9, colors='k', linestyles='dotted')

# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()  # Display the general-graphs

"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""
