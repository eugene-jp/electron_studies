import time
start=time.time()
import numpy as np
import pandas as pn
import matplotlib.pyplot as plt
import scipy.stats as st
import scipy.optimize as opt

def l_wall_time(seconds):
    m, s = divmod(seconds, 60)
    return "{0:02d}min:{1:02d}s".format(int(m),int(s))

print("{0}\tYea, I have the libraries".format(l_wall_time(time.time()-start)))

### will try out the Gauss
### not sure about the double-sided part :)
#f = lambda x, a, b, c: a*st.norm.pdf(x,b,c)
f = lambda x, a, b, c,d,e,g: a*st.norm.pdf(x,b,c)+d*st.norm.pdf(x,e,g)
### the background is assumed linear
fb = lambda x, a, b: a*x+b

no,lidz=55,125
bi=lidz-no
file_d="2017_UL_data_1.txt"
file_mc="2017_MC_dimass_n_weights_0_72.txt"
df_mc=pn.read_csv(file_mc, sep='\t',names=["mass","weights"])
df_d=pn.read_csv(file_d, sep='\t',names=["mass"])
print("{0}\tJust finished importing the files".format(l_wall_time(time.time()-start)))

### fit for data
y_d, edges_d = np.histogram(df_d["mass"], bins=bi, range=(no, lidz+0.1))
x_d = (edges_d[1:] + edges_d[:-1])/2 
yerr_d=np.sqrt(y_d) 
print("{0}\tHist-ed the data".format(l_wall_time(time.time()-start)))

### I'm not sure if I haven't chosen an interval too little
bck_d=(x_d<65)|(x_d>120)
xb_d=x_d[bck_d]
yb_d=y_d[bck_d]
parametersb_d, errb_d = opt.curve_fit(fb, xb_d, yb_d, p0=(-1,1000)) 
print("{0}\tFound the bckg".format(l_wall_time(time.time()-start)))

### to extract signal: 
s_d_y=y_d-fb(x_d,*parametersb_d)
s_d_x=x_d 
parameters_d, err_d = opt.curve_fit(f, s_d_x, s_d_y, p0=(30000000,90,4,10000,90,10)) 
print("{0}\tAnd extracted the signal".format(l_wall_time(time.time()-start)))

### for MC we must include weights
y_mc, edges_mc = np.histogram(df_mc["mass"], weights=df_mc["weights"], bins=bi, range=(no, lidz)) 
x_mc = (edges_mc[1:] + edges_mc[:-1])/2 
yerr_mc=np.sqrt(y_mc) 
print("{0}\tHist-ed the mc".format(l_wall_time(time.time()-start)))

### bckg for mc
bck_mc=(x_mc<65)|(x_mc>120)
xb_mc=x_mc[bck_mc] 
yb_mc=y_mc[bck_mc] 
parametersb_mc, errb_mc = opt.curve_fit(fb, xb_mc, yb_mc, p0=(-1,1000))
print("{0}\tFound the bckg".format(l_wall_time(time.time()-start))) 

### signal in mc
s_mc_y=y_mc-fb(x_mc,*parametersb_mc)
s_mc_x=x_mc 
parameters_mc, err_mc = opt.curve_fit(f, s_mc_x, s_mc_y, p0=(30000000,90,4,10000,90,10)) 
print("{0}\tAnd extracted the signal".format(l_wall_time(time.time()-start)))

x_fit=np.linspace(no,lidz,100)
d_v_mc=s_d_y/s_mc_y

print("{0}\toh, diddly, here it comes!".format(l_wall_time(time.time()-start)))
### other decorations
fig, ax = plt.subplots(2,1, figsize=(8,8), gridspec_kw={'height_ratios': [3, 1]})
#fig.suptitle('y2017, 2Gauss fit, with PUweights, without smearing and SF', fontsize=18)

ax[0].errorbar(s_d_x,s_d_y,yerr_d,fmt="k.", markerfacecolor='none',capsize=3, label="signal in data") 
ax[0].plot(x_fit,f(x_fit,*parameters_d),label="data fit with 2G") 

ax[0].bar(s_mc_x,s_mc_y,color="k", alpha=0.1, label="signal in mc")
ax[0].plot(x_fit,f(x_fit,*parameters_mc),label="2G MC") 

ax[0].legend(loc='best')
ax[0].set_xlabel("dielectron mass, GeV")
ax[0].set_ylabel("Frequency")
ax[0].set_ylim([0,4000000])
ax[0].set_xlim([no,lidz])
ax[0].set_title('y2017, 2Gauss fit, with PUweights, without smearing and SF')

ax[1].scatter(s_d_x,d_v_mc,color="k",marker=".", facecolors='none',label="data/MC")
ax[1].legend(loc='best')
ax[1].set_xlabel("dielectron mass, GeV")
ax[1].set_ylabel("Data/MC")
ax[1].set_xlim([no,lidz])

plt.savefig("d_mc_combo_fit_wpu_2gauss_ratiopl.png",bbox_inches = "tight") 
plt.show()
