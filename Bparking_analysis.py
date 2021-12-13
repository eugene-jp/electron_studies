# Code for J/Psi with uproot 4 and 3 
# This is code for (nBToKEE==1), when launching this code, you have to input number from 0-5, which corresponds to 6 maps the files are located in!!!! Like (python -i Bparking_analysis.py 0)
import time
bigBang=time.time()
import uproot as up
import uproot3 as up3
#import uproot_methods as up_me
from ROOT import TLorentzVector
import numpy as np
import pandas as pn
import sys 
import awkward as ak
from uproot3_methods import PtEtaPhiMassLorentzVector

#up.recreate("JPsi/2017_JPsi_MuonEG_RESULTS.root") # !!!!!! Always check this line so, I would not rewrite all the files!!!!!!!!!!

def wall_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{0:.0f}h:{1:.0f}min:{2:.0f}s".format(h,m,s)
def l_wall_time(seconds):
    m, s = divmod(seconds, 60)
    return "{0:.0f}min:{1:.0f}s".format(m,s)

NameFiles = ["/afs/cern.ch/user/n/nstrautn/BparkFileNames_0.txt","/afs/cern.ch/user/n/nstrautn/BparkFileNames_1.txt","/afs/cern.ch/user/n/nstrautn/BparkFileNames_2.txt","/afs/cern.ch/user/n/nstrautn/BparkFileNames_3.txt","/afs/cern.ch/user/n/nstrautn/BparkFileNames_4.txt","/afs/cern.ch/user/n/nstrautn/BparkFileNames_5.txt"]
Number = ["0/","1/","2/","3/","4/","5/"]

File_Names = pn.read_csv(NameFiles[int(sys.argv[1])],sep='\t',names=["FileNames"])

#File_Names = pn.read_csv("/afs/cern.ch/user/n/nstrautn/BparkFileNames.txt",sep='\t',names=["FileNames"])
print("Got all the libraries and filenames")

#coeficient = 1
From = 0
To = len(File_Names["FileNames"])

DataFF = pn.DataFrame()

#root://eoscms.cern.ch//eos/cms/store/cmst3/group/bpark/BParkingNANO_2020Jan16/ParkingBPH1/crab_data_Run2018D_part1/200116_151214/0000

for i in range(From,To):
    
    start=time.time()
    
    print("Working on file number {0}/{1}, {2}".format(i+1,To,wall_time(time.time()-bigBang)))
    
    #rootfile="root://cmsxrootd.fnal.gov///"+File_Names["FileNames"][i]
    rootfile="root://eoscms.cern.ch//eos/cms/store/cmst3/group/bpark/BParkingNANO_2020Jan16/ParkingBPH1/crab_data_Run2018D_part1/200116_151214/000"+Number[int(sys.argv[1])]+File_Names["FileNames"][i]
    #tree = up.open(rootfile)["Events"]
    up3_tree = up3.open(rootfile)["Events"]
    
    #tree.arrays(tree.keys(), library="pd")
    
    print("Tree has been read in! {0}".format(l_wall_time(time.time()-start)))
    
    hlt_list = []
    Electron_list = []  
    
    for x in up3_tree.keys():
        if ('HLT_') in x :
            hlt_list.append(x)
        if ('BToKEE') in x :
            Electron_list.append(x)  
    
    #Electron_list.remove('Jet_nElectrons')
    #branches = ["Electron_pt","nElectron","Electron_eta","Electron_charge","Electron_phi","Electron_cutBased","Electron_r9"]
    subsection = Electron_list + hlt_list
    
    
    
    DataTable = up3_tree.pandas.df(subsection, entrystop=-1) # Works for uproot 3
    #tree.arrays(subsection, library="pd")
  
    print("I have the branches! {0}".format(l_wall_time(time.time()-start)))
    
    two_electrons_mask = DataTable["nBToKEE"] == 1
    DF = DataTable[two_electrons_mask]
    #DF = DF.reset_index() - > Partaisa uz veco uproot 3 formatu, kur subentry un entry ir viena limeni, nevar izveleties tikai 1. vai 2. elektronu (query, protams, strada)
    if len(DF)==0:
        continue
    
    
    gut_eta=DF["BToKEE_fit_l1_eta"].abs() < 2.5
    #gut_eta=DF["Electron_eta"][:,0].abs() < 2.5
    #gut_pt=DF["Electron_pt"][:,0] > 7.0
    #gut_ID=DF["Electron_cutBased"][:,0] >= 2
    #gut_charge=DF["Electron_charge"][:,0] + DF["Electron_charge"][:,1] == 0
   
    #fav=gut_charge&gut_pt&gut_eta&gut_ID
    #fav=gut_charge&gut_eta
    fav=gut_eta
    
    #df=DF[fav[DF.index.get_level_values('entry')].values] # Partaisa no 1 uz 2 per entry true/false stuff, tad var uzlikt masku uz pilnda DF
    df=DF[fav]
    #dq=DF[fav]
    
    #df = DataTable.query("nElectron==2")
    #df = df.reset_index()
    #df0 = df.query("subentry==0")
    #df1 = df.query("subentry==1")
    
    print("I have {0} diE events! {1}".format(len(df["nBToKEE"]),l_wall_time(time.time()-start)))
    
    #Electron_list.remove('nElectron') # Jautajums par so
    
    el_InvMass = []
    el_event_i = []
    el_data_filter = []    
    dR_list = []
    
    entry_N = df.index.get_level_values("entry")
    entry_df = entry_N[::2]
    #subentry_M = df.index.get_level_values("subentry")
    
    
    for y in entry_N: #entry_df
            
        el1 = PtEtaPhiMassLorentzVector(pt=df["BToKEE_fit_l1_pt"][y], eta=df["BToKEE_fit_l1_eta"][y], phi=df["BToKEE_fit_l1_phi"][y], mass=0.000511) 
        el2 = PtEtaPhiMassLorentzVector(pt=df["BToKEE_fit_l2_pt"][y], eta=df["BToKEE_fit_l2_eta"][y], phi=df["BToKEE_fit_l2_phi"][y], mass=0.000511)

        if ((el1+el2).mass < 20):
            el_InvMass.append((el1+el2).mass)
            el_event_i.append(y)
            el_data_filter.append(True)
            #el_data_filter.append(True)
            
            phi_check = []
            if abs(df["BToKEE_fit_l1_phi"][y][0]-df["BToKEE_fit_l2_phi"][y][0]) > 3.1415926:
                phi_check.append((6.2831852-abs(df["BToKEE_fit_l1_phi"][y][0]-df["BToKEE_fit_l2_phi"][y][0])))
            else:
                phi_check.append((df["BToKEE_fit_l1_phi"][y][0]-df["BToKEE_fit_l2_phi"][y][0]))
    
            dR_list.append(((df["BToKEE_fit_l1_eta"][y][0]-df["BToKEE_fit_l2_eta"][y][0])**2+(phi_check[0])**2)**0.5)    
        
        else:
            el_data_filter.append(False)
            #el_data_filter.append(False)    
              
    
    dff = df[el_data_filter]
    
    if len(dff)==0:
        continue      
    
    df0=dff.xs(0,level=1)
    #df1=dff.xs(1,level=1)
    #DataF = df0.join(df1,lsuffix="_0",rsuffix="_1")
    #DataF["DiElectron_InvMass"] = el_InvMass
    #DataF["Electron_dR"] = dR_list
    
    df0["DiElectron_InvMass"] = el_InvMass
    df0["Electron_dR"] = dR_list
    
    #DataFF = DataFF.append(DataF)
    DataFF = DataFF.append(df0)

    
    print("Got invariant masses, hehe")
    print("I have {0} raw data events! {1}".format(len(el_InvMass),l_wall_time(time.time()-start)))
    print(" Each event took {0:.2f} ms".format(1000*(time.time()-start)/len(el_InvMass)))

print("ROOT file writing has started! {0}".format(wall_time(time.time()-bigBang)))     


#nan_value=float("NaN")
#DataFF.replace(nan_value,False,inplace=True)

# ROOT file for RESULT data
#ROOT_File_RESULTS = up.recreate("/afs/cern.ch/user/n/nstrautn/Results/2017_JPsi_MuonEG_RESULTS_{0}_{1}_eta2p5.root".format(From,To))


ROOT_File_RESULTS = up.recreate("/afs/cern.ch/user/n/nstrautn/CMSSW_10_2_22/src/EgammaAnalysis/TnPTreeProducer/python/Results_Bpark/Bpark_JPsi_DATA_BToKEE_{0}_{1}_eta2p5_{2}.root".format(From,To,sys.argv[1]))


#ROOT_File_RESULTS = up.update("JPsi/2017_JPsi_MuonEG_RESULTS.root")


ROOT_File_RESULTS["Electrons"] = DataFF  # DataF


#ROOT_File_RESULTS["Electrons"] = up.newtree({DataF.columns:dataF.dtypes})       
#ROOT_File_RESULTS["Electrons"].extend({DataF.columns: DataF})


ROOT_File_RESULTS.close 

print("System argument {0}, and corresponding filename File name {1}".format(sys.argv[1],NameFiles[int(sys.argv[1])]))
print("All done! {0}".format(wall_time(time.time()-bigBang)))  





