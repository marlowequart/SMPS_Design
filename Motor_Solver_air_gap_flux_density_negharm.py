#import matplotlib.pyplot as plt
#import numpy
from pylab import * 

#Number of magnetic poles:
Nm=8.
#Number of magnetic pole pairs:
Np=Nm/2.
#Magnet fraction (magnet inner radial length as a fraction of pi radians(one half of rotor)):
alph_m=0.25
#Magnet Remanence (Tesla)(V*s/(sq m)):
Br=1.1
#radius at Magnet to air-gap (m):
Rm=0.025273
#radius at air-gap to stator (m):
Rs=0.0260604
#radius to under side of magnet (m):
Rr=0.020828
#Magnet relative permability (H/m)(V*s/A*m):
mr=1.073170731

#Number of harmonics to calculate:
#(add 1 to number of harmonics desired)
harm=8

#Resolution on datapoints:
res=41
k=arange(0,res+1)		#number of samples

#air gap radial data points
dr=(Rs-Rm)/res
r=[999]
for i in range(1,res+2):
	r.append(Rm+k[i-1]*dr)
	
#air gap tangential data points
dthet=pi/(res)
thet=[999]
for i in range(1,res+2):
	thet.append(-pi/2.+k[i-1]*dthet)

#Parallel Magnetization Coefficients:
#Note, only valid for >1 pole pair
#Hanselman B.50, B.51, B.52
# alph_p=alph_m*pi/2.
# Krn=[999]
# Kthetn=[999]
# Mp=[999]
# for n in range(1,harm+1):
	# Mp.append(2.*Np/(pi*(1.-(n*n*Np*Np))))
	# if (n % 2 == 0):
		# Krn.append(0.)
		# Kthetn.append(0.)
	# else:
		# Krn.append(Mp[n]*(sin(alph_p/Np)*cos(alph_p*n)-n*Np*cos(alph_p/Np)*sin(alph_p*n)))
		# Kthetn.append(-1.j*Mp[n]*(cos(alph_p/Np)*sin(alph_p*n)-n*Np*sin(alph_p/Np)*cos(alph_p*n)))
		
#Radial Magnetization Coefficients:
#Hanselman B.49
Krn_m=[999]
Krn_p=[999]
Kthetn_m=[999]
Kthetn_p=[999]
for n in range(1,harm+1):
	x_p=n*alph_m*pi/2.
	x_m=-n*alph_m*pi/2.
	if (n % 2 == 0):
		Krn_m.append(0.)
		Krn_p.append(0.)
		Kthetn_m.append(0.)
		Kthetn_p.append(0.)
	else:
		Krn_m.append(alph_m*sin(x_m)/x_m)
		Krn_p.append(alph_m*sin(x_p)/x_p)
		Kthetn_m.append(0.)
		Kthetn_p.append(0.)
	#print'n={0},Krn_m={1},Krn_p={2}'.format(n,Krn_m[n],Krn_p[n])
		
#for i in Krn: print(i)
#print('\n')
#for i in Kthetn: print(i)

#Air Gap Region Solution Coefficients
#Hanselman B.29, B.30, B.31
Kmc_m=[999]
Kmc_p=[999]
Beta_m=[999]
Beta_p=[999]

delr1_m=[999]
delr1_p=[999]
delr2_m=[999]
delr2_p=[999]
delr_m=[999]
delr_p=[999]

Ka1_m=[999]
Ka1_p=[999]
Ka2_m=[999]
Ka2_p=[999]
Ka_m=[999]
Ka_p=[999]

for n in range(1,harm+1):
	Beta_p.append(n*Np)
	Beta_m.append(-n*Np)
	
	#B.31
	Kmc_p.append((Krn_p[n]+Beta_p[n]*Kthetn_p[n]*1.j)/(1.-Beta_p[n]*Beta_p[n]))
	Kmc_m.append((Krn_m[n]+Beta_m[n]*Kthetn_m[n]*1.j)/(1.-Beta_m[n]*Beta_m[n]))
	
	#B.30
	delr1_m.append((mr+1.)*((Rr/Rm)**(2.*Beta_m[n])-(Rs/Rm)**(2.*Beta_m[n])))
	delr1_p.append((mr+1.)*((Rr/Rm)**(2.*Beta_p[n])-(Rs/Rm)**(2.*Beta_p[n])))
	delr2_m.append((mr-1.)*(1.-(Rr/Rm)**(2.*Beta_m[n])*(Rs/Rm)**(2.*Beta_m[n])))
	delr2_p.append((mr-1.)*(1.-(Rr/Rm)**(2.*Beta_p[n])*(Rs/Rm)**(2.*Beta_p[n])))
	delr_m.append(delr1_m[n]+delr2_m[n])
	delr_p.append(delr1_p[n]+delr2_p[n])
	
	#B.29
	Ka1_m.append((Beta_m[n]-1.)+(Beta_m[n]+1.)*(Rr/Rm)**(2.*Beta_m[n])-(2.*Beta_m[n])*(Rr/Rm)**(Beta_m[n]+1))
	Ka1_p.append((Beta_p[n]-1.)+(Beta_p[n]+1.)*(Rr/Rm)**(2.*Beta_p[n])-(2.*Beta_p[n])*(Rr/Rm)**(Beta_p[n]+1))
	Ka2_m.append(1.-(Rr/Rm)**(2.*Beta_m[n]))
	Ka2_p.append(1.-(Rr/Rm)**(2.*Beta_p[n]))
	Ka_m.append(Ka1_m[n]*Ka2_m[n]*Kmc_m[n]*Krn_m[n]/delr_m[n])
	Ka_p.append(Ka1_p[n]*Ka2_p[n]*Kmc_p[n]*Krn_p[n]/delr_p[n])
	
	# print'n={0},Ka_m={1},Ka_p={2},Kmc_m={3},Kmc_p={4}'.format(n,"%.5f" % abs(Ka_m[n]),"%.5f" % abs(Ka_p[n]),"%.5f" % abs(Kmc_m[n]),"%.5f" % abs(Kmc_p[n]))
	# print'n={0},delr1_m={1},delr1_p={2},delr2_m={3},delr2_p={4}'.format(n,"%.5f" % abs(delr1_m[n]),"%.5f" % abs(delr1_p[n]),"%.5f" % abs(delr2_m[n]),"%.5f" % abs(delr2_p[n]))
	# print'Beta_m={2},Beta_p={3},delr_m={0},delr_p={1}'.format("%.5f" % abs(delr_m[n]),"%.5f" % abs(delr_p[n]),Beta_m[n],Beta_p[n])
	# print('/n')

#Triangular Weighted Average coefficients:
#coeff=[999]
#for n in range(1,harm+1):
#	coeff.append(2./harm-n*2./harm**2)

#At each radial point, evaluate the radial and tangential components of flux density
#for all harmonics being measured.

Bar=[[0 for x in range(res+1)] for x in range(res+1)]
mag_Bar=[[0 for x in range(res+1)] for x in range(res+1)]
mag_Bar_Rs=[]
Bat=[[0 for x in range(res+1)] for x in range(res+1)]
#l=radius
for l in range(1,res+2):
	#t=theta
	for t in range(1,res+2):
		Bar_h=[0.]
		Bat_h=[0.]
		#Batn2=[]
		#n=number of harmonic
		for n in range(1,harm+1):
			#Generate Fourier series coefficient for radial and theta for given harmonic #, radius, and angle:
			Barn_m=-1.*Br*Ka_m[n]*((r[l]/Rm)**(Beta_m[n]-1.)+(Rs/Rm)**(2.*Beta_m[n])*(Rm/r[l])**(Beta_m[n]+1))
			Barn_p=-1.*Br*Ka_p[n]*((r[l]/Rm)**(Beta_p[n]-1.)+(Rs/Rm)**(2.*Beta_p[n])*(Rm/r[l])**(Beta_p[n]+1))
			Batn_m=-1.j*Br*Ka_m[n]*((r[l]/Rm)**(Beta_m[n]-1.)-(Rs/Rm)**(2.*Beta_m[n])*(Rm/r[l])**(Beta_m[n]+1))
			Batn_p=-1.j*Br*Ka_p[n]*((r[l]/Rm)**(Beta_p[n]-1.)-(Rs/Rm)**(2.*Beta_p[n])*(Rm/r[l])**(Beta_p[n]+1))
			
			#store first positive harmonic component at r=Rs
			if n==1 and l==res+1:
				mag_Bar1=abs(Barn_p)
				Bar1_r=r[l]
				Bar1_cf=(r[l]/Rm)**(Beta_p[n]-1.)+(Rs/Rm)**(2.*Beta_p[n])*(Rm/r[l])**(Beta_p[n]+1)
			#	Bar1_cf2=(r[l]/Rm)**(Beta[n]-1.)+1.
			#	print 'r={0},n={1},thet={2},Barn={3}'.format(r[l],n,thet[t],Barn)
			#	#print 'Barn={0}'.format(Barn)
			#	print 'Ka={0}'.format(Ka[n])
			
			#Multiply coefficient by e^j,n,theta
			Barrt_m=Barn_m*exp(-n*1.j*thet[t])
			Barrt_p=Barn_p*exp(n*1.j*thet[t])
			
			Batrt_m=Batn_m*exp(-n*1.j*thet[t])
			Batrt_p=Batn_p*exp(n*1.j*thet[t])
			
			#print 'Bar={0}'.format(Barrt)
			#print 'e^n,j,thet={0}'.format(exp(n*1.j*thet[t]))
			#print ('\n')
			
			#Add the harmonic components together.
			Bar_h.append(Bar_h[n-1]+Barrt_p+Barrt_m)
			#Bar_h.append(Bar_h[n-1]+Barrt_m+Barrt_p)
			Bat_h.append(Bat_h[n-1]+Batrt_m+Batrt_p)
			
			#Batn2.append(-exp(n*1.j*t)*1.j*Br*Ka[n]*((r[l]/Rm)**(Beta[n]-1.)-(Rs/Rm)**(2.*Beta[n])*(Rm/r[l])**(Beta[n]+1)))
			#Barn_h.append(Barn_h[n-1]+coeff[n]*-Br*Ka[n]*((r[l]/Rm)**(Beta[n]-1.)+(Rs/Rm)**(2.*Beta[n])*(Rm/r[l])**(Beta[n]+1)))
			#Batn_h.append(Batn_h[n-1]+coeff[n]*-1.j*Br*Ka[n]*((r[l]/Rm)**(Beta[n]-1.)-(Rs/Rm)**(2.*Beta[n])*(Rm/r[l])**(Beta[n]+1)))
		#print(Bar_h)
		Bar[l-1][t-1]=Bar_h[harm]
		#print(Bar[l-1][t-1])
		#Results in Tesla
		mag_Bar[l-1][t-1]=abs(Bar_h[harm])
		Bat[l-1][t-1]=Bat_h[harm]
		#print 'r={0},thet={1},mag_Bar={2}'.format(r[l],thet[t],abs(Bar_h[harm]))
		
		#Input the magnitude of flux density for r=Rs, vary theta
		if l==res+1:
			mag_Bar_Rs.append(abs(Bar_h[harm]))
			#print 'theta={0},mag_Bar_Rs={1}'.format("%.4f" % thet[t],"%.4f" % mag_Bar_Rs[t-1])
	


#print("%.4f" % abs(Ka[1]))
#print 'Bar1(Rs)={1},Ka={0},Br={2},r={3},cf={4},cf2={5}'.format("%.6f" % abs(Ka[1]),"%.6f" % mag_Bar1,Br,Bar1_r,"%.6f" % Bar1_cf,"%.6f" % Bar1_cf2)
#print'Kmc*Krn/delr={0},Ka1={1},Ka2={2},Ka={3}'.format("%.6f" % abs(Krn[1]*Kmc[1]/delr[1]),"%.4f" % Ka1[1],"%.4f" % Ka2[1],"%.6f" % abs(Ka[1]))
#print 'Bar1(Rs)={1},Ka={0},Br={2},r={3}'.format("%.6f" % abs(Ka[harm+2]),"%.6f" % mag_Bar1,Br,Bar1_r)

#for i in mag_Bar:

	#print'e^n,j,thet={0}'.format(exp(n*1.j*thet[t]))
	#print('\n')
	
#Plot Radial Flux Density vs. Theta
thet.pop(0)
thet[:]=[x*57.29577 for x in thet]
fig=plt.figure(0)
ax1=fig.add_subplot(111)
lnse1=ax1.plot(thet, mag_Bar_Rs,color='b',label='F=1')
ax1.grid()
ax1.set_ylabel('Radial Flux Density (T)')
ax1.set_xlabel('Angular Position (Degrees)')
#ax1.set_title('Tank Capacitance for given operating point')

plt.show()