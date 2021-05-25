import numpy as np
import pandas as pn
import matplotlib.pyplot as plt

bi=180
file="2017_data.txt"
df=pn.read_csv(file, sep='\t',names=["mass"])

plt.hist(df["mass"],bins=bi,range=[0,180], alpha=0.7, histtype=u'step')
plt.xlabel("2_E, GeV")
plt.ylabel("Frequency")
plt.title("2017, data")
plt.xticks(np.arange(0,190,10))
plt.savefig("{0}.png".format(file[:-4]))
plt.show()
