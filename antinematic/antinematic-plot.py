import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

import config

# Plot folder inside target
target_dir = config.plot_dir(__file__)
os.makedirs(target_dir, exist_ok=True)

data_dir = config.data_dir(__file__)
files = os.listdir(data_dir)

disfl = [data_dir + x for x in files if 'dis' in x]

# your dataset
i=0
eb = []
lp = []
dis = []
for disf in disfl :
    eb.append(float(disf.split("_")[3])) 
    data = np.loadtxt( disf ).transpose()
    thisdis = {
        "lp": float(disf.split("_")[5]),
        "eb": float(disf.split("_")[3]),
        "data": data[1]
    }
    dis.append(thisdis)
    i=i+1
l = data[0]

# setup the normalization and the colormap
normalize = plt.Normalize(min(eb), max(eb))
colormap = cm.jet

# plot
for item in dis:
    if item["lp"]==3:
        plt.plot(item["data"], linestyle="--", color=colormap(normalize(item["eb"])), label="lp = 3")
    elif item["lp"]==10:
        plt.plot(item["data"], linestyle="-", color=colormap(normalize(item["eb"])), label="lp = 10")

# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(eb)
plt.colorbar(scalarmappaple, label='\u03B5$_b$')

plt.xlabel("l")
# plt.yscale("log")
plt.ylabel("\u03C1$_r$(l)")



handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)
plt.legend(newHandles, newLabels)




# plt.savefig(target_dir + "dis.png")                   # Save the plot
plt.show()                                         # Display the plot



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""