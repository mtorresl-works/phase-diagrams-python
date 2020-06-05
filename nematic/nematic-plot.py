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
dis = []
for disf in disfl :
    eb.append(float(disf.split("_")[3])) 
    data = np.loadtxt( disf ).transpose()
    dis.append(data[1])
    i=i+1
l = data[0]

# setup the normalization and the colormap
normalize = plt.Normalize(min(eb), max(eb))
colormap = cm.jet

# plot
i=0
for n in eb:
    plt.plot(dis[i], color=colormap(normalize(n)))
    i=i+1

# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(eb)
plt.colorbar(scalarmappaple, label='\u03B5$_b$')

plt.xlabel("l")
plt.yscale("log")
plt.ylabel("\u03C1$_r$(l)")
# plt.savefig(target_dir + "dis.png")                   # Save the plot
plt.show()                                         # Display the plot



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""