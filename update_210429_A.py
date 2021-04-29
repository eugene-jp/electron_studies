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

el_pt1,el_pt2 =[], []
el_eta1,el_eta2 =[], []
el_mass1,el_mass2 =[], []
el_p1,el_p2,el_P =[],[], []
el_E1,el_E2,el_E =[],[], []

df=ds.query("nElectron==2")
df=df.reset_index()
print("I have the diE, {0:.3f} s".format(time.time()-start))

for i in range(len(df["nElectron"])):
    if df.query("nElectron==2")["Electron_charge"][i][0]+df.query("nElectron==2")["Electron_charge"][i][1] == 0:
        el_pt1.append(df.query("nElectron==2")["Electron_pt"][i][0])
        el_pt2.append(df.query("nElectron==2")["Electron_pt"][i][1])
        el_eta1.append(df.query("nElectron==2")["Electron_eta"][i][0])
        el_eta2.append(df.query("nElectron==2")["Electron_eta"][i][1])
        el_mass1.append(df.query("nElectron==2")["Electron_mass"][i][0])
        el_mass2.append(df.query("nElectron==2")["Electron_mass"][i][1])

print("I have the raw data, {0:.3} s".format(time.time()-start))
for i in range(len(el_pt1)):
    el_p1.append(el_pt1[i]/np.cos(np.arctan(np.exp(-el_eta1[i]))))
    el_p2.append(el_pt2[i]/np.cos(np.arctan(np.exp(-el_eta2[i]))))
    el_E1.append((el_mass1[i]**2 + el_p1[i]**2)**0.5)
    el_E2.append((el_mass2[i]**2 + el_p2[i]**2)**0.5)
    el_E.append(el_E1[i]+el_E2[i])

print("I shall start to draw, {0:.3f} s".format(time.time()-start))
plt.hist(el_E,bins=180,range=[0,180])
plt.xlabel("2_E, GeV")
plt.ylabel("Frequency")
plt.title("Tonis given NANOAOD, {0} entries, t={1:.0f} s".format(cik,time.time()-start))
plt.xticks(np.arange(0,190,10))
print("Ready to show, {0:.3f} s".format(time.time()-start))
plt.savefig("{0}_pilnP.png".format(cik))
#plt.show()



