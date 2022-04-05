# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

import time
bigBang=time.time()
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pn
from uproot3_methods import PtEtaPhiMassLorentzVector 
import awkward as ak
import sys
import uproot as up

def wall_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{0:.0f}h:{1:.0f}min:{2:.0f}s".format(h,m,s) #lxplus nepatik d
def l_wall_time(seconds):
    m, s = divmod(seconds, 60)
    return "{0:.0f}min:{1:.0f}s".format(m,s)

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

#l1Muons, l1MuonLabel = Handle("BXVector<l1t::Muon>"), "gmtStage2Digis:Muon:RECO"  # Read in L1T muon data
electrons, electronLabel = Handle("vector<pat::Electron>"), "slimmedElectrons::RECO"  # Read in electron data
#genParticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles" # Read in genP data

names=pn.read_csv("/afs/cern.ch/user/n/nstrautn/CMSSW_10_2_22/src/EgammaAnalysis/TnPTreeProducer/python/Bpark_MINI_names.txt", sep='\t',names=["nos"]) # File name file, so we can loop over all files in the dataset
print("I have the libraries and names")

# File counting stuff
notik=int(sys.argv[1]) # Start file number
tik=notik+5#len(names["nos"]) # Finish file number

if tik > len(names["nos"]): # Safety check
    tik = len(names["nos"])

DataFF = pn.DataFrame()

for aiziet in range(notik,tik): # Looping over files
    print("\n {0}/{1}, {2}".format(aiziet+1,tik,wall_time(time.time()-bigBang)))

    start=time.time()       
    #rootfile="/eos/cms/store/group/phys_bphys/chic_hlt/"+names["nos"][aiziet]
    rootfile=names["nos"][aiziet]
    #rootfile="/store/data/Run2018B/ParkingBPH1/MINIAOD/05May2019-v2/230000/00775987-81BC-A246-91CB-6056E660D7AD.root"
    events = Events("root://cmsxrootd.fnal.gov//"+rootfile)
    print(" {0}\tI have the tree".format(l_wall_time(time.time()-start)))
    
    # lists for all parameters we will take in form of 'float'/'int'/'string'? No complex objects
    
    el_charge = [] 
    el_pt = []
    el_eta = []
    el_phi = []
    el_isPF = []
    el_iev = []
    el_i = []       
    el_InvMass = []
    el_event_i = []
    
    el_counter = []
          
    # All the lists for extra parameters
    
    scl_eta = []
    ele_oldsigmaietaieta = []
    ele_oldsigmaiphiiphi = []
    ele_oldcircularity = []
    ele_oldr9 = []
    ele_scletawidth = []
    ele_sclphiwidth = []
    ele_he = []
    ele_oldhe = []
    ele_kfchi2 = []
    ele_gsfchi2 = []
    #ele_fbrem = []
    #ele_conversionVertexFitProbability = []
    ele_ep = []
    ele_eelepout = []
    ele_IoEmIop = []
    ele_deltaetain = []
    ele_deltaphiin = []
    ele_deltaetaseed = []
    ele_psEoverEraw = []
    ele_pfPhotonIso = []
    ele_pfChargedHadIso = []
    ele_pfNeutralHadIso = []
    ele_PFPUIso = []
    #ElectronMVAEstimatorRun2Fall17IsoV2Values = []
    ElectronMVAEstimatorRun2Fall17IsoV1Values = []
    ElectronMVAEstimatorRun2Fall17NoIsoV1Values = []
    #ElectronMVAEstimatorRun2Fall17NoIsoV2Values = []
    
    ele_kfhits = []
    ele_chi2_hits = []
    ele_gsfhits = []
    ele_expected_inner_hits = []
    
    cutBasedElectronID_Fall17_94X_V2_veto = []
    cutBasedElectronID_Fall17_94X_V2_loose = []
    cutBasedElectronID_Fall17_94X_V2_medium = []
    cutBasedElectronID_Fall17_94X_V2_tight = []
    mvaEleID_Fall17_iso_V2_wp90 = []
    mvaEleID_Fall17_iso_V2_wp80 = []
    mvaEleID_Fall17_noIso_V2_wp90 = []
    mvaEleID_Fall17_noIso_V2_wp80 = []
    mvaEleID_Fall17_noIso_V2_wpLoose_unsopported = []
    mvaEleID_Fall17_iso_V2_wpHZZ_unsopported = []
    
    for iev,event in enumerate(events): # Reading in events from the file
        event.getByLabel(electronLabel, electrons)
        #event.getByLabel(genParticlesLabel, genParticles)
        #print("iev = {0}".format(iev))


    
        for i,elec in enumerate(electrons.product()): # Checking all electrons in single event
            #print(i)
            
            # Adding data to chosen lists kinda the basic ones
            
            el_charge.append(elec.charge())
            el_pt.append(elec.pt())
            el_eta.append(elec.eta())
            el_phi.append(elec.phi()) 
            el_isPF.append(elec.isPF())
            el_iev.append(iev)
            el_i.append(i) 
            
            scl_eta.append(elec.superCluster().eta())
            ele_oldsigmaietaieta.append(elec.full5x5_sigmaIetaIeta())
            ele_oldsigmaiphiiphi.append(elec.full5x5_sigmaIphiIphi())
            ele_oldcircularity.append(1 - (elec.full5x5_e1x5()/elec.full5x5_e5x5()))
            ele_oldr9.append(elec.full5x5_r9())
            ele_scletawidth.append(elec.superCluster().etaWidth())
            ele_sclphiwidth.append(elec.superCluster().phiWidth())
            ele_he.append(elec.hadronicOverEm())
            ele_oldhe.append(elec.full5x5_hcalOverEcal())
            ele_kfchi2.append(elec.closestCtfTrackRef().normalizedChi2() if (elec.closestCtfTrackRef().isAvailable() == True and elec.closestCtfTrackRef().isNonnull() == True ) else 0)
            ele_gsfchi2.append(elec.gsfTrack().normalizedChi2())
            
            #ele_fbrem.append(elec.charge())
            
            #ele_conversionVertexFitProbability.append(elec.convVtxFitProb()) # Question whether this should be included
            
            ele_ep.append(elec.eSuperClusterOverP())
            ele_eelepout.append(elec.eEleClusterOverPout())
            ele_IoEmIop.append( 1.0/(elec.ecalEnergy())-1.0/(elec.trackMomentumAtVtx().R()) if (elec.ecalEnergy() != 0 and elec.trackMomentumAtVtx().R() != 0) else np.NaN) 
            ele_deltaetain.append(elec.deltaEtaSuperClusterTrackAtVtx())
            ele_deltaphiin.append(elec.deltaPhiSuperClusterTrackAtVtx())
            ele_deltaetaseed.append(elec.deltaEtaSeedClusterTrackAtCalo())
            ele_psEoverEraw.append((elec.superCluster().preshowerEnergy())/(elec.superCluster().rawEnergy())) 
            ele_pfPhotonIso.append(elec.pfIsolationVariables().sumPhotonEt) # Maybe () should be included at the end of sumPhotoEt???
            ele_pfChargedHadIso.append(elec.pfIsolationVariables().sumChargedHadronPt)
            ele_pfNeutralHadIso.append(elec.pfIsolationVariables().sumNeutralHadronEt)
            ele_PFPUIso.append(elec.pfIsolationVariables().sumPUPt)
            
            #ElectronMVAEstimatorRun2Fall17IsoV2Values.append(elec.userFloat("ElectronMVAEstimatorRun2Fall17IsoV2Values"))
            ElectronMVAEstimatorRun2Fall17IsoV1Values.append(elec.userFloat("ElectronMVAEstimatorRun2Fall17IsoV1Values"))
            ElectronMVAEstimatorRun2Fall17NoIsoV1Values.append(elec.userFloat("ElectronMVAEstimatorRun2Fall17NoIsoV1Values"))
            #ElectronMVAEstimatorRun2Fall17NoIsoV2Values.append(elec.userFloat("ElectronMVAEstimatorRun2Fall17NoIsoV2Values"))
    
            ele_kfhits.append(elec.closestCtfTrackRef().hitPattern().trackerLayersWithMeasurement() if (elec.closestCtfTrackRef().isAvailable() == True and elec.closestCtfTrackRef().isNonnull() == True ) else -1)
            ele_chi2_hits.append(elec.gsfTrack().normalizedChi2())
            ele_gsfhits.append(elec.gsfTrack().hitPattern().trackerLayersWithMeasurement())
            #ele_expected_inner_hits.append(elec.gsfTrack().hitPattern().numberOfLostHits("reco::HitPattern::MISSING_INNER_HITS")) # does not work if "reco::HitPattern::MISSING_INNER_HITS" is written in
    
            cutBasedElectronID_Fall17_94X_V2_veto.append(elec.electronID("cutBasedElectronID-Fall17-94X-V2-veto"))
            cutBasedElectronID_Fall17_94X_V2_loose.append(elec.electronID("cutBasedElectronID-Fall17-94X-V2-loose"))
            cutBasedElectronID_Fall17_94X_V2_medium.append(elec.electronID("cutBasedElectronID-Fall17-94X-V2-medium"))
            cutBasedElectronID_Fall17_94X_V2_tight.append(elec.electronID("cutBasedElectronID-Fall17-94X-V2-tight"))
            
            mvaEleID_Fall17_iso_V2_wp90.append(elec.electronID("mvaEleID-Fall17-iso-V2-wp90"))
            mvaEleID_Fall17_iso_V2_wp80.append(elec.electronID("mvaEleID-Fall17-iso-V2-wp80"))
            mvaEleID_Fall17_noIso_V2_wp90.append(elec.electronID("mvaEleID-Fall17-noIso-V2-wp90"))
            mvaEleID_Fall17_noIso_V2_wp80.append(elec.electronID("mvaEleID-Fall17-noIso-V2-wp80"))
            mvaEleID_Fall17_noIso_V2_wpLoose_unsopported.append(elec.electronID("mvaEleID-Fall17-noIso-V2-wpLoose"))
            mvaEleID_Fall17_iso_V2_wpHZZ_unsopported.append(elec.electronID("mvaEleID-Fall17-noIso-V2-wpLoose"))           
            
            
            
    multi_index = list(zip(el_iev,el_i))     # creates lists for entries from iev and subentries from i   
    
    index = pn.MultiIndex.from_tuples(multi_index,names=["entry","subentry"]) # creates entry and subentry structure in pandas
    
    data = list(zip(el_charge,el_pt,el_phi,el_eta,el_isPF,scl_eta,ele_oldsigmaietaieta,ele_oldsigmaiphiiphi,ele_oldcircularity,ele_oldr9,ele_scletawidth,ele_sclphiwidth,ele_he,ele_oldhe,ele_kfchi2,ele_gsfchi2,ele_ep,ele_eelepout,ele_IoEmIop,ele_deltaetain,ele_deltaphiin,ele_deltaetaseed,ele_psEoverEraw,ele_pfPhotonIso,ele_pfChargedHadIso,ele_pfNeutralHadIso,ele_PFPUIso,ElectronMVAEstimatorRun2Fall17IsoV1Values,ElectronMVAEstimatorRun2Fall17NoIsoV1Values,ele_kfhits,ele_chi2_hits,ele_gsfhits,cutBasedElectronID_Fall17_94X_V2_veto,cutBasedElectronID_Fall17_94X_V2_loose,cutBasedElectronID_Fall17_94X_V2_medium,cutBasedElectronID_Fall17_94X_V2_tight,mvaEleID_Fall17_iso_V2_wp90,mvaEleID_Fall17_iso_V2_wp80,mvaEleID_Fall17_noIso_V2_wp90,mvaEleID_Fall17_noIso_V2_wp80,mvaEleID_Fall17_noIso_V2_wpLoose_unsopported,mvaEleID_Fall17_iso_V2_wpHZZ_unsopported)) # list data zipped together in one tuple/list 
    # ,ele_conversionVertexFitProbability ElectronMVAEstimatorRun2Fall17IsoV2Values ElectronMVAEstimatorRun2Fall17NoIsoV2Values ,ele_expected_inner_hits
    
    dd = pn.DataFrame(data,index=index,columns=["Electron_charge","Electron_pt","Electron_phi","Electron_eta","Electron_isPF","Electron_scl_eta","Electron_oldsigmaietaieta","Electron_oldsigmaiphiiphi","Electron_oldcircularity","Electron_oldr9","Electron_scletawidth","Electron_sclphiwidth","Electron_he","Electron_oldhe","Electron_kfchi2","Electron_gsfchi2","Electron_ep","Electron_eelepout","Electron_IoEmIop","Electron_deltaetain","Electron_deltaphiin","Electron_deltaetaseed","Electron_psEoverEraw","Electron_pfPhotonIso","Electron_pfChargedHadIso","Electron_pfNeutralHadIso","Electron_PFPUIso","ElectronMVAEstimatorRun2Fall17IsoV1Values","ElectronMVAEstimatorRun2Fall17NoIsoV1Values","Electron_kfhits","Electron_chi2_hits","Electron_gsfhits","cutBasedElectronID_Fall17_94X_V2_veto","cutBasedElectronID_Fall17_94X_V2_loose","cutBasedElectronID_Fall17_94X_V2_medium","cutBasedElectronID_Fall17_94X_V2_tight","mvaEleID_Fall17_iso_V2_wp90","mvaEleID_Fall17_iso_V2_wp80","mvaEleID_Fall17_noIso_V2_wp90","mvaEleID_Fall17_noIso_V2_wp80","mvaEleID_Fall17_noIso_V2_wpLoose_unsopported","mvaEleID_Fall17_iso_V2_wpHZZ_unsopported"]) # Pandas data frame with entry/subentry structure 
    # ,"Electron_conversionVertexFitProbability" "ElectronMVAEstimatorRun2Fall17IsoV2Values" ,"ElectronMVAEstimatorRun2Fall17NoIsoV2Values" "Electron_expected_inner_hits",
    
    
    entry_N_test = dd.index.get_level_values("entry") # creates entry for each subentry (we dont need that). Doesn't do that for nanoAOD root files
    
    entry_N = []
    
    for i in range(len(entry_N_test)): # we take out dublicates in entry count (some shady counting before, so we need to do this)
        if entry_N_test[i] not in entry_N:
            entry_N.append(entry_N_test[i])    
    
    n2_list = []
    
    for i in entry_N:
        if len(dd["Electron_pt"][i]) == 2: # inv mass calc
            
            #a = DF["Electron_pt"][i].index.get_level_values("subentry") # Gets the correct subentry number (something is shady in pandas)
            #Manually made entries and subentries show one thing, but work like another
            
            if (dd["Electron_charge"][i][0]+dd["Electron_charge"][i][1] == 0) and (dd["Electron_isPF"][i][0] == 1 and dd["Electron_isPF"][i][1] == 1):
                n2_list.append(True)
                n2_list.append(True)            
            
                el1 = PtEtaPhiMassLorentzVector(pt=dd["Electron_pt"][i][0], eta=dd["Electron_eta"][i][0], phi=dd["Electron_phi"][i][0], mass=0.000511) 
                el2 = PtEtaPhiMassLorentzVector(pt=dd["Electron_pt"][i][1], eta=dd["Electron_eta"][i][1], phi=dd["Electron_phi"][i][1], mass=0.000511)

                el_InvMass.append((el1+el2).mass)
                #el_InvMass.append(np.NaN) # Extra empty line, so we can add inv.mass to our dataframe structure
                el_event_i.append(i)  
            else:
                n2_list.append(False)
                n2_list.append(False)  
        else:
            for i in range(len(dd["Electron_pt"][i])):
                n2_list.append(False)                
    
    df = dd[n2_list] # Mask for good events
    
    print("We have {0} PF electrons".format(len(df)))
    
    df0=df.xs(0,level=1) # 1st electron data split
    df1=df.xs(1,level=1) # 2nd electron data split
    DataF = df0.join(df1,lsuffix="_0",rsuffix="_1") # add the both electron parts together
    DataF["DiElectron_InvMass"] = el_InvMass # add invariant mass column
    
    print("We have {0} PF events".format(len(DataF)))
    
    DataFF = DataFF.append(DataF) # add everything in new dataset (important if we run over many files)
    
    # Ignore the out-commented parts (older version of the code)
    
    #df["Di-Electron_InvMass"] = el_InvMass    
    
    
    #gut_PF = dd["Electron_isPF"] == 1 
    #fav = gut_PF
    #DF = dd[fav]
    
    #entry_N_test = DF.index.get_level_values("entry") # creates entry for each subentry (we dont need that). Doesn't do that for nanoAOD root files
    
    #entry_N = []
    
    #for i in range(len(entry_N_test)):
    #    if entry_N_test[i] not in entry_N:
    #        entry_N.append(entry_N_test[i])
    
    #entry_N_1 = list(set(entry_N_test)) # We take out dublicates from entry list
    
    #print("We have {0} PF events".format(len(DF)))
    
#    n2list = [] # Filtering out only di-electron events
    
#    for i in entry_N:
#        if len(DF["Electron_pt"][i]) == 2: # inv mass calc
            
#            a = DF["Electron_pt"][i].index.get_level_values("subentry") # Gets the correct subentry number (something is shady in pandas)
            #Manually made entries and subentries show one thing, but work like another
            
#            if DF["Electron_charge"][i][a[0]]+DF["Electron_charge"][i][a[1]] == 0:
#                n2list.append(True)
#                n2list.append(True)            
            
#                el1 = PtEtaPhiMassLorentzVector(pt=DF["Electron_pt"][i][a[0]], eta=DF["Electron_eta"][i][a[0]], phi=DF["Electron_phi"][i][a[0]], mass=0.000511) 
#                el2 = PtEtaPhiMassLorentzVector(pt=DF["Electron_pt"][i][a[1]], eta=DF["Electron_eta"][i][a[1]], phi=DF["Electron_phi"][i][a[1]], mass=0.000511)

#                el_InvMass.append((el1+el2).mass)
#                el_InvMass.append(np.NaN) # Extra empty line, so we can add inv.mass to our dataframe structure
#                el_event_i.append(i)  
#            else:
#                n2list.append(False)
#                n2list.append(False)  
#        else:
#            for i in range(len(DF["Electron_pt"][i])):
#                n2list.append(False)                
    
#    gut_n = n2list
#    df = DF[gut_n]
#    df["Di-Electron_InvMass"] = el_InvMass
    
    
    #plt.hist(el_InvMass,bins=50,range=[0,20],  alpha=0.9, histtype=u'step',label='DiElectron_invMass', color='b') #u'step' normed=True
    #plt.legend(loc='upper right')
    #plt.xlabel("Inv.Mass, GeV", size = 15)
    #plt.ylabel("Events", size = 15)
    #plt.title("Bpark Data J/Psi", size = 15)
    #plt.savefig("/afs/cern.ch/user/n/nstrautn/CMSSW_10_2_22/src/EgammaAnalysis/TnPTreeProducer/python/JPsi_Mini/BPark_Mini_Pt.png")
    #plt.show()

    #plt.hist(dd["Electron_pt"],bins=50,range=[0,20],  alpha=0.9, histtype=u'step',label='Electron_pt', color='b') #u'step' normed=True
    #plt.legend(loc='upper right')
    #plt.xlabel("pT, GeV", size = 15)
    #plt.ylabel("Events", size = 15)
    #plt.title("Bpark Data J/Psi", size = 15)
    #plt.savefig("/afs/cern.ch/user/n/nstrautn/CMSSW_10_2_22/src/EgammaAnalysis/TnPTreeProducer/python/JPsi_Mini/BPark_Mini_Pt.png")
    #plt.show()
    
    #plt.hist(DF["Electron_pt"],bins=50,range=[0,20],  alpha=0.9, histtype=u'step',label='Electron_pt_isPF', color='b') #u'step' normed=True
    #plt.legend(loc='upper right')
    #plt.xlabel("pT, GeV", size = 15)
    #plt.ylabel("Events", size = 15)
    #plt.title("Bpark Data J/Psi", size = 15)
    #plt.savefig("/afs/cern.ch/user/n/nstrautn/CMSSW_10_2_22/src/EgammaAnalysis/TnPTreeProducer/python/JPsi_Mini/BPark_Mini_Pt_isPF.png")
    #plt.show()

#    zipped = list(zip(el_iev,el_i,el_charge,el_pt,el_phi,el_eta,el_isPF))
#    df = pn.DataFrame(zipped,columns=["event","electron_i","Electron_charge","Electron_pt","Electron_phi","Electron_eta","Electron_isPF"])        
            
ROOT_File_RESULTS = up.recreate("/eos/user/n/nstrautn/Bparking_JPsi/JPsi_DATA_fromMINI/Bpark_JPsi_DATA_MINI_{0}_{1}.root".format(notik,tik)) #len(names["nos"]) # creating root file

ROOT_File_RESULTS["Electrons"] = DataFF # adding dataframe with data to root file
           
ROOT_File_RESULTS.close        # closing the root file    
            
            

