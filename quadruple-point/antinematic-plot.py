import matplotlib.pyplot as plt
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
colordata = []
dis = []
zz = []

for disf in disfl :
    # print(disf)
    data = np.loadtxt(disf).transpose()
    zz.append(float(disf.split("_")[1]))
    colordata.append(float(disf.split("_")[1]))
    thisdis = {
        "qq":  data[0],
        "lp":  float(disf.split("_")[2]),
        "zz":  float(disf.split("_")[1]),
        "ci1":  data[2],
        "xxi1": data[3],
        "ci2":  data[4],
        "xxi2": data[5],
        "cn": data[6],
        "xxn": data[7],
        "arn": data[8],
        "adn": data[9],
        "ca": data[10],
        "xxa": data[11],
        "ara": data[12],
        "ada": data[13],
        "eb": data[14]
    }
    dis.append(thisdis)


# setup the normalization and the colormap
normalize = plt.Normalize(min(zz), max(zz))
colormap = cm.coolwarm

# general-graphs
fig, ax = plt.subplots(1, figsize=(6,5), dpi=200)
for item in dis:
    if True: # item["type"]==ANTINEMATIC:
        ax.plot(item["eb"], item["qq"], linewidth=0.5, linestyle="-", color=colormap(normalize(item["zz"])), label="$z = $"+str(item["zz"]))  # linestyle="-",
        print(item["eb"][0])

plt.xlabel('\u03B5$_b$')
# plt.yscale("log")
plt.ylabel("$q$")
plt.axis([-2.5, 2.9, 2.5, 3.8])

# plt.legend()

# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(zz)
fig.colorbar(scalarmappaple, label='$z$', ax=ax)


# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()                                         # Display the general-graphs



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""