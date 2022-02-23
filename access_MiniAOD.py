# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

import time
bigBang=time.time()
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

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

#l1Muons, l1MuonLabel = Handle("BXVector<l1t::Muon>"), "gmtStage2Digis:Muon:RECO"  # Read in L1T muon data
electrons, electronLabel = Handle("vector<pat::Electron>"), "slimmedLowPtElectrons::RECO"  # Read in electron data
#genParticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles" # Read in genP data

#names=pn.read_csv("Step3_FileNames.txt", sep='\t',names=["nos"]) # File name file, so we can loop over all files in the dataset
print("I have the libraries and names")

# File counting stuff
notik=0 # Start file number
tik=1#len(names["nos"]) # Finish file number


for aiziet in range(notik,tik): # Looping over files
    print("\n {0}/{1}, {2}".format(aiziet+1,tik,wall_time(time.time()-bigBang)))

    start=time.time()       
    #rootfile="/eos/cms/store/group/phys_bphys/chic_hlt/"+names["nos"][aiziet]
    rootfile="/store/data/Run2018B/ParkingBPH1/MINIAOD/05May2019-v2/230000/00775987-81BC-A246-91CB-6056E660D7AD.root"
    events = Events("root://cmsxrootd.fnal.gov//"+rootfile)
    print(" {0}\tI have the tree".format(l_wall_time(time.time()-start)))
    
    el_charge = [] 
    el_pt = []
    el_eta = []
    el_phi = []
    el_iev = []
    el_i = []       
    
    
    for iev,event in enumerate(events): # Reading in events from the file
        event.getByLabel(electronLabel, electrons)
        #event.getByLabel(genParticlesLabel, genParticles)
        print("iev = {0}".format(iev))


    
        for i,elec in enumerate(electrons.product()): # Checking all electrons in single event
            #print(i)
            el_charge.append(elec.charge())
            el_pt.append(elec.pt())
            el_eta.append(elec.eta())
            el_phi.append(elec.phi()) 
            el_iev.append(iev)
            el_i.append(i) 
            
            
            
            
            
            
            
            
