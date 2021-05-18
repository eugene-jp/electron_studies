import ROOT
import time
start=time.time()
import uproot
import matplotlib.pyplot as plt
import numpy as np
import math as math

print("I have the libraries")

failanosaukums="root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_plus5percentMaterial_102X_mcRun2_asymptotic_v8-v1/120000/07B01D04-E364-7B43-B52B-EBB19A971F8C.root"

tree = uproot.open(failanosaukums)["Events"]

print("I have the tree, {0:.3f} s".format(time.time()-start))

subsection = ["Electron_pt","nElectron","Electron_mass","Electron_eta","Electron_charge","Electron_phi"]

df = tree.pandas.df(subsection, entrystop=300000)

print("I have the branches, {0:.3f} s".format(time.time()-start))

ds = df.query("nElectron==2")
ds = ds.reset_index()

print("I have the diE, {1}, {0:.3f} s".format(time.time()-start,len(df["nElectron"])))

elMass = 0.000511
el_cosine = []
el_mass = []
        
for i in range(len(ds["nElectron"])):
    if ds["Electron_charge"][i][0]+ds["Electron_charge"][i][1] == 0:
    
        el1_pt = ds["Electron_pt"][i][0]
        el1_eta = ds["Electron_eta"][i][0]
        el1_phi = ds["Electron_phi"][i][0]
        el2_pt = ds["Electron_pt"][i][1]
        el2_eta = ds["Electron_eta"][i][1]
        el2_phi = ds["Electron_phi"][i][1]
        
        elec1 = ROOT.TLorentzVector()
        elec2 = ROOT.TLorentzVector()
        elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, elMass)
        elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, elMass)
        cosine = math.cos(elec1.Angle(elec2.Vect()))
        mass = (elec1+elec2).M()
        el_cosine.append(cosine)
        el_mass.append(mass)
        
print("I have the raw data, {0:.3} s".format(time.time()-start))

#plt.hist(el_E,bins=180,range=[0,180], alpha=0.7, histtype=u'step')
plt.hist(el_mass,bins=180,range=[0,180])
plt.xlabel("2_M, GeV")
plt.ylabel("Frequency")
plt.title("Last week's Toni given NANOAOD file from DAS with 300000 entries (30%)")
plt.xticks(np.arange(0,190,10))

print("Ready to show, {0:.3f} s".format(time.time()-start))

plt.show()
