import matplotlib.pyplot as plt
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
dis = []
diff = 230
for disf in disfl:
    print(disf)
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
            "mi": line[7] #,
            # "mn": line[8]
        }
            for line in data]
    }
    dis.append(thisdis)

# general-graphs
for set in dis:
    fig, ax = plt.subplots(1, figsize=(6, 6), dpi=200) # , figsize=(10, 10)
    xi = [item["xi"] for item in set["data"][:]]
    xn = [item["xn"] for item in set["data"][:]]
    ci = [item["ci"] for item in set["data"][:]]
    cn = [item["cn"] for item in set["data"][:]]
    mi = [item["mi"] for item in set["data"][:]]
    # mn = [item["mn"] for item in set["data"][:]]

    iterator = range(len(xi))

    rdi = [ci[i]*xi[i] for i in iterator]
    rdn = [cn[i]*xn[i] for i in iterator]
    rri = [ci[i]*(1-xi[i]) for i in iterator]
    rrn = [cn[i]*(1-xn[i]) for i in iterator]

    iterator2 = range(int(len(xi)/diff))
    for i in iterator2:
        ax.plot([rri[i*diff], rrn[i*diff]],
                [rdi[i*diff], rdn[i*diff]], "k", lw=0.5, label="Coexisting phases")

    ax.plot(rri, rdi, "b.", markersize=1)  # linestyle="--", color=colormap(normalize(item["eb"]))
    ax.plot(rrn, rdn, "b.", markersize=1)

    plt.xlabel("$\\rho$$_r$$_0$")
    # plt.xscale("logit")
    plt.ylabel("$\\rho$$_d$$_0$")
    ax.axis([0, 5, 0, 7])
    plt.title("q =" + str(utils.specialRound(set["q"])) + ", z = " + str(utils.specialRound(set["z"])) + ", l$_p$ = " +
              str(int(set["lp"])) + ", $\epsilon$$_b$ = " + str(utils.specialRound(set["eb"])))
    # plt.legend()


#Triple point
# for eb = 1
# points = [[0.18431631631631631, 0.2178286543779437, 1.628553700436659, 1.8562338591787755, 5.305044768097405, 7.866585926893056, 69.97261564086318, 2.4649233931087027, 3.916349006345033],
#           [0.21805902951475736, 0.9480088745669762, 1.8549976355448783, 2.5126006547530886, 5.302329475722317,  7.863799847221549,  69.90110430364939,  3.9141515890719702, 1.5662357343676823],
#           [0.1844,              0.9480953030492901, 1.6283711997402792, 2.5140080190576777, 5.305054960989853,  26.646078800582224, 456.58603214048674, 2.46472615764411,   1.5658746906864125]]

# for eb = -1
points = [[0.00887056856187291, 0.07487260648847602, 3.2068893897276465, 3.6742649975006634, 12.468632296970503, 10.400504574179122, 177.33457894988854, 2.743771367155233],
          [0.07519835072903899, 0.9855779131990668, 3.6722510317326322, 5.9982876232464415, 12.464951777367602, 10.400809596478187, 177.20706506977982, 2.742842812246425],
          [0.008977325775258449, 0.9855617306559215, 3.2056219274300353, 5.997279830031542, 12.463312551487233, 50.86269646298667, 2753.642853494241, 1.0999524766047974]]

# for eb = -1.403
# points = [[0.2633, 0.26317405398238675, 1.3853103124363089, 1.6316221828822537, 4.7053328277303965, 7.574487386553928, 58.02530778020884, 2.5977574852120067, 4.224825541849652],
#           [0.2633, 0.9557579216923262, 1.6296794440513005, 2.257233728568668, 4.698167979974144, 7.567043362386871, 57.92002036710591, 4.22053835406472, 1.6077419625758038],
#           [0.2632, 0.9560318879019973, 1.3848525143550903, 2.259197651486816, 4.7014531873310546, 24.729879553311946, 373.98489786449363, 2.597564791617658, 1.6055436747336078]]

# for eb = -3
# points = [[0.6428538538538539, 0.4308730455226336, 0.828277822727259, 1.1616024831140102, 3.733238593597904, 7.191362527411241, 33.70507776023839, 2.988298184874415, 6.448031994034122],
#           [0.4307653826913457, 0.9900366059964035, 1.1617107163903868, 1.8530437315676482, 3.732957922198733, 7.1913930083977595, 33.71228083631739, 6.448878278921032, 1.5403102732340275],
#           [0.6425841947315771, 0.990031679280946, 0.8284496353823585, 1.8530579050154055, 3.7329977192037935, 21.506754617689012, 265.6551099749831, 2.98944721555445, 1.540515937110356]]

ax.plot([(1 - points[0][0]) * points[0][2], (1 - points[1][0]) * points[1][2], (1 - points[2][1]) * points[2][3], (1 - points[0][0]) * points[0][2]],
        [points[0][0] * points[0][2], points[1][0] * points[1][2], points[2][1] * points[2][3], points[0][0] * points[0][2]],
        "k--")



# plt.savefig(target_dir + "dis.png")                   # Save the general-graphs
plt.show()  # Display the general-graphs
"""
pip uninstall matplotlib cycler python-dateutil numpy pyparsing kiwisolver six
"""
