import uproot # this works with uproot 4.0.6
values, ex,ey = uproot.open('2017_ElectronMVA90.root')['EGamma_SF2D'].to_numpy()

fo=open("2017_mva90_iso_quick.txt","w")
fo.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format("pseido_no","pseido_lidz","pt_no","pt_lidz","SF"))
for eta in range(len(ex)-1):
    for pt in range(len(ey)-1):
        fo.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(ex[eta],ex[eta+1],ey[pt],ey[pt+1],values[eta,pt]))
fo.close()
