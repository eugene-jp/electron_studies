import numpy as np
import pandas as pn
import matplotlib.pyplot as plt
import scipy.stats as st
import scipy.optimize as opt

### šī ir mazliet random izvēlēta funkcija,
### Kārlis saka, ka jāliek Double sided Crystal ball 
### vērts izmēģināt scipy.stats.crystalball
f = lambda x, a, b, c, d: a*st.cauchy.pdf(x, b, c) + d/x**2
### fons lineārs, iespējams, jāņem labāks 
fb = lambda x, a, b: a*x+b

# šī ir vecā versija, kur visam viens koeficients
bi=180
koef=2.33
file_d="2017_UL_data_1.txt"
file_mc="2017_UL_mc.txt"
df_d=pn.read_csv(file_d, sep='\t',names=["mass"])
df_mc=pn.read_csv(file_mc, sep='\t',names=["mass"])

### fit for data
### nepieciešams numpy, lai sadala kā stabiņi un stabiņu platums
y_d, edges_d = np.histogram(df_d["mass"], bins=bi, range=(0, 180))
x_d = (edges_d[1:] + edges_d[:-1])/2 # atrod stabiņa vidu
yerr_d=np.sqrt(y_d) # kļūda statistiskā

### lai atrastu background signālu, izvēlos apgabalus abās pusēs pīķim
### vari paskatīties grafikos, varbūt Tu uzskati, ka jāņem citviet (plašāk, tālāk)
bck_d=(x_d>55)&(x_d<65)|(x_d>120)&(x_d<140) # mans izvēlētais apgabals
xb_d=x_d[bck_d]
yb_d=y_d[bck_d]
parametersb_d, errb_d = opt.curve_fit(fb, xb_d, yb_d, p0=(-1,1000)) # aproksimēju ar lineāru funkciju, kuras koeficientu sākuma minējumi ir -1 un 1k
# šī rindiņa ir funkcija, kas atrod koeficeintu vērtības, lai vislabāk raksturotu datus dotajā apgabalā

### no datiem (apgabalā no 55 līdz 125) atņemu background, ko saēķinu ar tikko iegūto formulu
s_d_y=y_d[(x_d>55)&(x_d<125)]-fb(x_d[(x_d>55)&(x_d<125)],*parametersb_d) # galā sanāk signāla stabiņu vērtības
s_d_x=x_d[(x_d>55)&(x_d<125)] # galā sanāk signāla x vērtības
parameters_d, err_d = opt.curve_fit(f, s_d_x, s_d_y, p0=(1000,90,90,-1)) # tagad signālas tiek fitots ar sākumā ieviesto funkciju, respektīvi, atrasti koeficeinti

### zīmēju data 
plt.bar(s_d_x,s_d_y,color="k", alpha=0.1, label="signal") # signāls
x_fit=np.linspace(55,125,100)
plt.plot(x_fit,f(x_fit,*parameters_d),label="Cauchy data") # fit for the signal

### MC tas pats
y_mc, edges_mc = np.histogram(df_mc["mass"], bins=bi, range=(0, 180)) # np atrod stabiņus
x_mc = (edges_mc[1:] + edges_mc[:-1])/2 # atrod viduspunktus
yerr_mc=np.sqrt(y_mc) # ieciparo kļūdu

### fonu meklēju tajos pašos reģionos
bck_mc=(x_mc>55)&(x_mc<65)|(x_mc>120)&(x_mc<140) # šis izdod an array of True vai False, respektīvi, vai punkts ir vai av manis izvēlētajos apgabalos
xb_mc=x_mc[bck_mc] # šo true vai false masku uzmetu x punktiem
yb_mc=y_mc[bck_mc] # šo true vai false masku uzmetu y punktiem
parametersb_mc, errb_mc = opt.curve_fit(fb, xb_mc, yb_mc, p0=(-1,1000)) # meklēju koeficeintus, lai raksturotu MC fonu

### tagad hops meklēt signālu
s_mc_y=y_mc[(x_mc>55)&(x_mc<125)]-fb(x_mc[(x_mc>55)&(x_mc<125)],*parametersb_mc) # no visiem datiem atņemu fitoto fonu
s_mc_x=x_mc[(x_mc>55)&(x_mc<125)] # vnk noīsinu, lai punkti ir tikai apgabalā, ko zīmēšu
parameters_mc, err_mc = opt.curve_fit(f, s_mc_x, s_mc_y, p0=(1000,90,90,-1)) # fitoju, lai atrastu koeficientus

### un tagad zīmēju stabiņus MC signālam 
plt.bar(s_mc_x,s_mc_y,color="k", alpha=0.1, label="signal")
x_fit=np.linspace(55,125,100)
plt.plot(x_fit,f(x_fit,*parameters_mc),label="Cauchy MC") # un fitu MC signālam

### Re ku ir iekomentēts paraugs, kā pieveino weights
### gadījumā, kad svari atrodas otrā kolonnā vnk saucam to
### līdzīgi kā weights=df["wights"]

#plt.hist(df_mc["mass"],bins=bi,range=[0,180], alpha=0.7,
#         histtype=u'step',weights=np.ones(len(df_mc["mass"]))*koef,label="MC")
#plt.errorbar(x,y,yerr,fmt="o",capsize=3,label="Data")


### piemetu dekorācijas
plt.xlabel("2_E, GeV")
plt.ylabel("Frequency")
plt.title("y2017, simple fit, without weights")
plt.xticks(np.arange(0,190,10))
plt.ylim([0,4000000])
plt.xlim([55,125])
plt.legend(loc="best")
plt.savefig("d_mc_combo_fit_redback.png") # saglabāju failu ar meaningful nosaukumu
plt.show()
