import time
start=time.time()
import uproot
import matplotlib.pyplot as plt
import numpy as np

print("I have the libraries")

rootfile="root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_plus5percentMaterial_102X_mcRun2_asymptotic_v8-v1/120000/07B01D04-E364-7B43-B52B-EBB19A971F8C.root"

tree = uproot.open(rootfile)["Events"]
print("I have the tree, {0:.3f} s".format(time.time()-start))

cik=300000
subsection = ["Electron_pt","nElectron","Electron_mass","Electron_eta","Electron_charge"]
ds = tree.pandas.df(subsection, entrystop=cik)
print("I have the branches, {0:.3f} s".format(time.time()-start))

el_E =[]

df=ds.query("nElectron==2")
df=df.reset_index()
print("I have the diE, {1}, {0:.3f} s".format(time.time()-start,len(df["nElectron"]))

for i in range(len(df["nElectron"])):
    if df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0:
        el_p1=df["Electron_pt"][i][0]/np.cos(np.arctan(np.exp(-df["Electron_eta"][i][0])))
        el_p2=df["Electron_pt"][i][1]/np.cos(np.arctan(np.exp(-df["Electron_eta"][i][1])))
        el_E1=(df["Electron_mass"][i][0]**2 + el_p1**2)**0.5
        el_E2=(df["Electron_mass"][i][1]**2 + el_p2**2)**0.5
        el_E.append(el_E1+el_E2)    
        
print("I have the raw data, {0:.3} s".format(time.time()-start))

#print("I shall start to draw, {0:.3f} s".format(time.time()-start))
plt.hist(el_E,bins=180,range=[0,180])
plt.xlabel("2_E, GeV")
plt.ylabel("Frequency")
plt.title("Tonis given NANOAOD, {0} entries, t={1:.0f} s".format(cik,time.time()-start))
plt.xticks(np.arange(0,190,10))
print("Ready to show, {0:.3f} s".format(time.time()-start))
plt.savefig("{0}_pilnP.png".format(cik))
#plt.show()



