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
    data = np.loadtxt( disf ).transpose()
    thisdis = {
        "type": ANTINEMATIC if disf.split("_")[0].endswith(ANTINEMATIC) else NEMATIC,
        "q":  float(disf.split("_")[1]),
        "z":  float(disf.split("_")[2]),
        "lp": float(disf.split("_")[3]),
        "x":  float(disf.split("_")[4]),
        "c": float(disf.split("_")[5]),
        "max": data[1],
        "position": data[2]
    }
    dis.append(thisdis)
eb = data[0]
# general-graphs
fig, ax = plt.subplots(1, figsize=(4,3.5), dpi=200)
for item in dis:
    if item["type"]==ANTINEMATIC:
        ax.plot(eb, item["position"], linewidth=4.0, color="k", linestyle="-", label="$\ell_p = $"+str(item["lp"]))  # linestyle="-",

plt.xlabel('\u03B5$_b$')
plt.yscale("log")
plt.ylabel("$MPL$")
plt.axis([1, -10, 1, 1200])

# plt.legend()


# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()                                         # Display the general-graphs



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""