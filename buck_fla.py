from matplotlib.pyplot import *
from numpy import *

tot_time=.02
nsamps=100000
saw_switch_freq=150000.
#max dt=6.66*10^-7 for sawtooth
#desired dt<10^13 for caps
#max # samps=100,000
#min time=600us
dt=tot_time/nsamps

n_range=arange(1,nsamps+1)

t=[]
for i in range(1,nsamps+1):
    t.append(n_range[i-1]*dt)


#Sense Resistors
R2_sense=100000.
R1_sense=100000.
#r_divide=R2/(R2+R1)

#Type III Error amp parameters
Vref=2.5
# feedback_pole1_f=20000.
# feedback_pole2_f=20000.
R1=200000.
R2=100000.
R3=5000.
C1=2.2*10**-9
C2=47.*10**-12
C3=1.*10**-9
K_lowpass1= 1.-2.7182**(-(1/(R2*C2))*dt)
K_lowpass2= 1.-2.7182**(-(1/(R3*C3))*dt)
error_amp_plus_rail=15.
error_amp_minus_rail=0.
integrator_minus_lim=-6.
integrator_plus_lim=6.

#PWM modulator
# pwm_plus_rail=5.
# pwm_minus_rail=0.
# pwm_vin_max=5.
# pwm_dc_max=1.
# pwm_gain=100.*pwm_dc_max/pwm_vin_max
#switcher params
Vin=28.

#LC filter params
L=100.*10**-6
LESR=0.1
C=44.*10**-6
CESR=90.*10**-3

#step load params
Ifixed=1.
Istep=0.

#measured params
v_divider=[2.50]
v_fbk_lp1=[2.49]
v_fbk_lp2=[2.49]
v_error=[.00001]
Rin_crnt=[0.1]
Cin_crnt=[0.1]
Iin_sum=[0.1]
VCin=[2.]
Iin_sum=[0.0001]
Vr_fbk=[0.1]
V_int_cap=[.34]
# IC_fbk=[0.01]
# VC_fbk=[1.6]
# VC_fbk_hold=[1.6]
# IC_int=[0.01]
# VC_int=[1.15]
V_eao=[.9]
# V_eao_hold=[.9]
# pwm_dc=[.5]
Vout=[28.]

L_vdrop=[0.]
L_crnt=[1.]
L_vesr=[.05]

C_volts=[5.]
C_crnt=[.9]
C_vesr=[.1]

v_sense=[5.01]
Iload=[1.]

##------------------------------------
## Sawtooth Gen
##------------------------------------

d_sw=1./saw_switch_freq
num_samp=round(d_sw/dt)
dy=5./num_samp
sawtooth=[0.]
cnt=0

for i in range(1,nsamps):
	cnt=cnt+1
	if (cnt>num_samp):
		sawtooth.append(0.)
		cnt=0
	else:
		sawtooth.append(sawtooth[i-1]+dy)

	


for i in range(1,nsamps):
	
##------------------------------------
## Type III Error Amp
##------------------------------------
	v_divider.append(R2_sense*(v_sense[i-1])/(R2_sense+R1_sense))
	
	v_fbk_lp1.append(v_fbk_lp1[i-1]+((v_divider[i]-v_fbk_lp1[i-1])*K_lowpass1))
	v_fbk_lp2.append(v_fbk_lp2[i-1]+((v_fbk_lp1[i]-v_fbk_lp2[i-1])*K_lowpass2))
	v_error.append(Vref-v_fbk_lp2[i])

	#input current
	# Rin_crnt.append((v_divider[i]-Vref)/R1)
	
	# Cin_crnt.append(round((2.*C1/(2.*R1*C1+dt))*(v_divider[i]-Vref-VCin[i-1])-(dt/(2.*R1*C1+dt))*Cin_crnt[i-1],4))
	# VCin.append(round(VCin[i-1]+(dt/C1)*((Cin_crnt[i]+Cin_crnt[i-1])/2),4))
	
	Rin_crnt.append(v_error[i]/R1)
	Cin_crnt.append((v_fbk_lp2[i]-v_fbk_lp2[i-1])*(C3/dt))
	
	Iin_sum.append(Rin_crnt[i]+Cin_crnt[i])
	
	#feedback stage current and voltage
	# IC_fbk.append((2.*C3/(2.*R3*C3+dt))*(-VC_fbk[i-1]-V_eao[i-1]+Vref)-(dt/(2.*R3*C3+dt))*IC_fbk[i-1])
	# VC_fbk.append(VC_fbk[i-1]+(dt/C3)*((IC_fbk[i]+IC_fbk[i-1])/2))
	
	# IC_int.append(Iin_sum[i]-IC_fbk[i])
	# VC_int.append(VC_int[i-1]+(dt/C2)*((IC_int[i]+IC_int[i-1])/2))
	
	# if ((Vref-(VC_int[i]+VC_fbk[i]))<=error_amp_minus_rail):
		# V_eao.append(error_amp_minus_rail)
	# elif ((Vref-(VC_int[i]+VC_fbk[i]))>=error_amp_plus_rail):
		# V_eao.append(error_amp_plus_rail)
	# else:
		# V_eao.append(Vref-(VC_int[i]+VC_fbk[i]))

	# V_eao.append(Vref+VC_int[i])
	
	if ((Iin_sum[i]*R2)<error_amp_minus_rail):
		Vr_fbk.append(error_amp_minus_rail)
	elif ((Iin_sum[i]*R2)>error_amp_plus_rail):
		Vr_fbk.append(error_amp_plus_rail)
	else:
		Vr_fbk.append(Iin_sum[i]*R2)
	

	if ((V_int_cap[i-1]+((Iin_sum[i-1]+Iin_sum[i])/2)*(dt/C2))<=integrator_minus_lim):
		V_int_cap.append(integrator_minus_lim)
	elif ((V_int_cap[i-1]+((Iin_sum[i-1]+Iin_sum[i])/2)*(dt/C2))>=integrator_plus_lim):
		V_int_cap.append(integrator_plus_lim)
	else:
		V_int_cap.append(V_int_cap[i-1]+((Iin_sum[i-1]+Iin_sum[i])/2)*(dt/C2))
	

	if ((Vref-(Vr_fbk[i]+V_int_cap[i]))<=error_amp_minus_rail):
		V_eao.append(error_amp_minus_rail)
	elif ((Vref-(Vr_fbk[i]+V_int_cap[i]))>=error_amp_plus_rail):
		V_eao.append(error_amp_plus_rail)
	else:
		V_eao.append(Vref-(Vr_fbk[i]+V_int_cap[i]))
	# V_eao.append(1.)

##------------------------------------
## Switcher
##------------------------------------

	if(V_eao[i]>sawtooth[i]):
		Vout.append(Vin)
	else:
		Vout.append(0.)

# #pwm modulator
	# if ((V_eao[i]-pwm_minus_rail)<=0.):
		# pwm_dc.append(0.)
	# elif (V_eao[i]>=pwm_plus_rail):
		# pwm_dc.append(pwm_dc_max)
	# else:
		# pwm_dc.append((V_eao[i]-pwm_minus_rail)*(.01*pwm_gain))
		
# #switcher
	# Vout.append(pwm_dc[i]*Vin)

##------------------------------------
## LC Filter
##------------------------------------


	L_vdrop.append(Vout[i]-v_sense[i-1])
	L_crnt.append(round(L_crnt[i-1]+((dt/L)*((L_vdrop[i-1]+L_vdrop[i])/2)),4))
	L_vesr.append(L_crnt[i]*LESR)
	# print(L_crnt)
	# print(Iload)
	C_crnt.append(L_crnt[i]-Iload[i-1])
	# print(C_crnt)
	C_vesr.append(C_crnt[i]*CESR)
	C_volts.append(round(C_volts[i-1]+((dt/C)*((C_crnt[i-1]+C_crnt[i])/2)),4))
	v_sense.append(C_vesr[i]+C_volts[i])

##------------------------------------
## Step Load
##------------------------------------
	if (t[i-1]<.25*tot_time):
		Iload.append(Ifixed)
	elif (t[i-1]>.25*tot_time) & (t[i-1]<.75*tot_time):
		Iload.append(Istep+Ifixed)
	else:
		Iload.append(Ifixed)
		


##------------------------------------
## Plots
##------------------------------------
# print(v_sense[1000:1010])
# print(v_divider[1000:1010])
# print()
# print(v_error[0:5])
# print()
# print(V_eao[0:5])
# print()
# print(pwm_dc[0:10])
# print()
# print(Vout[0:10])
# print()
# print(L_vdrop[0:10])
# print()
# print(L_crnt[0:100])
# print()
# print(L_vesr[0:10])
# print()
# print(IC_fbk[15000:15010])
# print()
# print(IC_int[15000:15010])
# print()
# print(VC_int[15000:15010])
# print(Iin_sum[1000:1010])
# print()

# subplot(121)
plot(t, v_sense,color='b')
# plot(t,L_crnt)
# plot(t, v_divider)
# plot(t,Iload)
plot(t,sawtooth, color='r')
# plot(t,Vout)
#plot(t,VC_int)
plot(t,Iin_sum, color='k')
# plot(t,IC_int, color='r')
# plot(t,IC_fbk, color='b')
#plot(t,VC_fbk,color='k')
# plot(t,Cin_crnt,color='c')
plot(t,Vr_fbk,color='b')
plot(t,V_int_cap,color='c')
#plot(t,pwm_dc,color='r')
plot(t,V_eao,color='g')
#plot(t,v_fbk_lp2,color='r')
#plot(t,v_error)
# xlim(.2*tot_time,.3*tot_time)
# ylim(-0.1,0.1)
ylabel('Voltage')
xlabel(r'Time')
title(r'Step Response')
# subplot(122)
# plot(t_2, v_sense,color='b')
# ylabel('Voltage')
# xlabel(r'Time')
# title(r'Step Response')
show()