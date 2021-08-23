import time
bigBang=time.time()
import uproot
import ROOT
import matplotlib.pyplot as plt
import numpy as np
import pandas as pn

def wall_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{0:.0f}h:{1:.0f}min:{2:.0f}s".format(h,m,s) #lxplus nepatik d
def l_wall_time(seconds):
    m, s = divmod(seconds, 60)
    return "{0:.0f}min:{1:.0f}s".format(m,s)

names=pn.read_csv("nosaukumi_2017_MC_v9.txt", sep='\t',names=["nos"]) 
PUweights= uproot.open("pu_weights_2017.root")["weights"].values
sf=pn.read_csv("2017_mva90_iso_quick.txt",sep="\t") #made it with the tool here in github, or find it in my public folder
print("I have the libraries and names")

notik=0
tik=len(names["nos"])
for aiziet in range(notik,tik):
    print("\n {0}/{1}, {2}".format(aiziet+1,tik,wall_time(time.time()-bigBang)))
    start=time.time()
        
    rootfile="root://cmsxrootd.fnal.gov///"+names["nos"][aiziet]
    tree = uproot.open(rootfile)["Events"]
    print(" {0}\tI have the tree".format(l_wall_time(time.time()-start)))

    el_mass = []
    el_weight = []
    subsection = ["Electron_pt","nElectron","Electron_eta",
                  "Electron_charge","Electron_phi","Pileup_nPU",
                  "Electron_mvaFall17V2Iso_WP90"]
    ds = tree.pandas.df(subsection, entrystop=-1)
    print(" {0}\tI have the branches".format(l_wall_time(time.time()-start)))

    df=ds.query("nElectron==2")
    df=df.reset_index()
    print(" {0}\tI have the diE, {1}".format(l_wall_time(time.time()-start),len(df["nElectron"])))

    for i in range(len(df["nElectron"])):
        if (df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0) and ((df["Electron_mvaFall17V2Iso_WP90"][i][0] and df["Electron_mvaFall17V2Iso_WP90"][i][1])== True):
            el1 = ROOT.TLorentzVector()
            el2 = ROOT.TLorentzVector()

            el1.SetPtEtaPhiM(df["Electron_pt"][i][0],
                             df["Electron_eta"][i][0],
                             df["Electron_phi"][i][0],0.000511)
            el2.SetPtEtaPhiM(df["Electron_pt"][i][1],
                             df["Electron_eta"][i][1],
                             df["Electron_phi"][i][1],0.000511)
            el_mass.append((el1+el2).M())   
            
            sf1,sf2=0,0 
            for mekle in range(len(sf)):
                if df["Electron_eta"][i][0]>sf["pseido_no"][mekle] and df["Electron_eta"][i][0]<sf["pseido_lidz"][mekle]:
                    if df["Electron_pt"][i][0]>sf["pt_no"][mekle] and df["Electron_pt"][i][0]<sf["pt_lidz"][mekle]:
                        sf1=sf["SF"][mekle]
                if df["Electron_eta"][i][1]>sf["pseido_no"][mekle] and df["Electron_eta"][i][1]<sf["pseido_lidz"][mekle]:
                    if df["Electron_pt"][i][1]>sf["pt_no"][mekle] and df["Electron_pt"][i][1]<sf["pt_lidz"][mekle]:
                        sf2=sf["SF"][mekle]
            
            weights = 41.48 * 5765400 * 1 * sf1 * sf2 * PUweights[df["Pileup_nPU"][i]]/102863931
            el_weight.append(weights)

    filetime=time.time()-start
    print(" {0}\tI have the raw data".format(l_wall_time(filetime)))
    print("  each {0:.2f} ms".format(1000*filetime/len(df["nElectron"])))
    #print("\nShall save")
    savetime=time.time()
    
    fo=open("2017_MC_v9_dimass_n_weights_{0}_{1}.txt".format(notik,tik),"a")
    for i in range(len(el_mass)):
        fo.write(str(el_mass[i])+"\t"+str(el_weight[i])+"\n")
    fo.close()
    
    fs=open("2017_MC_v9_progress_{0}_{1}.txt".format(notik,tik),"a")
    fs.write("{0}\t{1}\t{2}\t{3:.2f}\n".format(aiziet,wall_time(time.time()-bigBang),
                                           len(df["nElectron"]),1000*filetime/len(df["nElectron"])))
    fs.close()
    #print(" Saving took {0:.3f} s".format(time.time()-savetime))
print("{0}\tAll done".format(wall_time(time.time()-bigBang)))
