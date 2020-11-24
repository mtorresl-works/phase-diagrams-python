import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import matplotlib.cm as cm
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
    fig, ax = plt.subplots(1, figsize=(6, 6), dpi=200) # , figsize=(10, 10)
    xi = [item["xi"] for item in set["data"][:]]
    xn = [item["xn"] for item in set["data"][:]]
    pi = [item["pi"] for item in set["data"][:]]
    ax.plot(xi, pi, "b.", markersize=1,
             label="I - (I + N)")  # linestyle="--", color=colormap(normalize(item["eb"]))
    ax.plot(xn, pi, "b.", markersize=1, label="(I + N) - N")
    plt.xlabel("x")
    # plt.xscale("logit")
    plt.ylabel("P$_I$(x)")
    ax.axis([0, 1, 3, 6])
    plt.title("q =" + str(set["q"]) + ", z = " + str(set["z"]) + ", l$_p$ = " +
              str(set["lp"]) + ", $\epsilon$$_b$ = " + str(set["eb"]))
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
ax.hlines(4.760032582099456, 0, 1, colors='k', linestyles='dotted')
trans = transforms.blended_transform_factory(
    ax.get_yticklabels()[0].get_transform(), ax.transData)
ax.text(0,4.760032582099456, "{:.3f}".format(4.760032582099456), color="black", transform=trans,
        ha="right", va="center")
# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()  # Display the general-graphs

"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""
