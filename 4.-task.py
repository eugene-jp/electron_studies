import ROOT
import time
start=time.time()
import uproot
import matplotlib.pyplot as plt
import numpy as np
import math as math

print("I have the libraries")

rootfile="root://cmsxrootd.fnal.gov///store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_plus5percentMaterial_102X_mcRun2_asymptotic_v8-v1/120000/07B01D04-E364-7B43-B52B-EBB19A971F8C.root"

tree = uproot.open(rootfile)["Events"]

print("I have the tree, {0:.3f} s".format(time.time()-start))

cik=300000
subsection = ["Electron_pt","nElectron","Electron_eta","Electron_charge","Electron_phi"]
ds = tree.pandas.df(subsection, entrystop=cik) # We take relevant data

print("I have the branches, {0:.3f} s".format(time.time()-start))

el_inv = []
mass_check = []
repetition = []
repetition_fix = []
repetition_check = []
el_mass = 0.000511
Cosine = []
Pt_SUM = []

df=ds.query("nElectron==3") # We choose only 3 electron events
df=df.reset_index() # Reindex it

print("I have the triE, {1}, {0:.3f} s".format(time.time()-start,len(df["nElectron"])))

for i in range(len(df["nElectron"])):
    if df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0: # 1.-2. electron pair analysis

        el1_pt = df["Electron_pt"][i][0]
        el1_eta = df["Electron_eta"][i][0]
        el1_phi = df["Electron_phi"][i][0]
        el2_pt = df["Electron_pt"][i][1]
        el2_eta = df["Electron_eta"][i][1]
        el2_phi = df["Electron_phi"][i][1]
        
        elec1 = ROOT.TLorentzVector()
        elec2 = ROOT.TLorentzVector()
        elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, el_mass)
        elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, el_mass)
        mass = (elec1+elec2).M()
        mass_check.append(mass)
        cosine = math.cos(elec1.Angle(elec2.Vect()))
        #pt_vect = elec1.Vect()+elec2.Vect()
        #pt_vect.Mag()
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
            #Pt_SUM.append(pt_vect.Mag())
        
    
    if df["Electron_charge"][i][0]+df["Electron_charge"][i][2] == 0: # 1.-3. electron pair analysis

        el1_pt = df["Electron_pt"][i][0]
        el1_eta = df["Electron_eta"][i][0]
        el1_phi = df["Electron_phi"][i][0]
        el2_pt = df["Electron_pt"][i][2]
        el2_eta = df["Electron_eta"][i][2]
        el2_phi = df["Electron_phi"][i][2]
        
        elec1 = ROOT.TLorentzVector()
        elec2 = ROOT.TLorentzVector()
        elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, el_mass)
        elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, el_mass)
        mass = (elec1+elec2).M()
        mass_check.append(mass)
        cosine = math.cos(elec1.Angle(elec2.Vect()))
        #pt_vect = elec1.Vect()+elec2.Vect()
        #pt_vect.Mag()
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
            #Pt_SUM.append(pt_vect.Mag())
        
        
    
    if df["Electron_charge"][i][1]+df["Electron_charge"][i][2] == 0: # 2.-3. electron pair analysis
            
        
        el1_pt = df["Electron_pt"][i][1]
        el1_eta = df["Electron_eta"][i][1]
        el1_phi = df["Electron_phi"][i][1]
        el2_pt = df["Electron_pt"][i][2]
        el2_eta = df["Electron_eta"][i][2]
        el2_phi = df["Electron_phi"][i][2]
        
        elec1 = ROOT.TLorentzVector()
        elec2 = ROOT.TLorentzVector()
        elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, el_mass)
        elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, el_mass)
        mass = (elec1+elec2).M()
        mass_check.append(mass)
        cosine = math.cos(elec1.Angle(elec2.Vect()))
        #pt_vect = elec1.Vect()+elec2.Vect()
        #pt_vect.Mag()
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
            #Pt_SUM.append(pt_vect.Mag())
        
    #We get rid of extra data point from single 3 electron event
    #we choose between 1.-2. and 1.-3. electron pairs
    #We take the one that is closer to 91.2 GeV
    
    if df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0 and \
       df["Electron_charge"][i][0]+df["Electron_charge"][i][2] == 0 and \
       len(el_inv) >= 2 and repetition[-1] == repetition[-2] and \
       mass_check[-1] == el_inv[-1] and mass_check[-2] == el_inv[-2]:      
           
            
            delta1 = abs(91.2 - el_inv[-2])
            delta2 = abs(91.2 - el_inv[-1])
        
            if delta1 > delta2:
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                repetition_fix.append(i)  
                      
            elif delta1 < delta2:
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i)  
                            
            else:
                print("We have delta1=delta2, need to upgrade code")
                continue
    
    #We get rid of extra data point from single 3 electron event
    #we choose between 1.-2. and 1.-3. electron pairs
    #We take the one that is closer to 91.2 GeV
    
    
    if df["Electron_charge"][i][0]+df["Electron_charge"][i][1] == 0 and \
       df["Electron_charge"][i][1]+df["Electron_charge"][i][2] == 0 and \
       len(el_inv) >= 2 and repetition[-1] == repetition[-2] and \
       mass_check[-1] == el_inv[-1] and mass_check[-2] == el_inv[-2]:
         
       
            delta1 = abs(91.2 - el_inv[-2])
            delta2 = abs(91.2 - el_inv[-1])
        
            if delta1 > delta2:
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                repetition_fix.append(i) 
        
            elif delta1 < delta2:
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i) 
                
            else:
                print("We have delta1=delta2, need to upgrade code")
                continue
    
    
    #We get rid of extra data point from single 3 electron event
    #we choose between 1.-2. and 2.-3. electron pairs
    #We take the one that is closer to 91.2 GeV
       
    if df["Electron_charge"][i][0]+df["Electron_charge"][i][2] == 0 and \
       df["Electron_charge"][i][1]+df["Electron_charge"][i][2] == 0 and \
       len(el_inv) >= 2 and repetition[-1] == repetition[-2] and \
       mass_check[-1] == el_inv[-1] and mass_check[-2] == el_inv[-2]: 
           
        
            delta1 = abs(91.2 - el_inv[-2])
            delta2 = abs(91.2 - el_inv[-1])
        
            if delta1 > delta2:
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                repetition_fix.append(i) 
        
            elif delta1 < delta2:
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i) 
            else:
                print("We have delta1=delta2, need to upgrade code")
                continue
     
    #We get rid of extra data point from single 3 electron event
    #we choose between 1.-3. and 2.-3. electron pairs
    #We take the one that is closer to 91.2 GeV 
                    
print("I have the raw data, {0:.3} s".format(time.time()-start))

repeat = []
repeat_del = []
repeating = []
for i in range(len(repetition)-1): # We check how many data points use the same data entry twice
    if repetition[i] == repetition[i+1]:
        repeat.append(repetition[i])
        
for i in range(len(repetition_fix)-1): # We check if we have deleted one of the double-data points
    if repetition_fix[i] == repetition_fix[i+1]:
        repeat_del.append(repetition_fix[i]) 
        
for i in range(len(repetition_check)-1): # We check if we use the same data point twice after our fix
    if repetition_check[i] == repetition_check[i+1]:
        repeating.append(repetition_check[i]) 
               
print("In total we got " + str(len(el_inv)) + " events!")

print("We used same event twice " + str(len(repeat)) + " times... We need to fix this somehow")

print("After our fix we used same event twice " + str(len(repeating)) + " times...")

print("Safety check. We deleted both of our double data points " + str(len(repeat_del)) + " times. This should be 0")

if len(repeat_del) == 0 and len(repeat) == len(repetition_fix): # We check whether we have deleted the same amount of points as were doubled at the start of the script
    print("Problem solved")
else:
    print("We deleted too few or too many data points!")


plt.figure(1)
#plt.xlabel("M, GeV")
#plt.ylabel("Frequency")
#plt.title("Tonis given NANOAOD with 'Formula', {0} entries, t={1:.0f} s".format(cik,time.time()-start))
#plt.xticks(np.arange(0,190,10))

#plt.hist(Pt_SUM,bins=180,range=[0,180],alpha=0.7,histtype=u'step')

plt.hist(Cosine,bins=100,range=[-1,1],alpha=0.7,histtype=u'step')
plt.xlabel("Cos(l1->l2), value")
plt.ylabel("Frequency")
plt.title("Toni given NANOAOD with 3 electron events, {0} entries, t={1:.0f} s".format(cik,time.time()-start))

plt.figure(2)
plt.hist(el_inv,bins=180,range=[0,180], alpha=0.7, histtype=u'step')
plt.xlabel("M, GeV")
plt.ylabel("Frequency")
plt.title("Toni given NANOAOD with 3 electron events, {0} entries, t={1:.0f} s".format(cik,time.time()-start))
plt.xticks(np.arange(0,190,10))
print("Ready to show, {0:.3f} s".format(time.time()-start))
#plt.savefig("{0}_pilnP.png".format(cik))
plt.show()
