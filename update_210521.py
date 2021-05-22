import time
bigBang=time.time()
import uproot
import ROOT
import matplotlib.pyplot as plt
import numpy as np
import pandas as pn
names=pn.read_csv("all_files_2017_exclUL.txt", sep='\t',names=["nos"]) 
print("I have the libraries and names")

notik=0
tik=10#len(names)
el_mass =[]
for aiziet in range(notik,tik):
    print("\n {0}/{1} and {2:0f} min or {3:0f} h:".format(aiziet+1,tik,(time.time()-bigBang)/60,(time.time()-bigBang)/3600))
    start=time.time()
        
    rootfile="root://cmsxrootd.fnal.gov///"+names["nos"][aiziet]
    tree = uproot.open(rootfile)["Events"]
    print(" I have the tree, {0:.3f} s".format(time.time()-start))

    subsection = ["Electron_pt","nElectron","Electron_eta","Electron_charge","Electron_phi"]
    ds = tree.pandas.df(subsection, entrystop=-1)
    print(" I have the branches, {0:.3f} s".format(time.time()-start))

    df=ds.query("nElectron==2")
    df=df.reset_index()
    print(" I have the diE, {1}, {0:.3f} s".format(time.time()-start,len(df["nElectron"])))

    for i in range(len(df["nElectron"])):
        if df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0:
            el1 = ROOT.TLorentzVector()
            el2 = ROOT.TLorentzVector()

            el1.SetPtEtaPhiM(df["Electron_pt"][i][0],
                             df["Electron_eta"][i][0],
                             df["Electron_phi"][i][0],0.000511)
            el2.SetPtEtaPhiM(df["Electron_pt"][i][1],
                             df["Electron_eta"][i][1],
                             df["Electron_phi"][i][1],0.000511)
            el_mass.append((el1+el2).M())   

    print(" I have the raw data, {0:.3f} s".format(time.time()-start))
    
print("\nShall save")
savetime=time.time()
fo=open("2017_dimass_test_{0}_{1}.txt"/format(notik, tik),"a")
for i in range(len(el_mass)):
    fo.write(str(el_mass[i])+"\n")
fo.close()
print("Saving took {0:.3f} s".format(time.time()-savetime))
print("All done, {0:.0f} s ({1:.0f} min)".format(time.time()-bigBang,(time.time()-bigBang)/60))

#print("I shall start to draw, {0:.3f} s".format(time.time()-start))
#plt.hist(el_mass,bins=90,range=[0,180], alpha=0.7, histtype=u'step')
#plt.xlabel("2_E, GeV")
#plt.ylabel("Frequency")
#plt.title("2017, {0} files, t={1:.0f} s".format(cik,time.time()-start))
#plt.xticks(np.arange(0,190,10))
#print("Ready to show, {0:.3f} s".format(time.time()-start))
#plt.savefig("{0}_pilnP.png".format(cik))
#plt.show()
