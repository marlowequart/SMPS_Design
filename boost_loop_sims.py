import matplotlib.pyplot as plt
from numpy import *
from cmath import atan

# input filter
L1=8.*10**-6
L1_esr=.002
C1=30.*10**-6
C2=5800.*10**-6
C2_esr=.55
# boost elements
#L3=13.*10**-6
L2=60.*10**-6
L2_esr=.0075
#R4=0.01
C3=10.*10**-6
C4=2900.*10**-6
C4_esr=.009
#C5=2900.*10**-6
#C5_esr=1.
R_load=5.3
Vin=28.
Vout=48.
# Hs=10000./(10000.+10000.)
D=1.-Vin/Vout
D_p=1.-D
Ts=1./100000

# Erickson Voltage Mode Gain Factors
Gd0=Vin/D_p
W0=D_p/((L2*C4)**0.5)
Wz=D_p*D_p*R_load/L2
Q=D_p*R_load*((C4/L2)**0.5)

#Gain factors
Ma=0.5*(Vin-Vout)/L2
Fm=1./(Ma*Ts)
Fv=D_p*D_p*Ts/(2.*L2)
Fg=(2.*D-1.)*Ts/(2.*L2)

#Compensation elements
Rin=30000.
Rf=50000.
Cf=47.*10**-9
Cf2=4700.*10**-12


nsamps=10000
df=10.

n_range=arange(1,nsamps+1)
freq=[]
for i in range(1,nsamps+1):
    freq.append(n_range[i-1]*df)
	
##------------------------------------
## Boost power stage Current Mode Control
##------------------------------------
Zo=[]
Za=[]
Zb=[]
ZL_in=[]
Ze=[]
Zf=[]
for i in range(0,nsamps):
	# Za.append(1.+((2.j*pi*freq[i])*C4*C4_esr))
	# Zb.append((2.j*pi*freq[i])*(((2.j*pi*freq[i])*C4*C3*C4_esr)+C4+C3))
	# Zo.append(Za[i]/Zb[i])
	Zo.append(1./((2.j*pi*freq[i])*(C3+C4)))
	#ZL with input filter 7-25-14
	Ze.append((2.j*pi*freq[i])*C2_esr*C2+1)
	Zf.append((2.j*pi*freq[i])*(L1_esr+(2.j*pi*freq[i])*L1)*(((2.j*pi*freq[i])*C2*C1*C2_esr)+C1+C2)+Ze[i])
	ZL_in.append(Ze[i]/Zf[i])

ZL=[]
ZL_noin=[]
Zload=[]
Gvd=[]
Gid=[]
Gvd_e=[]
Gvc=[]

VM_filt_trans=[]
VM_filt_phase=[]
VME_filt_trans=[]
VME_filt_phase=[]

PS_filt_trans=[]
PS_filt_phase=[]
PS_phase_marg=[]

for i in range(0,nsamps):
	# Zo.append(C_esr+1./((2.j*pi*freq[i])*C))
	
	ZL_noin.append((2.j*pi*freq[i])*L2+L2_esr)
	#ZL with input filter 7-25-14
	#ZL.append(ZL_in[i]*ZL_noin[i])
	#ZL with no input filter 7-25-14
	#ZL.append(ZL_noin[i]/(D_p*D_p))
	ZL.append((2.j*pi*freq[i])*L2/(D_p*D_p))
	Zload.append(R_load)
	# Zo.append(1/((2.j*pi*freq[i])*C))
	# ZL.append((2.j*pi*freq[i])*L2/(D_p*D_p))
	
	Gvd.append((Vin/D_p)*(Zload[i]*Zo[i]-ZL[i]*Zo[i])/(Zload[i]*Zo[i]+Zo[i]*ZL[i]+ZL[i]*Zload[i]))
	# Gvd_e.append(Gd0*(1.-(2.j*pi*freq[i])/Wz)/(1.+(2.j*pi*freq[i])/(Q*W0)+((2.j*pi*freq[i])/W0)**2))
	
	VM_filt_trans.append(linalg.norm(Gvd[i]))
	VM_filt_phase.append(angle(Gvd[i])*180/pi)
	# VME_filt_trans.append(linalg.norm(Gvd_e[i]))
	# VME_filt_phase.append(angle(Gvd_e[i])*180/pi)
	
	Gid.append((Vin/(D_p*D_p))*(2.*Zo[i]+Zload[i])/(Zo[i]*Zload[i]+ZL[i]*Zo[i]+ZL[i]*Zload[i]))
	
	Gvc.append(Gvd[i]*Fm/(1.+Fm*Fv*Gvd[i]+Fm*Gid[i]))
	
	PS_filt_trans.append(linalg.norm(Gvc[i]))
	PS_filt_phase.append(angle(Gvc[i])*180/pi)
	PS_phase_marg.append(PS_filt_phase[i]+180.)
	
##------------------------------------
## Boost Current Mode Control Loop Gain
##------------------------------------
Zf=[]
Gc=[]
Gc_trans=[]
Gc_phase=[]

Ts=[]
Ts_trans=[]
Ts_phase=[]
Ts_phase_marg=[]

for i in range(0,nsamps):
	Za.append(Rf+1./(Cf*(2.j*pi*freq[i])))
	Zb.append(1./(Cf2*(2.j*pi*freq[i])))
	Zf.append(Za[i]*Zb[i]/(Za[i]+Zb[i]))
	Gc.append(Zf[i]/Rin)
	
	Gc_trans.append(linalg.norm(Gc[i]))
	Gc_phase.append(angle(Gc[i])*180/pi)	

	Ts.append(Gvc[i]*Gc[i])

	Ts_trans.append(linalg.norm(Ts[i]))
	Ts_phase.append(angle(Ts[i])*180/pi)
	Ts_phase_marg.append(Ts_phase[i]+180.)
	
##------------------------------------
## Plots
##------------------------------------

fig=plt.figure(0)
ax1=fig.add_subplot(111)
lnse1=ax1.semilogx(freq, 20*log10(PS_filt_trans),color='b',label='P.S. Magnitude')
lnse2=ax1.semilogx(freq, 20*log10(Gc_trans),color='g',label='Comp Magnitude')
ax1.grid()
ax1.set_ylabel('Magnitude (dB)')
ax1.set_xlabel('Frequency')
ax1.set_title('Current Mode Boost, Control to Output Freq Response\nErickson Model Including Parasitics')
ax1.annotate("Boost L=60uH\nBoost C=2910uF\nR Load=5.3\nFs=100kHz\nVin=28V\nVout=48V",xy=(200,50),bbox=dict(boxstyle="square,pad=.5", fc="0.8"))

ax1.set_yticks(arange(-60,100,20))

ax2=ax1.twinx()
lnse3=ax2.plot(freq,PS_filt_phase,color='r',label='P.S. Phase')
lnse4=ax2.plot(freq,Gc_phase,color='k',label='Comp Phase')
ax2.set_ylabel('Phase (deg)')

lnse=lnse1+lnse2+lnse3+lnse4
labse=[l.get_label() for l in lnse]
ax1.legend(lnse,labse,loc=1)

plt.show()

fig=plt.figure(1)
ax1=fig.add_subplot(111)
lns1=ax1.semilogx(freq, 20*log10(Ts_trans),color='b',label='Open Loop Gain')
ax1.grid()
ax1.set_ylabel('Magnitude (dB)')
ax1.set_xlabel('Frequency')
ax1.set_title('Boost Loop Response')

ax2=ax1.twinx()
lns2=ax2.plot(freq,Ts_phase_marg,color='r',label='Phase Margin')
ax2.set_ylabel('Phase Margin (deg)')

lns=lns1+lns2
labs=[l.get_label() for l in lns]
ax1.legend(lns,labs,loc=1)
ax1.set_yticks(arange(-60,80,20))
ax1.grid(True, which='both')
#ax2.set_yticks(arange(0,140,20))
#ax2.set_ylim(0,120)
ax1.annotate("Crossover=36000 Hz",xy=(36000,0),arrowprops=dict(arrowstyle='->'),xytext=(100000,20))
ax2.annotate("Phase Margin=51 degrees",xy=(36000,51),arrowprops=dict(arrowstyle='->'),xytext=(30000,20))

#plt.show()