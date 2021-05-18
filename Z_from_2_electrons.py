import ROOT
import time
start=time.time()
import uproot
import matplotlib.pyplot as plt
import numpy as np
import math as math

#Salidzinajums // Comparison

print("I have the libraries")

rootfile="root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_plus5percentMaterial_102X_mcRun2_asymptotic_v8-v1/120000/07B01D04-E364-7B43-B52B-EBB19A971F8C.root"

tree = uproot.open(rootfile)["Events"]
print("I have the tree, {0:.3f} s".format(time.time()-start))

cik=100000
subsection = ["Electron_pt","nElectron","Electron_mass","Electron_eta","Electron_charge","Electron_phi"]
ds = tree.pandas.df(subsection, entrystop=cik)
print("I have the branches, {0:.3f} s".format(time.time()-start))

el_inv =[]

df=ds.query("nElectron==2")
df=df.reset_index()
print("I have the diE, {1}, {0:.3f} s".format(time.time()-start,len(df["nElectron"])))

el_mass = 0.000511
Z_mass = []
for i in range(len(df["nElectron"])):
    if df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0:
        
        
        el1_pt = df["Electron_pt"][i][0]
        el1_eta = df["Electron_eta"][i][0]
        el1_phi = df["Electron_phi"][i][0]
        el2_pt = df["Electron_pt"][i][1]
        el2_eta = df["Electron_eta"][i][1]
        el2_phi = df["Electron_phi"][i][1]
        
        elec1 = ROOT.TLorentzVector()
        elec2 = ROOT.TLorentzVector()
        elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, el_mass)
        elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, el_mass)
        cosine = math.cos(elec1.Angle(elec2.Vect()))
        mass = (elec1+elec2).M()
        el_inv.append(mass)
        
        
        
        #el_p1=df["Electron_pt"][i][0]/np.cos(np.arctan(np.exp(-df["Electron_eta"][i][0])))   # Commented first version, which gave wrong results....
        #el_p2=df["Electron_pt"][i][1]/np.cos(np.arctan(np.exp(-df["Electron_eta"][i][1])))
        #el_E1=(el_mass**2 + el_p1**2)**0.5
        #el_E2=(el_mass**2 + el_p2**2)**0.5
        #invariant = el_mass**2 + el_mass**2 + 2*(el_E1*el_E2-(elec1.Px()*elec2.Px()+elec1.Py()*elec1.Py()+elec1.Pz()*elec1.Pz()))
        #print(invariant)
        invariant2 = 2*el1_pt*el2_pt*(math.cosh(el1_eta-el2_eta)-math.cos(el1_phi-el2_phi))
        print(invariant2)
        Z_mass.append((invariant2)**0.5)
        
           
        
print("I have the raw data, {0:.3} s".format(time.time()-start))

#print("I shall start to draw, {0:.3f} s".format(time.time()-start))
plt.figure(1)
plt.hist(Z_mass,bins=180,range=[0,180], alpha=0.7, histtype=u'step')
plt.figure(2)
plt.hist(el_inv,bins=180,range=[0,180], alpha=0.7, histtype=u'step')
plt.xlabel("M, GeV")
plt.ylabel("Frequency")
plt.title("Tonis given NANOAOD, {0} entries, t={1:.0f} s".format(cik,time.time()-start))
plt.xticks(np.arange(0,190,10))
print("Ready to show, {0:.3f} s".format(time.time()-start))
#plt.savefig("{0}_pilnP.png".format(cik))
plt.show()
