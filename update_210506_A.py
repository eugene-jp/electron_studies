###
### Es meklēju failus, kas varētu būt di-el (pieņēmu, ka DoubleEG),
### interesanti, ka ir gan dati ar izteiktu pīķi, gan ne (pimais gan ir kk UL)
###

import time 
all=time.time() 
import uproot 
import ROOT
import matplotlib.pyplot as plt 
import numpy as np 

print("\nI have the libraries") 
te=["/store/data/Run2016B/DoubleEG/NANOAOD/ver1_HIPM_UL2016_MiniAODv1_NanoAODv2-v1/230000/58A35916-EF9B-6B4F-9CB6-6B499AFDDF82.root",
    "/store/data/Run2016C/DoubleEG/NANOAOD/02Apr2020-v1/230000/1B904C55-1F79-3A4B-9D9D-ABBE65C3D05E.root",
    "/store/data/Run2016D/DoubleEG/NANOAOD/Nano1June2019-v1/40000/A34362EF-A916-5E4C-B4A1-7F2DCD05F708.root"]

cik=300000
elMass=0.000511
subsection = ["Electron_pt","nElectron","Electron_mass",
	      "Electron_eta","Electron_charge","Electron_phi"]

for kurs in range(len(te)):
    start=time.time()
    print("Looking at {0}/{1}".format(kurs+1,len(te)))
    rootfile="root://cmsxrootd.fnal.gov///"+te[kurs]
    tree = uproot.open(rootfile)["Events"] 
    print(" I have the tree, {0:.3f} s".format(time.time()-start)) 

    ds =tree.pandas.df(subsection, entrystop=cik) 
    print(" I have the branches, {0:.3f} s".format(time.time()-start)) 

    el_mass =[]

    df=ds.query("nElectron==2")  
    df=df.reset_index() 
    print(" I have the diE, {1}, {0:.3f} s".format(time.time()-start,len(df["nElectron"]))) 

    for i in range(len(df["nElectron"])):
        if df["Electron_charge"][i][0]+df["Electron_charge"][i][1]== 0:
            el1_pt = df["Electron_pt"][i][0]
            el1_eta = df["Electron_eta"][i][0]
            el1_phi = df["Electron_phi"][i][0]
        
            el2_pt = df["Electron_pt"][i][1]
            el2_eta = df["Electron_eta"][i][1]
            el2_phi = df["Electron_phi"][i][1]
        
            elec1 = ROOT.TLorentzVector()
            elec2 = ROOT.TLorentzVector()
            elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, elMass)
            elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, elMass)
        
            mass = (elec1+elec2).M()
            el_mass.append(mass)
        
    print(" I have the raw data, {0:.3f} s".format(time.time()-start))
    plt.figure(kurs)
    plt.hist(el_mass,bins=90,range=[0,180], alpha=0.7, histtype=u'step') 
    plt.xlabel("2_E, GeV") 
    plt.ylabel("Frequency") 
    plt.title("{0}, {1} entries, t={2:.0f} s".format(te[kurs][-41:-5],cik,time.time()-start)) 
    plt.xticks(np.arange(0,190,10)) 
    print(" Ready to show, {0:.3f} s \n".format(time.time()-start)) 
    plt.savefig("{0}_{1}.png".format(cik,te[kurs][-41:-5]))
plt.show()
print("All together t={0:.0f} s".format(time.time()-all))
