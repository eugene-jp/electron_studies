# Zee MC, money plots
# UL 2017
import time
bigBang=time.time()
import uproot # if I am not mistaking, we are working with uproot 2
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
# MC file names are stored in a column, in this file:
names=pn.read_csv("all_nosaukumi_2017_MC_v9.txt", sep='\t',names=["nos"])
# PU is from https://github.com/CJLST/ZZAnalysis/blob/Run2_CutBased_BTag16/AnalysisStep/utils/make_PU_weight_hist.py
PUweights= uproot.open("pu_weights_2017.root")["weights"].values
# SF is from https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaUL2016To2018#SFs_for_Electrons_UL_2017
# here it is converted as a 2D matrix of values
sfv=pn.read_csv("2017_SF_loose.txt",sep="\t",header=None)
ex,ey=[-2.5,-2.,-1.566,-1.444,-0.8,0.,0.8,1.444,1.566,2.,2.5],[ 10., 20., 35., 50., 100., 200., 500.]
print("I have the libraries and names")

# atm, it is set to work on (only) one file  
notik=int(sys.argv[1])
tik=notik+1
if tik>len(names["nos"]):
    tik=len(names["nos"])
    
for aiziet in range(notik,tik):
    print("\n {0}/{1}, {2}".format(aiziet+1,tik,wall_time(time.time()-bigBang)))
    start=time.time()

    rootfile="root://cmsxrootd.fnal.gov///"+names["nos"][aiziet]
    tree = uproot.open(rootfile)["Events"]
    print(" {0}\tI have the tree, len={1}".format(l_wall_time(time.time()-start),len(tree)))
    subsection = ["Electron_pt","nElectron","Electron_eta",
                  "Electron_charge","Electron_phi","Pileup_nPU",
                  "Electron_cutBased","Electron_r9"]
# dividing in smaller chunks significantly improoved the overall speed, so we sticked with it    
    cik=200000
    dala=divmod(len(tree),cik)[0]
    if divmod(len(tree),cik)[1]>0:
        dala=dala+1
    
    for jauns in range(0,dala):
        print("\n {0}\tStarting {1}/{2}".format(l_wall_time(time.time()-start),jauns+1,dala))
        start=time.time()
        nno=jauns*cik
        lidz=(jauns+1)*cik
        if lidz>len(tree):
            lidz=len(tree)
        ds = tree.pandas.df(subsection, entrystart=nno, entrystop=lidz)
        print(" {0}\tI have the branches".format(l_wall_time(time.time()-start)))
# we select two electron events
        df=ds.query("nElectron==2")
        df=df.reset_index()
        print(" {0}\tI have the diE, {1}".format(l_wall_time(time.time()-start),len(df["nElectron"])))

        el_mass = []
        el_weight = []
        for i in range(len(df)):
 # having multiple if's not if () and () and () or () was quicker for us, we sticked with it
 # first, we filter of r9 criteria, we ask for both electrons to have it
            if df["Electron_r9"][i][0] > 0.96 and df["Electron_r9"][i][1] > 0.96:
 # second, we want both electrons to be in the barrel 
                if df["Electron_eta"].abs()[i][0] <1.479 and df["Electron_eta"].abs()[i][1] <1.479:
 # third, we ask for loose ID, and understood that it should be not only 2, but also 3 and 4
                    if df["Electron_cutBased"][i][0] in [2,3,4] and df["Electron_cutBased"][i][1]in [2,3,4]:
 # fourth, we want the pair to have opposite charges
                        if (df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0):
 # fifth, we care to have leading el_pt>32 and sub-leading>20 GeV, if it is not satisfied we say bye-bye
                            if df["Electron_pt"][i][0] > df["Electron_pt"][i][1]:
                                if not (df["Electron_pt"][i][0] > 32 and df["Electron_pt"][i][1] > 20):
                                    continue
                            else:
                                if not (df["Electron_pt"][i][0] > 20 and df["Electron_pt"][i][1] > 32):
                                    continue
# if the criteria is met, we calculate the invariant mass
                            el1 = ROOT.TLorentzVector()
                            el2 = ROOT.TLorentzVector()

                            el1.SetPtEtaPhiM(df["Electron_pt"][i][0],
                                             df["Electron_eta"][i][0],
                                             df["Electron_phi"][i][0],0.000511)
                            el2.SetPtEtaPhiM(df["Electron_pt"][i][1],
                                             df["Electron_eta"][i][1],
                                             df["Electron_phi"][i][1],0.000511)
# if the invariant mass is <80 or >100, we say bye-bye
                            if (el1+el2).M()<80 or (el1+el2).M()>100:
                                continue
# the SF is located based on el_pt and el_eta
                            sf1,sf2=0,0 
                            for meta in range(len(ex)-1):
                                if (df["Electron_eta"][i][0]<ex[meta+1] and df["Electron_eta"][i][0]>=ex[meta]) or (df["Electron_eta"][i][0]==2.5 and meta==len(ex)-1):
                                    for mpt in range(len(ey)-1):
                                        if df["Electron_pt"][i][0]<ey[mpt+1] and df["Electron_pt"][i][0]>=ey[mpt]:
                                            sf1=sfv.loc[meta,mpt]
                                if (df["Electron_eta"][i][1]<ex[meta+1] and df["Electron_eta"][i][1]>=ex[meta]) or (df["Electron_eta"][i][1]==2.5 and meta==len(ex)-1):
                                    for mpt in range(len(ey)-1):
                                        if df["Electron_pt"][i][1]<ey[mpt+1] and df["Electron_pt"][i][1]>=ey[mpt]:
                                            sf2=sfv.loc[meta,mpt]
# if the PU is outside of the range or the scale(s) are 0, we say bye-bye
                            if df["Pileup_nPU"][i]<len(PUweights) and not (sf1==0 or sf2==0):
# luminosity from: https://docs.google.com/presentation/d/1gEF2jExqS1hWs-dlYgxrTT2xQztYbBZcrLdw45Aiy7g/edit#slide=id.ge8cc301637_0_55
# cross-section from: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#DY_Z
# generator weight=1 because NOT NLO
# number of events from: dataset=/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM
                                weights = 41.48 * 6077220 * 1 * sf1 * sf2 * PUweights[df["Pileup_nPU"][i]]/102863931
                                el_weight.append(weights)
                                el_mass.append((el1+el2).M())
# if no events suited us in this bunch, it is written in the progress log
        if len(el_mass)==0:
            print(" {0}\tNone in {1}!".format(l_wall_time(time.time()-start),jauns))
            fs=open("progress/2017_MC_v9_money_plot_progress_{0}_{1}.txt".format(notik,tik),"a")
            fs.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5:.2f}\n".format(aiziet,jauns+1,dala,wall_time(time.time()-bigBang),0,0))
            fs.close()
            continue
                            
        filetime=time.time()-start
        print(" {0}\tI have the raw data, {1}".format(l_wall_time(filetime),len(el_mass)))
        print("  each {0:.2f} ms".format(1000*filetime/len(el_mass)))
        savetime=time.time()
# we save in a .txt :) the invariant mass, weights, and from which file and bunch, also how many bunches and events we should have (for double-checking)
        fo=open("results/2017_MC_v9_money_plot_{0}_{1}.txt".format(notik,tik),"a")
        for i in range(len(el_mass)):
            fo.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(el_mass[i],el_weight[i],aiziet,jauns+1,dala,len(el_mass)))
        fo.close()
# we save a progress log documenting info about the file, bunch out of nbunches, the time it took, how many events were nice, what's the rate
        fs=open("progress/2017_MC_v9_money_plot_progress_{0}_{1}.txt".format(notik,tik),"a")
        fs.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5:.2f}\n".format(aiziet,jauns+1,dala,wall_time(time.time()-bigBang),len(el_mass),1000*filetime/len(el_mass)))
        fs.close()
print("{0}\tAll done".format(wall_time(time.time()-bigBang)))
