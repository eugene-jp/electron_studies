# ar argumentiem, biezu saglabasanu
# Zee data, money plots
# 2017. gadam

import time
bigBang=time.time()
import uproot
import ROOT
import numpy as np
import pandas as pn
import sys 

def wall_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{0:.0f}h:{1:.0f}min:{2:.0f}s".format(h,m,s) #lxplus nepatik d
def l_wall_time(seconds):
    m, s = divmod(seconds, 60)
    return "{0:.0f}min:{1:.0f}s".format(m,s)

names=pn.read_csv("all_files_2017_UL_Nv9.txt", sep='\t',names=["nos"]) 
print("I have the libraries and names")

notik=int(sys.argv[1])
tik=int(sys.argv[2])#len(names["nos"])
if tik>len(names["nos"]):
    tik=len(names["nos"])
for aiziet in range(notik,tik):
    print("\n {0}/{1}, {2}".format(aiziet+1,tik,wall_time(time.time()-bigBang)))
    start=time.time()
        
    rootfile="root://cmsxrootd.fnal.gov///"+names["nos"][aiziet]
    tree = uproot.open(rootfile)["Events"]
    print(" {0}\tI have the tree".format(l_wall_time(time.time()-start)))

    subsection = ["Electron_pt","nElectron","Electron_eta",
                  "Electron_charge","Electron_phi",
                  "Electron_cutBased","Electron_r9"]
    ds = tree.pandas.df(subsection, entrystop=-1)
    print(" {0}\tI have the branches".format(l_wall_time(time.time()-start)))

    df=ds.query("nElectron==2")
    df=df.reset_index()
    print(" {0}\tI have the diE, {1}".format(l_wall_time(time.time()-start),len(df["nElectron"])))
    
    cik=50000
    dala=divmod(len(df["nElectron"]),cik)[0]
    if divmod(len(df["nElectron"]),cik)[1]>0:
        dala=dala+1
        
    for jauns in range(dala):
        start=time.time()
        el_mass = []
        print(" {0}\tStarting {1}/{2}".format(l_wall_time(time.time()-start),jauns+1,dala))
        nno=jauns*cik
        lidz=(jauns+1)*cik
        if lidz>len(df["nElectron"]):
            lidz=len(df["nElectron"])
        for i in range(nno,lidz):
            if df["Electron_r9"][i][0] > 0.96 and df["Electron_r9"][i][1] > 0.96:
                if df["Electron_eta"].abs()[i][0] <1.479 and df["Electron_eta"].abs()[i][1] <1.479:
                    if df["Electron_cutBased"][i][0] in [2,3,4] and df["Electron_cutBased"][i][1]in [2,3,4]:
                        if (df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0):
                            if df["Electron_pt"][i][0] > df["Electron_pt"][i][1]:
                                if not (df["Electron_pt"][i][0] > 32 and df["Electron_pt"][i][1] > 20): 
                                    continue
                            else:
                                if not (df["Electron_pt"][i][0] > 20 and df["Electron_pt"][i][1] > 32): 
                                    continue

                            el1 = ROOT.TLorentzVector()
                            el2 = ROOT.TLorentzVector()

                            el1.SetPtEtaPhiM(df["Electron_pt"][i][0],
                                             df["Electron_eta"][i][0],
                                             df["Electron_phi"][i][0],0.000511)
                            el2.SetPtEtaPhiM(df["Electron_pt"][i][1],
                                             df["Electron_eta"][i][1],
                                             df["Electron_phi"][i][1],0.000511)     
                            if (el1+el2).M()<80 or (el1+el2).M()>100:
                                continue
                            el_mass.append((el1+el2).M())
        if len(el_mass)==0:
            print(" {0}\tNone in {1}/{2} of {3}!".format(l_wall_time(filetime),jauns+1,dala,aiziet))
            fs=open("2017_data_v9_money_plot_progress_{0}_{1}.txt".format(notik,tik),"a")
            fs.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5:.2f}\n".format(aiziet,jauns+1,dala,wall_time(time.time()-bigBang),len(el_mass),0))
            fs.close()
            continue
        filetime=time.time()-start
        print(" {0}\tI have the raw data, {1}".format(l_wall_time(filetime),len(el_mass)))
        print("  each {0:.2f} ms".format(1000*filetime/len(el_mass)))
        savetime=time.time()

        fo=open("2017_data_v9_money_plot_{0}_{1}.txt".format(notik,tik),"a")
        for i in range(len(el_mass)):
            fo.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(el_mass[i],aiziet,jauns+1,dala,len(el_mass)))
        fo.close()

        fs=open("2017_data_v9_money_plot_progress_{0}_{1}.txt".format(notik,tik),"a")
        fs.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5:.2f}\n".format(aiziet,jauns+1,dala,wall_time(time.time()-bigBang),
                                               len(el_mass),1000*filetime/len(el_mass)))
        fs.close()
                        
print("{0}\tAll done".format(wall_time(time.time()-bigBang)))    
    
