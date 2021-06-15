import numpy as np
import pandas as pn
import matplotlib.pyplot as plt

bi=180
koef=2.33
file_d="2017_UL_data_1.txt"
file_mc="2017_UL_mc.txt"
df_d=pn.read_csv(file_d, sep='\t',names=["mass"])
df_mc=pn.read_csv(file_mc, sep='\t',names=["mass"])

y, edges = np.histogram(df_d["mass"], bins=bi, range=(0, 180))
x = (edges[1:] + edges[:-1])/2

plt.hist(df_mc["mass"],bins=bi,range=[0,180], alpha=0.7,
                 histtype=u'step',weights=np.ones(len(df_mc["mass"]))*koef,label="MC")
plt.errorbar(x,y,yerr=yerr=np.sqrt(y),fmt="o",capsize=3,label="Data")
plt.xlabel("2_E, GeV")
plt.ylabel("Frequency")
plt.title("y2017, koef={0}".format(koef))
plt.xticks(np.arange(0,190,10))
plt.ylim([0,4000000])
plt.xlim([55,125])
plt.legend(loc="best")
plt.savefig("d_mc_combo_{0}.png".format(koef))
plt.show()
