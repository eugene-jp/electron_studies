import uproot
import matplotlib.pyplot as plt
import numpy as np

failanosaukums="root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_plus5percentMaterial_102X_mcRun2_asymptotic_v8-v1/120000/07B01D04-E364-7B43-B52B-EBB19A971F8C.root"

tree = uproot.open(failanosaukums)["Events"]

subsection = ["Electron_pt","nElectron"]

df = tree.pandas.df(subsection, entrystop=1000)

tukss = [] #just ingore this line
el_pt1 = []
el_pt2 = []
el_pt = []

for i in range(len(df["nElectron"])): # takes first electron's pt
    try:
        el_pt1.append(df.query("nElectron==2")["Electron_pt"][i][0])
    except:
        tukss.append(i) # ignore, didnt know what to put here, otherwise there is error


for i in range(len(df["nElectron"])): # takes second electron's pt
    try:
        el_pt2.append(df.query("nElectron==2")["Electron_pt"][i][1])
    except:
        tukss.append(i) # same as above

        
for i in range(len(el_pt1)): # adds both pt's together
    el_pt.append(el_pt1[i]+el_pt2[i])
    
    
plt.hist(el_pt,bins=180,range=[0,180])
plt.xlabel("2el_pt, GeV")
plt.ylabel("Frequency")
plt.title("Last week's Toni given NANOAOD file from DAS with 100000 entries (10%)")
plt.xticks(np.arange(0,190,10))

plt.show()
