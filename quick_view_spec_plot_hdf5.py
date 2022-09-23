"""
23/09/2022
quick_view_spec_plot_hdf5.py
"""

import h5py,sys,os,glob
import numpy as np
import matplotlib.pyplot as plt

print('')
print("Example USAGE")
print('')
print('python3 quick_view_spec_plot_hdf5.py rawburst_osc_MSO_3045_22_09_2022_18_09_13_275169.hdf5 <fr/bin> <ymin> <ymax>')
print('')
print('fr/bin, ymin & ymax are optional parameters')
print('')

filename = str(sys.argv[1])
#filename = '/data/dsp/oscilloscope/22_09_2022_RRI/rawburst_osc_MSO_3045_23_09_2022_11_04_48_223444.hdf5'


with h5py.File(filename, "r") as hdf:
    base_item = list(hdf.items())
    #print(base_item)
    raw = hdf.get('raw_')
    raw_items = list(raw.items())
    #print(raw_items)
    data = np.array(raw.get('data'))
    #print(data)
    
a = data[0] 
nfft = 512 ;
b = len(a) % nfft    
c = len(a) - b       
a = (a[0:c])         
d = int(len(a)/nfft) 

spec = np.zeros((1,int(nfft/2)), dtype=int)
y3 = np.zeros((d,int(nfft/2)), dtype=int)

temp = a;
s = temp.reshape(d, nfft)
idx = 0
for idx in range(d):  
    y = (np.fft.fft(s[idx],nfft))
    y1 = np.square((np.absolute(y[0:int(nfft/2)])));
    y3[idx,0:int(nfft/2)] = y1    # 10*np.log(y3[0][1:])

mean = np.mean(y3, axis=0)

######### Ploting section #######
Fsamp = 1250 # MHz
print('Ploting without DC channel') 
print('Sampling frequency ', Fsamp, ' MHz')


if len(sys.argv) >= 3:
    freq = str(sys.argv[2])
     
if len(sys.argv) == 5:
    ymin = int(sys.argv[3])
    ymax = int(sys.argv[4])
    plt.ylim(ymin,ymax)
      
plt.plot((10*np.log(mean))[1:]) # Ploting without DC channel

if freq == 'fr':
    plt.xticks(np.arange(1, ((nfft/2)+1), 15), np.array((np.arange(1, ((nfft/2)+1), 15)*((Fsamp/2)/(nfft/2))), dtype = 'int'), fontsize = 7)
else:
    plt.xticks(np.arange(1, ((nfft/2)+1), 15), fontsize = 7)

plt.yticks(fontsize = 7)
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power (dB)")
plt.title(filename, fontsize = 8)
png_plot_name = (filename.rsplit('/')[-1])+'_.png'
plt.grid()
plt.savefig(png_plot_name, dpi=300)
print('Plot saved as ',png_plot_name)
plt.show()
