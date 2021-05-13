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

quadruple_del = []
triple_del = []
double_del = []

df=ds.query("nElectron==4") # We choose only 4 electron events
df=df.reset_index() # Reindex it

# Double - from one data entry, we get 2 data points, for example, we have 4 eletrons, and 1-2 and 1-3 pairs get counted, because they get through our filters
# Triple or T - from one data entry, we get 3 data points, for example, we have 4 eletrons, and 1-2, 1-3, 1-4 pairs get counted, because they get through our filters
# Quadruple or Q - from one data entry, we get 4 data points, for example, we have 4 eletrons, and 1-2, 1-3, 2-4 and 3-4 pairs get counted, because they get through our filters

print("I have the quadE, {1}, {0:.3f} s".format(time.time()-start,len(df["nElectron"])))

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
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
            
            
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
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
                    
    if df["Electron_charge"][i][0]+df["Electron_charge"][i][3] == 0: # 1.-4. electron pair analysis

        el1_pt = df["Electron_pt"][i][0]
        el1_eta = df["Electron_eta"][i][0]
        el1_phi = df["Electron_phi"][i][0]
        el2_pt = df["Electron_pt"][i][3]
        el2_eta = df["Electron_eta"][i][3]
        el2_phi = df["Electron_phi"][i][3]
        
        elec1 = ROOT.TLorentzVector()
        elec2 = ROOT.TLorentzVector()
        elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, el_mass)
        elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, el_mass)
        mass = (elec1+elec2).M()
        mass_check.append(mass)
        cosine = math.cos(elec1.Angle(elec2.Vect()))
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
        
        
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
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
        
        
    if df["Electron_charge"][i][1]+df["Electron_charge"][i][3] == 0: # 2.-4. electron pair analysis

        el1_pt = df["Electron_pt"][i][1]
        el1_eta = df["Electron_eta"][i][1]
        el1_phi = df["Electron_phi"][i][1]
        el2_pt = df["Electron_pt"][i][3]
        el2_eta = df["Electron_eta"][i][3]
        el2_phi = df["Electron_phi"][i][3]
        
        elec1 = ROOT.TLorentzVector()
        elec2 = ROOT.TLorentzVector()
        elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, el_mass)
        elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, el_mass)
        mass = (elec1+elec2).M()
        mass_check.append(mass)
        cosine = math.cos(elec1.Angle(elec2.Vect()))
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
                                    
            
            
    if df["Electron_charge"][i][2]+df["Electron_charge"][i][3] == 0: # 3.-4. electron pair analysis

        el1_pt = df["Electron_pt"][i][2]
        el1_eta = df["Electron_eta"][i][2]
        el1_phi = df["Electron_phi"][i][2]
        el2_pt = df["Electron_pt"][i][3]
        el2_eta = df["Electron_eta"][i][3]
        el2_phi = df["Electron_phi"][i][3]
        
        elec1 = ROOT.TLorentzVector()
        elec2 = ROOT.TLorentzVector()
        elec1.SetPtEtaPhiM(el1_pt, el1_eta, el1_phi, el_mass)
        elec2.SetPtEtaPhiM(el2_pt, el2_eta, el2_phi, el_mass)
        mass = (elec1+elec2).M()
        mass_check.append(mass)
        cosine = math.cos(elec1.Angle(elec2.Vect()))
        if mass > 70 and mass < 110:
            el_inv.append(mass)
            Cosine.append(cosine)
            repetition.append(i)
            repetition_check.append(i)
                    

    if len(el_inv) >= 4 and repetition[-1] == repetition[-2] and repetition[-1] == repetition[-3] and repetition[-1] == repetition[-4] and \
       mass_check[-1] == el_inv[-1] and mass_check[-2] == el_inv[-2] and mass_check[-3] == el_inv[-3] and mass_check[-4] == el_inv[-4]:      
            
            # We get rid of quadruple data points from event
                       
            delta1 = abs(91.2 - el_inv[-4])
            delta2 = abs(91.2 - el_inv[-3])
            delta3 = abs(91.2 - el_inv[-2])
            delta4 = abs(91.2 - el_inv[-1])
            
            if delta1 < delta2 and delta1 < delta3 and delta1 < delta4 :
                del el_inv[-3]
                del Cosine[-3]
                del repetition_check[-3]
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i)
                repetition_fix.append(i)
                repetition_fix.append(i) 
                quadruple_del.append(i) 
                      
            elif delta2 < delta1 and delta2 < delta3 and delta2 < delta4 :
                del el_inv[-4]
                del Cosine[-4]
                del repetition_check[-4]
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i)
                repetition_fix.append(i)  
                repetition_fix.append(i)
                quadruple_del.append(i)
                
            elif delta3 < delta1 and delta3 < delta2 and delta3 < delta4 :
                del el_inv[-4]
                del Cosine[-4]
                del repetition_check[-4]
                del el_inv[-3]
                del Cosine[-3]
                del repetition_check[-3]
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i)
                repetition_fix.append(i)
                repetition_fix.append(i)
                quadruple_del.append(i)  
            
            elif delta4 < delta1 and delta4 < delta2 and delta4 < delta3 :
                del el_inv[-4]
                del Cosine[-4]
                del repetition_check[-4]
                del el_inv[-3]
                del Cosine[-3]
                del repetition_check[-3]
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                repetition_fix.append(i)
                repetition_fix.append(i)
                repetition_fix.append(i)
                quadruple_del.append(i)
                                    
            else:
                print("We have equal deltas! Boi, you need to upgrade your code")
                continue                       
 
    if len(el_inv) >= 3 and repetition[-1] == repetition[-2] and repetition[-1] == repetition[-3] and \
       (mass_check[-1] == el_inv[-1] or mass_check[-2] == el_inv[-1] or mass_check[-3] == el_inv[-1] or mass_check[-4] == el_inv[-1]) and \
       (mass_check[-1] == el_inv[-2] or mass_check[-2] == el_inv[-2] or mass_check[-3] == el_inv[-2] or mass_check[-4] == el_inv[-2]) and \
       (mass_check[-1] == el_inv[-3] or mass_check[-2] == el_inv[-3] or mass_check[-3] == el_inv[-3] or mass_check[-4] == el_inv[-3]):      
            
            # We get rid of triple data points from single event
                       
            delta1 = abs(91.2 - el_inv[-3])
            delta2 = abs(91.2 - el_inv[-2])
            delta3 = abs(91.2 - el_inv[-1])
            
            if delta1 < delta2 and delta1 < delta3 :
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i)
                repetition_fix.append(i)
                triple_del.append(i)  
                      
            elif delta2 < delta1 and delta2 < delta3 :
                del el_inv[-3]
                del Cosine[-3]
                del repetition_check[-3]
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i)
                repetition_fix.append(i)
                triple_del.append(i)  
                
            elif delta3 < delta1 and delta3 < delta2 :
                del el_inv[-3]
                del Cosine[-3]
                del repetition_check[-3]
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                repetition_fix.append(i)
                repetition_fix.append(i)
                triple_del.append(i) 
                                
            else:
                print("We have equal deltas! Boi, you need to upgrade your code")
                continue  

    #if i == 2 and len(el_inv) >= 2 and repetition[-1] == repetition[-2]:      # First try, used this if cycle in combinating with next one to fix stuff, so double data deleting process wouldn't delete triple data events, but fixed it later.
                       
            #delta1 = abs(91.2 - el_inv[-2])
            #delta2 = abs(91.2 - el_inv[-1])
        
            #if delta1 > delta2:
                #del el_inv[-2]
                #del Cosine[-2]
                #del repetition_check[-2]
                #repetition_fix.append(i)  
                      
            #elif delta1 < delta2:
                #del el_inv[-1]
                #del Cosine[-1]
                #del repetition_check[-1]
                #repetition_fix.append(i)  
                            
            #else:
                #print("We have delta1=delta2, need to upgrade code")
                #continue  

    if len(el_inv) >= 2 and repetition[-1] == repetition[-2] and \
       (mass_check[-1] == el_inv[-1] or mass_check[-2] == el_inv[-1] or mass_check[-3] == el_inv[-1] or mass_check[-4] == el_inv[-1]) and \
       (mass_check[-1] == el_inv[-2] or mass_check[-2] == el_inv[-2] or mass_check[-3] == el_inv[-2] or mass_check[-4] == el_inv[-2]):      
            
            # We get rid of double data points from single event
                       
            delta1 = abs(91.2 - el_inv[-2])
            delta2 = abs(91.2 - el_inv[-1])
        
            if delta1 > delta2:
                del el_inv[-2]
                del Cosine[-2]
                del repetition_check[-2]
                repetition_fix.append(i)
                double_del.append(i)  
                      
            elif delta1 < delta2:
                del el_inv[-1]
                del Cosine[-1]
                del repetition_check[-1]
                repetition_fix.append(i)
                double_del.append(i)  
                            
            else:
                print("We have equal deltas! Boi, you need to upgrade your code")
                continue 
                       
            
            
            
print("I have the raw data, {0:.3} s".format(time.time()-start))


repeat2 = []
repeat3 = []
repeat4 = []
repeat_del2 = []
repeat_del3 = []
repeat_del4 = []
repeating2 = []
repeating3 = []
repeating4 = []


for i in range(len(repetition)-1): # We check how many data points use the same data entry twice, counts in triple and quadruple data entries aswell
    if repetition[i] == repetition[i+1]:
        repeat2.append(repetition[i])
        
for i in range(len(repetition)-2): # We check how many data points use the same data entry three times, counts in quadruple data entries aswell
    if repetition[i] == repetition[i+1] and repetition[i] == repetition[i+2]:
        repeat3.append(repetition[i])
        
for i in range(len(repetition)-3): # We check how many data points use the same data entry four times
    if repetition[i] == repetition[i+1] and repetition[i] == repetition[i+2] and repetition[i] == repetition[i+3]:
        repeat4.append(repetition[i])              
            
            



for i in range(len(repetition_fix)-1): # We check if we have deleted both data points from double data entry - Safety check -> should be 0
    if repetition_fix[i] == repetition_fix[i+1]:
        repeat_del2.append(repetition_fix[i])
        
for i in range(len(repetition_fix)-2): # We check if we have deleted all 3 data points from triple data entry - Safety check -> should be 0
    if repetition_fix[i] == repetition_fix[i+1] and repetition_fix[i] == repetition_fix[i+2]:
        repeat_del3.append(repetition_fix[i]) 
        
for i in range(len(repetition_fix)-3): # We check if we have deleted all four data points from quadruple data entry - Safety check -> should be 0
    if repetition_fix[i] == repetition_fix[i+1] and repetition_fix[i] == repetition_fix[i+2] and repetition_fix[i] == repetition_fix[i+3]:
        repeat_del4.append(repetition_fix[i])  
        




for i in range(len(repetition_check)-1): # We check if we used the same data point twice after our fix, counts in quadruple and triple events aswell
    if repetition_check[i] == repetition_check[i+1]:
        repeating2.append(repetition_check[i])
        
for i in range(len(repetition_check)-2): # We check if we used the same data point three times after our fix, counts in quadruple events aswell
    if repetition_check[i] == repetition_check[i+1] and repetition_check[i] == repetition_check[i+2]:
        repeating3.append(repetition_check[i])
        
for i in range(len(repetition_check)-3): # We check if we used the same data point four times after our fix
    if repetition_check[i] == repetition_check[i+1] and repetition_check[i] == repetition_check[i+2] and repetition_check[i] == repetition_check[i+3]:
        repeating4.append(repetition_check[i])    




print("In total we got " + str(len(el_inv)) + " events!")
print("\n")

print("We used same event twice " + str(len(repeat2)-2*(len(repeat3)-2*len(repeat4))-3*len(repeat4)) + " times...We need to fix this somehow") # We substract 2x T and 3x Q, because one triple entry gets counted as two double events, and quadruple gets counted as three double events
print("We used same event three times " + str(len(repeat3)-2*len(repeat4)) + " times... We need to fix this somehow") # We substract 2x T, because one qudruple gets counted as two triple events
print("We used same event four times " + str(len(repeat4)) + " times... We need to fix this somehow")
print("\n")

print("We got rid of " + str(len(double_del)) + " double events")
print("We got rid of " + str(len(triple_del)) + " triple events")
print("We got rid of " + str(len(quadruple_del)) + " quadruple events")
print("\n")

print("Safety check. We deleted both of our double data points " + str(len(repeat_del2)-len(triple_del)-2*len(quadruple_del)) + " times. This should be 0") # We substract 2x Q because for the algorithm it looks like triple event, and for double algorithm, the T gets calculated two times
print("Safety check. We deleted all three of our triple data points " + str(len(repeat_del3)-len(quadruple_del)) + " times. This should be 0")
print("Safety check. We deleted all four of our quadruple data points " + str(len(repeat_del4)) + " times. This should be 0")
print("Im 99% sure, this should be correct safety check, but again 99% not 100%!")
print("\n")

print("After our fix we used same event twice " + str(len(repeating2)-len(repeating3)-len(repeating4)) + " times...")
print("After our fix we used same event three times " + str(len(repeating3)-len(repeating4)) + " times... ")
print("After our fix we used same event four times " + str(len(repeating4)) + " times...")
print("\n")


plt.figure(1)
plt.hist(Cosine,bins=100,range=[-1,1],alpha=0.7,histtype=u'step')
plt.xlabel("Cos(lep1<->lep2), value")
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
