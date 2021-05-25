import time
bigBang=time.time()
import glob,os
import pandas as pn

def wall_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{0:.0f}h:{1:.0f}min:{2:.0f}s".format(h,m,s)
def quarterz(this,total):
    if this==round(total/4):
        print("  25 %") 
    elif this==round(2*total/4):
        print("  50 %") 
    elif this==round(3*total/4):
        print("  75 %") 

n=0
num=0
for file in glob.glob("2017_dimass_test_*.txt"):
    n+=1
    print("{0}/{1}\t{2}".format(n,len(glob.glob("2017_dimass_test_*.txt")),
                                wall_time(time.time()-bigBang)))
    df=pn.read_csv(file, sep='\t',names=["dimass"])
    print(" has {0}".format(len(df["dimass"])))
    num+=len(df["dimass"])
    fo=open("2017_data.txt","a")
    for i in range(len(df["dimass"])):
        fo.write(str(df["dimass"][i])+"\n")
        quarterz(i,len(df["dimass"]))
    fo.close()
    
print("{0} All done".format(wall_time(time.time()-bigBang)))
print("Had {0} or {1:.2f} M or {2:.2f} G".format(num,num/10**6,num/10**9))
        
