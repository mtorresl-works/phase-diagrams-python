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
qq = []

for disf in disfl :
    data = np.loadtxt(disf).transpose()
    qq.append(float(disf.split("_")[1]))
    colordata.append(float(disf.split("_")[1]))
    thisdis = {
        "qq":  float(disf.split("_")[1]),
        "lp":  float(disf.split("_")[2]),
        "zz":  data[1],
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
normalize = plt.Normalize(min(qq), max(qq))
colormap = cm.coolwarm

# general-graphs
eb=[]
qq = sorted(qq)
Q, Z = np.meshgrid(qq, dis[0]["zz"])
newdis = sorted(dis, key=lambda k: k['qq'])
# fig, ax = plt.subplots(1, figsize=(6,5), dpi=200, projection='3d')
for item in newdis:
    for i in range(len(item["zz"])):
        eb.append(item["eb"][i])
fig = plt.figure(1, figsize=(6,5), dpi=200)
ax = plt.axes(projection='3d')

Q = np.reshape(Q, (300, 300))
Z = np.reshape(Z, (300, 300))
eb = np.reshape(eb, (300, 300))
ax.plot_surface(Q, Z, eb, rstride=1, cstride=1,
                cmap=colormap, edgecolor='none')

ax.set_xlabel("$q$")
ax.set_ylabel("$z$")
ax.set_zlabel('\u03B5$_b$')

ax.set_xlim(Q.min(), Q.max())
ax.set_ylim(0, 12)
ax.set_zlim(-2.5, 2.9)

#
# for item in dis:
#     ax.plot(item["eb"], item["zz"], linewidth=2.0, linestyle="-", color=colormap(normalize(item["qq"])), label="$q = $"+str(item["qq"]))  # linestyle="-",
#
# plt.xlabel('\u03B5$_b$')
# # plt.yscale("log")
# plt.ylabel("$z$")
# plt.axis([-2.5, 2.9, 0, 12])
#
# # plt.legend()
#
# # setup the colorbar
# scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
# scalarmappaple.set_array(qq)
# fig.colorbar(scalarmappaple, label='$q$', ax=ax)


# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()                                         # Display the general-graphs



"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""