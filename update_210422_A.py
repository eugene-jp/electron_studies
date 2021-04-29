import time
start=time.time()
import uproot
import matplotlib.pyplot as plt
print("I have the libraries")


#mazais
#rootfile="root://cmsxrootd.fnal.gov////store/mc/RunIISummer16NanoAODv7/DYJetsToLL_Pt-50T$
#lielais
rootfile="root://cmsxrootd.fnal.gov////store/mc/RunIISummer16NanoAODv7/DYJetsToLL_Pt-50To$

tree = uproot.open(rootfile)["Events"]
now=time.time()
print("I have the tree, {0:.3f} s".format(now-start))
#print(tree.keys())

brun=["Electron_pt","HLT_DoubleEle33_CaloIdL","nElectron",
      "Electron_charge","HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf",
      "HLT_DoubleEle25_CaloIdL_GsfTrkIdVL","HLT_DoubleEle33_CaloIdL_MW",
      "HLT_DoubleEle33_CaloIdL_GsfTrkIdVL"]


df = tree.pandas.df(brun, entrystop=1799320)
now=time.time()
print("I saved the df, {0:.3f} s".format(now-start))

#ds=df.query("nElectron==2")

#hea=ds.head(10)
#print(hea)

divi,de24,de33,de33_Gs,de33_MW=[],[],[],[],[]
for i in range(len(df["Electron_pt"])):
        if df["nElectron"][i]==2:
                divi.append(df["Electron_pt"][i][0]+df["Electron_pt"][i][1])
                if df["HLT_DoubleEle33_CaloIdL"][i]==1:
                        de33.append(df["Electron_pt"][i][0]+df["Electron_pt"][i][1])
                if df["HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf"][i]==1:
                        de24.append(df["Electron_pt"][i][0]+df["Electron_pt"][i][1])
                if df["HLT_DoubleEle33_CaloIdL_MW"][i]==1:
                        de33_MW.append(df["Electron_pt"][i][0]+df["Electron_pt"][i][1])
                if df["HLT_DoubleEle33_CaloIdL_GsfTrkIdVL"][i]==1:
                        de33_Gs.append(df["Electron_pt"][i][0]+df["Electron_pt"][i][1])

now=time.time()
print("I sorted the data, {0:.3f} s".format(now-start))


#some=df.stack().values
plt.figure()
plt.hist(de33_MW,label="HLT_DoubleEle33_CaloIdL_MW", alpha=0.7, histtype=u'step')
plt.hist(de33,label="HLT_DoubleEle33_CaloIdL", alpha=0.7, histtype=u'step')
plt.hist(de24,label="HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf", alpha=0.7, histtype=u'step')
plt.hist(de33_Gs,label="HLT_DoubleEle33_CaloIdL_GsfTrkIdVL", alpha=0.7, histtype=u'step')

plt.xlabel("pt, GeV")
plt.ylabel("number")
plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
#plt.savefig("nanp_bins_30.png",bbox_inches='tight')
plt.show()
