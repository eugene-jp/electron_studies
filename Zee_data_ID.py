# Zee data, <20GeV cuts
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

names=pn.read_csv("nosaukumi_2017_data_v9.txt", sep='\t',names=["nos"]) 
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
    subsection = ["Electron_pt","nElectron","Electron_eta",
                  "Electron_charge","Electron_phi",
                  "Electron_mvaFall17V2Iso_WP90"]
    ds = tree.pandas.df(subsection, entrystop=-1)
    print(" {0}\tI have the branches".format(l_wall_time(time.time()-start)))

    df=ds.query("nElectron==2")
    df=df.reset_index()
    print(" {0}\tI have the diE, {1}".format(l_wall_time(time.time()-start),len(df["nElectron"])))

    for i in range(len(df["nElectron"])):
        if (df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0) and ((df["Electron_mvaFall17V2Iso_WP90"][i][0] and df["Electron_mvaFall17V2Iso_WP90"][i][1]) == True) and (df["Electron_pt"][i][0] > 20 and df["Electron_pt"][i][1] > 20):
            el1 = ROOT.TLorentzVector()
            el2 = ROOT.TLorentzVector()

            el1.SetPtEtaPhiM(df["Electron_pt"][i][0],
                             df["Electron_eta"][i][0],
                             df["Electron_phi"][i][0],0.000511)
            el2.SetPtEtaPhiM(df["Electron_pt"][i][1],
                             df["Electron_eta"][i][1],
                             df["Electron_phi"][i][1],0.000511)
            el_mass.append((el1+el2).M())   
            
    filetime=time.time()-start
    print(" {0}\tI have the raw data".format(l_wall_time(filetime)))
    print("  each {0:.2f} ms".format(1000*filetime/len(df["nElectron"])))
    #print("\nShall save")
    savetime=time.time()
    
    fo=open("2017_data_v9_dimass_n_weights_{0}_{1}.txt".format(notik,tik),"a")
    for i in range(len(el_mass)):
        fo.write(str(el_mass[i])+"\n")
    fo.close()
    
    fs=open("2017_data_v9_progress_{0}_{1}.txt".format(notik,tik),"a")
    fs.write("{0}\t{1}\t{2}\t{3:.2f}\n".format(aiziet,wall_time(time.time()-bigBang),
                                           len(df["nElectron"]),1000*filetime/len(df["nElectron"])))
    fs.close()
    #print(" Saving took {0:.3f} s".format(time.time()-savetime))
print("{0}\tAll done".format(wall_time(time.time()-bigBang)))
