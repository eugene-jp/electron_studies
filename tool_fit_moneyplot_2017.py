# moneyplot & gathering the data
# UL 2017
import time
start=time.time()
import glob,os
import numpy as np
import pandas as pn
import matplotlib.pyplot as plt
import scipy.stats as st
import scipy.optimize as opt

def l_wall_time(seconds):
    m, s = divmod(seconds, 60)
    return "{0:02d}min:{1:02d}s".format(int(m),int(s))

print("{0}\tYea, I have the libraries".format(l_wall_time(time.time()-start)))
kur="/afs/cern.ch/user/a/angaile/public/funCondo/results/"
df_mc=pn.read_csv(kur+"2017_MC_v9_start.txt", sep='\t',names=["mass","weights","file","bunch","nBunch","amount"])
n,num=0,0
for file in glob.glob(kur+"2017_MC_v9_money_plot_*.txt"):
    n+=1
    dfa_mc=pn.read_csv(file, sep='\t',names=["mass","weights","file","bunch","nBunch","amount"])
#    print("MC {0}/{1}\t{2} has {3}".format(n,len(glob.glob(kur+"2017_MC_v9_money_plot_*.txt")),
#                                l_wall_time(time.time()-start),len(dfa_mc)))
    num+=len(dfa_mc)
    df_mc=df_mc.append(dfa_mc)

ku="/afs/cern.ch/user/a/angaile/public/funCondo/"
df_d=pn.read_csv(ku+"2017_data_start.txt", sep='\t',names=["mass","file","bunch","nBunch","amount"])
n,num=0,0
for file in glob.glob(ku+"2017_data_v9_money_plot_*.txt"):
    n+=1
    dfa_d=pn.read_csv(file, sep='\t',names=["mass","file","bunch","nBunch","amount"])
#    print("DD {0}/{1}\t{2} has {3}".format(n,len(glob.glob(ku+"2017_data_v9_money_plot_*.txt")),
#                                l_wall_time(time.time()-start),len(dfa_d)))
    num+=len(dfa_d)
    df_d=df_d.append(dfa_d)

no,lidz=80,100
bi=(lidz-no)*4
print("{0}\tJust finished importing the files, had {1}".format(l_wall_time(time.time()-start),num))

### fit for data
y_d, edges_d = np.histogram(df_d["mass"],weights=np.ones(len(df_d))*1, bins=bi, range=(no, lidz+0.1))
x_d = (edges_d[1:] + edges_d[:-1])/2
yerr_d=np.sqrt(y_d)
print("{0}\tHist-ed the data".format(l_wall_time(time.time()-start)))

### for MC we must include weights
y_mc, edges_mc = np.histogram(df_mc["mass"], weights=df_mc["weights"], bins=bi, range=(no, lidz))
x_mc = (edges_mc[1:] + edges_mc[:-1])/2
yerr_mc=np.sqrt(y_mc)
print("{0}\tHist-ed the mc".format(l_wall_time(time.time()-start)))

x_fit=np.linspace(no,lidz,300)
d_v_mc=y_d/y_mc

print("{0}\toh, diddly, here comes the ratio!".format(l_wall_time(time.time()-start)))

fig, ax = plt.subplots(2,1, figsize=(8,8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
fig.tight_layout()
ax[0].hist(df_mc["mass"], weights=df_mc["weights"],
           bins=bi, range=(no, lidz),histtype=u'stepfilled', fc='b', ec='b',lw=2, alpha=0.3,
           label="Z ee simulation",align='mid')

ax[0].errorbar(x_d,y_d,yerr_d,fmt="ko",capsize=3, label="Data")
ax[0].legend(loc=1)
ax[0].set_ylabel("Events/0.25 GeV")
ax[0].set_ylim([0,130000])
ax[0].set_xlim([no,lidz])
ax[0].set_title('Replicating THE moneyplot with full DATA')
major_ticks=np.arange(80,100,2)

ax[0].set_xticks(major_ticks)
ax[0].grid(True,linestyle=':',c="k")
ax[0].ticklabel_format(style='scientific')

ax[1].scatter(x_mc,d_v_mc,color="k",marker="o")
ax[1].plot(x_mc,np.ones(len(x_mc)),lw=2,color="k",linestyle='-.',alpha=0.7,label="1.0")
ax[1].set_xlabel("m_ee, GeV")
ax[1].set_ylabel("Data/MC")
ax[1].set_xlim([no,lidz])
ax[1].set_ylim([0.8,1.2])
major_yticks=np.arange(0.8,1.2,0.1)
ax[1].set_xticks(major_ticks)
ax[1].set_yticks(major_yticks)
ax[1].grid(True,linestyle=':',c="k")

plt.savefig("UL17_moneyplot_v4_fullData.png",bbox_inches = "tight", transparent=True)
plt.show()
