import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator
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
# disfl.reverse()

NEMATIC="nematic"
ANTINEMATIC="antinematic"

# your dataset
i=0
eb = []
lp = []
dis = []
for disf in disfl :
    eb.append(float(disf.split("_")[4]))
    data = np.loadtxt( disf ).transpose()
    thisdis = {
        "type": ANTINEMATIC if disf.split("_")[0].endswith(ANTINEMATIC) else NEMATIC,
        "q":  float(disf.split("_")[1]),
        "z":  float(disf.split("_")[2]),
        "lp": float(disf.split("_")[3]),
        "eb": float(disf.split("_")[4]),
        "x":  float(disf.split("_")[5]),
        "c": float(disf.split("_")[6]),
        "data_r": data[1],
        "data_sr": data[2]
    }
    dis.append(thisdis)
    i=i+1

# setup the normalization and the colormap
normalize = plt.Normalize(min(eb), max(eb))
colormap = cm.jet

# setup subplot configuration
widths = [20, 1]
heights = [3, 1]
gs_kw = dict(height_ratios=heights, width_ratios=widths, hspace=0)
fig, axs = plt.subplots(ncols=2, nrows=2, sharex=True, figsize=(8, 6), dpi=200, gridspec_kw=gs_kw)

gs = axs[0, 1].get_gridspec()
# remove the underlying axes
for ax in axs[0:, -1]:
    ax.remove()
axbig = fig.add_subplot(gs[0:, -1])

# general-graphs
for item in dis:
    if item["type"]==NEMATIC:
        axs[0, 0].plot(item["data_r"], linewidth=2.0, linestyle="-", color=colormap(normalize(item["eb"])), label=NEMATIC)  # linestyle="--",
    elif item["type"]==ANTINEMATIC:
        axs[0, 0].plot(item["data_r"], linewidth=2.0, color=colormap(normalize(item["eb"])), label="anti-nematic")  # linestyle="-",
        index, value = max(enumerate(item["data_r"]), key=operator.itemgetter(1))
        axs[0, 0].plot(index, value, 'k.', markersize=10)

    if item["type"]==NEMATIC:
        axs[1, 0].plot(item["data_sr"], linewidth=2.0, linestyle="-", color=colormap(normalize(item["eb"])), label=NEMATIC)  # linestyle="--",
    elif item["type"]==ANTINEMATIC:
        axs[1, 0].plot(item["data_sr"], linewidth=2.0, color=colormap(normalize(item["eb"])), label="anti-nematic")  # linestyle="-",


axs[0, 0].set(xlabel="l", ylabel="\u03C1$_r$(l)", yscale="log") #
axs[0, 0].axis([-0.1, 40, 0.8e-2, 0.5])

handles, labels = axs[0, 0].get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)
axs[0, 0].legend(newHandles, newLabels)


axs[1, 0].set(xlabel="l", ylabel="S$_r$(l)")
axs[1, 0].axis([-0.1, 40, -0.51, -0.44])
axs[1, 0].hlines(-0.5, 0, 40, colors='k', linestyles='dotted')

handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)
# plt.legend(newHandles, newLabels)

# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(eb)
fig.colorbar(scalarmappaple, label='\u03B5$_b$', ax=axs, cax=axbig)


# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
fig.show()                                         # Display the general-graphs



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""