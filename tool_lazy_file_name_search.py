### This recipe creates a .txt file with all the corresponding files 
### of a dataset(s)
### DISCLAIMER:
### This must be updated when more knowledge is aquired,
### it does the trick, but is a back-door way

### Two functions are employed that previously are defined
### in the .bashrc as:

###searchSample(){
###    dasgoclient -query="dataset=$1"
###}
###
###searchFiles(){
###    dasgoclient -query="file dataset=$1"
###}

### Since dasgoclient is used, proxy must be initiated 
### in the terminal at the beginning of the search with:
###voms-proxy-init --voms cms

### 0. I'm interested in datasets that match 
### dataset=/DoubleEG/Run2017*UL*NanoAODv9*/NANOAOD
### 1. In the terminal copy (choose a meaningful file name):
###searchSample /DoubleEG/Run2017*UL*NanoAODv9*/NANOAOD >> all_datasets_2017_UL_Nv9.txt
### 2. Then run this python code:
import pandas as pn
df=pn.read_csv("all_datasets_2017_UL_Nv9.txt", sep='\t',names=["nos"])
fo=open("search_all_files_2017_UL_Nv9.txt",'w')
for i in range(len(df)):
    out="searchFiles {0} >> all_files_2017_UL_Nv9.txt \n".format(df["nos"][i])
    fo.write(out)
fo.close()
### 3. locate the file search_all_files_2017_UL_Nv9.txt, 
### it contains lines that you should copy in the terminal 
### 4. Copy the lines (all with one copy-paste) in the terminal 
### and now you will obtain one .txt file (all_files_2017_UL_Nv9.txt)
### with one column containing the file(s) name.
### Later you can use it with 
###names=pn.read_csv("all_files_2017_UL_Nv9.txt", sep='\t',names=["nos"]) 
###for aiziet in range(len(names)):
###    rootfile="root://cmsxrootd.fnal.gov///"+names["nos"][aiziet]
