import matplotlib.pyplot as plt
from numpy import *
from cmath import atan

#Type-3 E.A. inputs
R1=1000.
R2=22100.
R3=10.
C1=6.8*10**-9
C2=18.*10**-12
C3=82.*10**-9

# #Type-2 E.A. inputs
# R1=1000.
# R2=22100.
# C1=6.8*10**-9
# C2=180.*10**-12

#opamp open loop gain plot
R_amp=100.
C_amp=6.366*10**-6

#LC Elements
#Inductor
L=150.*10**-6
LESR=0.1
Lcap=10.*10**-12
#Capacitor
C=22.*10**-6
CESR=20.*10**-3
CESL=40.*10**-9
#parallel damping resistor
R=10.**12
#Sense resistors
R1=10000.
R2=10000.

#PWM gain
Vpwm=5.
DC=.178
max_switch_v=28.
Gpwm=DC*max_switch_v/Vpwm

nsamps=10000
df=10.

n_range=arange(1,nsamps+1)
freq=[]
for i in range(1,nsamps+1):
    freq.append(n_range[i-1]*df)

##------------------------------------
## LC Filter & Resistor Divider
##------------------------------------
Zfilt=[]
filt_trans=[]
filt_phase=[]

Zcap=[]
ZL=[]
for i in range(0,nsamps):
	Zcap.append(((2.j*pi*freq[i])**2*C*CESL+(2.j*pi*freq[i])*C*CESR+1)/((2.j*pi*freq[i])*C))
	ZL.append(((2.j*pi*freq[i])*L+LESR)/((2.j*pi*freq[i])**2*L*Lcap+(2.j*pi*freq[i])*Lcap*LESR+1))
	
for i in range(0,nsamps):
	#trans fxn with sense resistors
	#Zfilt.append(R2*((2.j*pi*freq[i])*C*CESR+1.)/((R2+R1)*(L*C*(2.j*pi*freq[i])**2+(2.j*pi*freq[i])*C*CESR+1.)))
	
	#with parallel damping resistor
	#Zfilt.append(R2*((2.j*pi*freq[i])*C*CESR+R)/((R2+R1)*(L*C*(CESR+R)*(2.j*pi*freq[i])**2+(2.j*pi*freq[i])*(L+C*CESR)+R)))
	
	#including parasitics & no sense resistors
	#Zfilt.append(Zcap[i]/(Zcap[i]+ZL[i]))
	#parasitics and sense resistors
	Zfilt.append(R2*Zcap[i]/((R2+R1)*(Zcap[i]+ZL[i])))
	#parasitics, sense resistors and damping resistor
	#Zfilt.append(R2*(Zcap[i]*R/(Zcap[i]+R))/((R2+R1)*((Zcap[i]*R/(Zcap[i]+R))+ZL[i])))
	filt_trans.append(linalg.norm(Zfilt[i]))
	#filt_phase.append(angle(Zfilt[i])*180/pi)

##------------------------------------
## Error Amp
##------------------------------------
Zi=[]
Zf=[]
tx=[]
ea_trans=[]
ea_phase=[]
op_amp=[]
op_amp_trans=[]

for i in range(0,nsamps):
	Zi.append(((2.j*pi*freq[i])*R3*R1*C3+R1)/((2.j*pi*freq[i])*(C3*R3+C3*R1)+1))
	Zf.append(((2.j*pi*freq[i])*R2*C1+1)/((2.j*pi*freq[i])**2*R2*C1*C2+(2.j*pi*freq[i])*(C2+C1)))
	tx.append(Zf[i]/Zi[i])
	ea_trans.append(linalg.norm(tx[i]))
	op_amp.append(39810.8/((2.j*pi*freq[i])*R_amp*C_amp+1.))
	op_amp_trans.append(linalg.norm(op_amp[i]))
#	ea_phase.append(angle(tx[i])*180/pi)

##------------------------------------
## Loop gain
##------------------------------------
GH=[]
G_CL=[]
GH_trans=[]
G_CL_trans=[]
GH_phase=[]
phase_marg=[]

for i in range(0,nsamps):
	GH.append(tx[i]*Zfilt[i]*Gpwm)
	GH_trans.append(linalg.norm(GH[i]))
	GH_phase.append(angle(GH[i])*180/pi)
	G_CL.append(GH[i]/(1+GH[i]))
	G_CL_trans.append(linalg.norm(G_CL[i]))
	phase_marg.append(GH_phase[i]+180.)

##------------------------------------
## Plots
##------------------------------------
# print(GH_phase[9999])
# print(90.+GH_phase[9999])
# print(phase_marg[9999])
fig=plt.figure(0)
ax1=fig.add_subplot(121)
ax1.semilogx(freq, 20*log10(filt_trans),color='b')
ax1.grid()
ax1.set_ylabel('Magnitude (dB)')
ax1.set_xlabel('Frequency')
ax1.set_title('LC Freq Response')
ax1=fig.add_subplot(122)
ax1.semilogx(freq, 20*log10(ea_trans),color='b')
ax1.semilogx(freq, 20*log10(op_amp_trans),color='c')
ax1.grid()
ax1.set_ylabel('Magnitude (dB)')
ax1.set_xlabel('Frequency')
ax1.set_title('Error Amp Response')
plt.show()


fig=plt.figure(1)
ax1=fig.add_subplot(111)
ax1.semilogx(freq, 20*log10(GH_trans),color='b',label='Open Loop Gain')
ax1.semilogx(freq, 20*log10(G_CL_trans),color='g',label='Closed Loop Gain')
ax1.grid()
ax1.set_ylabel('Magnitude (dB)')
ax1.set_xlabel('Frequency')
ax1.set_title('Buck Converter Response')
#ax1.set_ylim(-60,50)
ax2=ax1.twinx()
ax2.plot(freq,phase_marg,color='r',label='Phase Margin')
ax2.set_ylabel('Phase Margin (deg)')
#ax2.set_ylim(0,180)

ax1.legend(('Open Loop Gain', 'Closed Loop Gain'),loc=1)
#ax2.legend(('Phase Margin'),loc=7)
#ax1.set_xlim(10**3,10**6)
#plt.axvline(21000,color='c')
plt.show()