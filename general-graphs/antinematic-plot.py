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
print(disfl)
disfl.reverse()

# your dataset
i=0
eb = []
lp = []
dis = []
for disf in disfl :
    eb.append(float(disf.split("_")[4]))
    data = np.loadtxt( disf ).transpose()
    thisdis = {
        "q":  float(disf.split("_")[1]),
        "z":  float(disf.split("_")[2]),
        "lp": float(disf.split("_")[3]),
        "eb": float(disf.split("_")[4]),
        "x":  float(disf.split("_")[5]),
        "c": float(disf.split("_")[6]),
        "data": data[1][0:80]
    }
    dis.append(thisdis)
    i=i+1
l = data[0]

# setup the normalization and the colormap
normalize = plt.Normalize(min(eb), max(eb))
colormap = cm.jet

# general-graphs
for item in dis:
    if item["x"]==0.05:
        plt.figure(1)
        plt.plot(item["data"], linewidth=3.0, color=colormap(normalize(item["eb"])), label="x = 0.05")  # linestyle="--",
    elif item["x"]==0.95:
        plt.figure(2)
        plt.plot(item["data"], linewidth=3.0, color=colormap(normalize(item["eb"])), label="x = 0.95")  # linestyle="-",

plt.figure(1)
# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(eb)
plt.colorbar(scalarmappaple, label='\u03B5$_b$')

plt.xlabel("l")
# plt.yscale("log")
plt.ylabel("\u03C1$_r$(l)")
plt.axis([-1, 80, 1e-10, 2])



handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)
plt.legend(newHandles, newLabels)

plt.figure(2)
# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(eb)
plt.colorbar(scalarmappaple, label='\u03B5$_b$')

plt.xlabel("l")
# plt.yscale("log")
plt.ylabel("\u03C1$_r$(l)")
plt.axis([-1, 15, 1e-3, 0.2])


handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)
plt.legend(newHandles, newLabels)


# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()                                         # Display the general-graphs



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""