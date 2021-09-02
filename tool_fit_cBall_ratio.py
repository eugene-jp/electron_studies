import time
start=time.time()
import numpy as np
import pandas as pn
import matplotlib.pyplot as plt
import scipy.optimize as opt

def l_wall_time(seconds):
    m, s = divmod(seconds, 60)
    return "{0:02d}min:{1:02d}s".format(int(m),int(s))
  
### signal is approximated with double-sided crystal ball
def cBall(x,alpha_l,alpha_h,n_l,n_h,mean,sigma,N):
    y=np.piecewise(x, 
                 [((x-mean)/sigma >= -alpha_l) & ((x-mean)/sigma <= alpha_h), 
                  (x-mean)/sigma < -alpha_l, 
                  (x-mean)/sigma > alpha_h], 
                 [lambda x : N*np.exp(-0.5*((x-mean)/sigma)**2), 
                  lambda x : N*np.exp(-0.5*alpha_l**2)*np.power(alpha_l/n_l*(n_l/alpha_l-alpha_l-(x-mean)/sigma),-n_l), 
                  lambda x : N*np.exp(-0.5*alpha_h**2)*np.power(alpha_h/n_h*(n_h/alpha_h-alpha_h+(x-mean)/sigma),-n_h)]
                )
    return y
### the background is STILL! assumed linear
fb = lambda x, a, b: a*x+b

print("{0}\tYea, I have the libraries".format(l_wall_time(time.time()-start)))

no,lidz=55,125
bi=lidz-no
pub="/afs/cern.ch/user/n/nstrautn/public/"
file_d=pub+"2017_data_v9_20GeV.txt"
file_mc=pub+"2017_MC_v9_20GeV.txt"
df_mc=pn.read_csv(file_mc, sep='\t',names=["mass","weights"])
df_d=pn.read_csv(file_d, sep='\t',names=["mass","redundant"])
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
parameters_d, err_d = opt.curve_fit(cBall, s_d_x, s_d_y, p0=(0.78,1.2,14,5,90,2.5,2338416)) 
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
parameters_mc, err_mc = opt.curve_fit(cBall, s_mc_x, s_mc_y, p0=(0.8,1.2,9,7,90,2.5,2675761)) 
print("{0}\tAnd extracted the signal".format(l_wall_time(time.time()-start)))

x_fit=np.linspace(no,lidz,300)
d_v_mc=s_d_y/s_mc_y

print("{0}\toh, diddly, here comes the arrangement!".format(l_wall_time(time.time()-start)))
### other decorations

plt.figure()
plt.bar(s_mc_x,s_mc_y,color="k",  align='center', alpha=0.1, label="signal in mc")
plt.plot(x_fit,cBall(x_fit,*parameters_mc),
         label="Double-sided Crystal Ball\n a_l={0:.2f},\n a_h={1:.2f},\n n_l={2:.2f},\n n_h={3:.2f},\n mean={4:.2f},\n sigma={5:.2f},\n N={6:.2f}".format(*parameters_mc)) 

plt.legend(bbox_to_anchor=(1.3, 0.8))
plt.xlabel("dielectron mass, GeV")
plt.ylabel("Frequency")
plt.ylim([0,3000000])
plt.xlim([no,lidz])
plt.title('y2017, DSCB fit, with SF, >20GeV cut')

plt.savefig("d_mc_combo_fits_wSF_cBall_v9_p1.png",bbox_inches = "tight") 
plt.show()

print("{0}\toh, diddly, here comes the ratio!".format(l_wall_time(time.time()-start)))
fig, ax = plt.subplots(2,1, figsize=(8,8), gridspec_kw={'height_ratios': [3, 1]})
ax[0].errorbar(s_d_x,s_d_y,yerr_d,fmt="k.", markerfacecolor='none',capsize=3, label="signal in data") 
ax[0].plot(x_fit,cBall(x_fit,*parameters_d),label="DSCB data fit, peak = {0:.2f} GeV".format(parameters_d[4])) 
ax[0].bar(s_mc_x,s_mc_y,color="k",  align='center', alpha=0.1, label="signal in mc")
ax[0].plot(x_fit,cBall(x_fit,*parameters_mc),label="DSCB MC fit, peak = {0:.2f} GeV".format(parameters_mc[4])) 

ax[0].legend(bbox_to_anchor=(1.3, 0.8))
ax[0].set_xlabel("dielectron mass, GeV")
ax[0].set_ylabel("Frequency")
ax[0].set_ylim([0,3000000])
ax[0].set_xlim([no,lidz])
ax[0].set_title('y2017, DSCB, with SF, >20GeV cut')

ax[1].scatter(s_d_x,d_v_mc,color="k",marker=".", facecolors='none')
ax[1].plot(s_d_x,np.ones(len(s_d_x)),lw=1,color="k",alpha=0.7,label="1.0")
ax[1].plot(s_d_x,0.8*np.ones(len(s_d_x)),lw=1,color="r",linestyle="--",alpha=0.7,label="0.8")

ax[1].set_xlabel("dielectron mass, GeV")
ax[1].set_ylabel("Data/MC")
ax[1].set_xlim([no,lidz])
ax[1].set_ylim([0.5,1.5])
ax[1].legend(loc='best')

plt.savefig("d_mc_combo_fit_wSF_cBall_ratiopl_v9_p1.png",bbox_inches = "tight") 
plt.show()
