import uproot
import math as m
import matplotlib.pyplot as plt
import numpy as np

FileName="root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_plus5percentMaterial_102X_mcRun2_asymptotic_v8-v1/120000/07B01D04-E364-7B43-B52B-EBB19A971F8C.root"

tree = uproot.open(FileName)["Events"]

subsection = ["Electron_pt","nElectron","Electron_mass","Electron_eta","Electron_charge"]

df = tree.pandas.df(subsection, entrystop=300000)


tukss = [] # For error fighting purposes
el_pt1 = [] # 1st e pt
el_pt2 = [] # 2nd e pt
el_eta1 = [] # 1st e eta
el_eta2 = [] # 2nd e eta
el_mass1 = [] # 1st e mass
el_mass2 = [] # 2nd e mass
el_p1 = [] # 1st e full P 3D
el_p2 = [] # 2nd e full P 3D
el_P = []
el_E1 = [] # 1st e full E
el_E2 = [] # 2nd e full E
el_E = [] # Full E of the pair



for i in range(len(df["nElectron"])):
    try:
          if df.query("nElectron==2")["Electron_charge"][i][0]+df.query("nElectron==2")["Electron_charge"][i][1] == 0: # Take only pair of electron and positron SUM(charge)=0
              el_pt1.append(df.query("nElectron==2")["Electron_pt"][i][0])     # We get list of pt_1
              el_pt2.append(df.query("nElectron==2")["Electron_pt"][i][1])     # We get list of pt_2
              el_eta1.append(df.query("nElectron==2")["Electron_eta"][i][0])   # We get list of eta_1
              el_eta2.append(df.query("nElectron==2")["Electron_eta"][i][1])   # We get list of eta_2
              el_mass1.append(df.query("nElectron==2")["Electron_mass"][i][0]) # We get 1st mass
              el_mass2.append(df.query("nElectron==2")["Electron_mass"][i][1]) # We get 2nd mass
          else:
              continue
    except:
        tukss.append(i) # Anti-error line


for i in range(len(el_pt1)):
    try:
        el_p1.append(el_pt1[i]/m.cos(m.atan(m.exp(-el_eta1[i]))))  # We get list of P1
        el_p2.append(el_pt2[i]/m.cos(m.atan(m.exp(-el_eta2[i]))))  # We get list of P2
        #el_P.append(el_p1[i]+el_p2[i])                            # We get list of P of both electrons combined. Kinda questionable....
    except:
        tukss.append(i) # Anti-error line



for i in range(len(el_mass1)):
    try:
        el_E1.append((el_mass1[i]**2 + el_p1[i]**2)**0.5) # Energy of 1st electron E^2=p^2+m^2
        el_E2.append((el_mass2[i]**2 + el_p2[i]**2)**0.5) # Energy of 2nd electron
        el_E.append(el_E1[i]+el_E2[i])                    # Sum of energies of both electrons
    except:
        tukss.append(i) # Anti-error line


        
plt.hist(el_E,bins=180,range=[0,180])
plt.xlabel("2_E, GeV")
plt.ylabel("Frequency")
plt.title("Last week's Toni given NANOAOD file from DAS with 300000 entries (30%)")
plt.xticks(np.arange(0,190,10))

plt.show()
