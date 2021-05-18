import time
start=time.time()
import uproot
import ROOT
import matplotlib.pyplot as plt
import numpy as np

print("\nI have the libraries")

rootfile="root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_plus5percentMaterial_102X_mcRun2_asymptotic_v8-v1/120000/07B01D04-E364-7B43-B52B-EBB19A971F8C.root"
cik=300000
subsection = ["Electron_pt","nElectron","Electron_eta","Electron_charge","Electron_phi"]

tree = uproot.open(rootfile)["Events"]
print("I have the tree, {0:.3f} s".format(time.time()-start))

ds =tree.pandas.df(subsection, entrystop=cik)
print("I have the branches, {0:.3f} s".format(time.time()-start))

el_mass =[]
labi=0
df=ds.query("nElectron==3")
df=df.reset_index()
print("I have the diE, {1}, {0:.3f} s".format(time.time()-start,len(df["nElectron"])))


for index in range(len(df["nElectron"])):
    mass=0
    for first_el in range(df["nElectron"][index]):
        for second_el in range(first_el+1,df["nElectron"][index]):
            if df["Electron_charge"][index][first_el]+df["Electron_charge"][index][second_el] == 0:
                labi+=1
                el1 = ROOT.TLorentzVector()
                el2 = ROOT.TLorentzVector()

                el1.SetPtEtaPhiM(df["Electron_pt"][index][first_el],
                                 df["Electron_eta"][index][first_el],
                                 df["Electron_phi"][index][first_el],0.000511)
                el2.SetPtEtaPhiM(df["Electron_pt"][index][second_el],
                                 df["Electron_eta"][index][second_el],
                                 df["Electron_phi"][index][second_el],0.000511)
                mass_here = (el1+el2).M()

                if np.abs(mass_here-91.2)<20:
                    if np.abs(mass_here-91.2)<np.abs(mass-91.2):
                        mass=mass_here
    if mass==0:
        break
    el_mass.append(mass)
    
print("I have the raw data, {0:.3f} s".format(time.time()-start))

print("To sum up:")
print(" Total nEl={0} ".format(df["nElectron"][0]),len(df["nElectron"]))
print(" all pairs with opposite charge, ",labi)
print(" in boundaries of 70-110,",len(el_mass))

plt.figure(0)
plt.hist(el_mass,bins=90,range=[0,180], alpha=0.7, histtype=u'step')
plt.xlabel("2_E, GeV")
plt.ylabel("Frequency")
plt.title("{0}, {1} entries, t={2:.0f} s".format(rootfile[-41:-5],cik,time.time()-start))
plt.xticks(np.arange(0,190,10))
print("Ready to show, {0:.3f} s \n".format(time.time()-start))
#plt.savefig("{0}el_{1}_{2}.png".format(df["nElectron"][0],cik,rootfile[-41:-5]))
plt.show()
