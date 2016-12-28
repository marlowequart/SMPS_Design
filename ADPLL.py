from pylab import *
from numpy import *
from scipy import *
from scipy.signal import *


num_wave=300					#num of waves in ref_clock
wave_samp=8						#samples per wave in ref_clock
n_samp=num_wave*wave_samp		#total samples in program
ref_clk_freq=10000.
dt=wave_samp/ref_clk_freq
input_freq=10.
input_n_wave=int(n_samp*dt*input_freq)+1

n_counter_set=2**4
o_counter_set=39				#nominal samples per output waveform cycle


##------------------------------------
## Test waveforms
##------------------------------------

ref_clk_waveform=[]
clk1_waveform=[]
for i in range(num_wave):
	ref_clk_waveform.append(1)
	# clk1_waveform.append(1)
	# clk1_waveform.append(0)
	ref_clk_waveform.append(0)
				
clk1_n_samp_per_wave=[20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20,
				20,20,20,20,20,20,20,20,20,20]
				
clk1_waveform=[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
				1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
				1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
				1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
				1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
				1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
				1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
				1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
				
# clk1_n_samp_per_wave=[]
# for i in range(3*input_n_wave):
	# clk1_n_samp_per_wave.append((1/input_freq)/(2*dt))
	
				
# output_n_samp_per_wave=[51,51,50,50,50,50,50,50,50,50,
				# 10,10,10,10,10,10,10,10,10,10,
				# 10,10,10,10,10,10,10,10,10,10,
				# 10,10,10,10,10,10,10,10,10,10,
				# 40,40,40,40,40,40,40,40,40,40,
				# 10,10,10,10,10,10,10,10,10,10]

clk_ref=[]
cnt=0
p=0
for x in range (0,n_samp):
	p=p+1
	if ref_clk_waveform[cnt]:
		clk_ref.append(1)
	else:
		clk_ref.append(0)
		
	if p==wave_samp/2:
		cnt=cnt+1
		p=0

clk1=[]
output_clk=[]
cnt=0
cnt2=0
p=0
q=0
for y in range (0,n_samp):
	p=p+1
	q=q+1
	if clk1_waveform[cnt]:
		clk1.append(1)
	else:
		clk1.append(0)
	
	if p==clk1_n_samp_per_wave[cnt]:
		cnt=cnt+1
		p=0

	# if ref_clk_waveform[cnt2]:
		# output_clk.append(1)
	# else:
		# output_clk.append(0)
		
	# if q==output_n_samp_per_wave[cnt2]:
		# cnt2=cnt2+1
		# q=0
		

n_range=arange(1,n_samp+1)
t=[]
for i in range(1,n_samp+1):
	t.append(n_range[i-1])

##------------------------------------
## main feedback loop
##------------------------------------

lead,lag,insert,delete=[0],[0],[],[]
enable_stream,not_enable_stream=[0],[0]
N_counter=0
O_counter=0
lag_high=0
lead_high=0
output_clk=[1]

for i in range(0, n_samp):


##------------------------------------
## Phase Comparator
##------------------------------------
		
	if (not clk1[i-1] and clk1[i]) and not output_clk[i]:
		lead_high=0
		lag_high=1
	
	if (not output_clk[i-1] and output_clk[i]) and clk1[i]:
		lead_high=0
		lag_high=0
		
	if (not output_clk[i-1] and output_clk[i]) and not clk1[i]:
		lag_high=0
		lead_high=1
		
	if (not clk1[i-1] and clk1[i]) and output_clk[i]:
		lag_high=0
		lead_high=0
		
	if lag_high:
		lag.append(1)
	else:
		lag.append(0)
		
	if lead_high:
		lead.append(1)
	else:
		lead.append(0)


##------------------------------------
## Divide by 'N' up/down counter
##------------------------------------

	if lead[i]>.2:
		N_counter=N_counter+1
	
	if lag[i]>.2:
		N_counter=N_counter-1

	if N_counter>n_counter_set:
		delete_high=0
		insert_high=1
		N_counter=0
	elif N_counter<-n_counter_set:
		delete_high=1
		insert_high=0
		N_counter=0
	else:
		delete_high=0
		insert_high=0
	
	if delete_high:
		delete.append(1)
	else:
		delete.append(0)
	
	if insert_high:
		insert.append(1)
	else:
		insert.append(0)


##------------------------------------
## Phase Adjustment Circuit
##------------------------------------


##------------------------------------
## Divide by M counter
##------------------------------------

	
	O_counter=O_counter+1
	
	if insert[i] and o_counter_set<41:
		o_counter_set=o_counter_set+1
	elif insert[i] and o_counter_set>=41:
		o_counter_set=41
			
	if delete[i] and o_counter_set>37:
		o_counter_set=o_counter_set-1
	elif delete[i] and o_counter_set<=37:
		o_counter_set=37

	if O_counter>o_counter_set/2.:
		output_high=1
	else:
		output_high=0
		

		
	if O_counter>=o_counter_set:
		O_counter=0
	
	if output_high:
		output_clk.append(1)
	else:
		output_clk.append(0)
	
#End of main feedback loop

##------------------------------------
## Plots
##------------------------------------

output_clk.pop(0)
lead.pop(0)
lag.pop(0)
enable_stream.pop(0)

for i in range(n_samp):
	clk1[i]=.95*clk1[i]
	output_clk[i]=.90*output_clk[i]
	lead[i]=.75*lead[i]
	lag[i]=.70*lag[i]
	insert[i]=.55*insert[i]
	delete[i]=.50*delete[i]


subplot(1,1,1)
plot(t,clk1,'.-')
#plot(t,clk_ref,'.-',color='r')
plot(t,output_clk,'.-',color='k')
plot(t,lead,'.-',color='c')
plot(t,lag,'.-',color='m')
plot(t,insert,'.-')
plot(t,delete,'.-')
# plot(t,enable_stream,'.-')



# ylabel('voltage')
xlabel('sample number')
grid()
#xlim(0, .000335)
# ylim(-.1,1.1)
#title('Square Wave')
show()
