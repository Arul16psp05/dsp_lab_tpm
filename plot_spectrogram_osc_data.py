"""
USAGE: python3 plot_spectrogram_osc_data.py /data/dsp/oscilloscope/osc_obs/28_09_2022 0

"""
import h5py,sys,os,glob
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms

BW = 625
nfft = int(512);
D_point = int(9952);
chunk = int(D_point/nfft);

"""
data_dir = '/data/dsp/oscilloscope/osc_obs/28_09_2022'
ant_no = 0
"""
data_dir = str(sys.argv[1])
ant_no = int(sys.argv[2])

title_string = data_dir+' IP: '+str(ant_no)
"""
os.chdir(data_dir)
files = sorted(os.listdir())
"""

files = []; files = np.array(files, dtype='str')

for dirName, subdirs, fileList in os.walk(data_dir):
    print('Scanning %s...' % dirName) 
    filename = (glob.glob(dirName+"/*.hdf5"))
    files = np.append(files,filename)

pwr = np.zeros(np.size(files), dtype = 'float')
time = np.zeros(np.size(files), dtype='datetime64[ms]')
spec = np.zeros((np.size(files),int(nfft/2)), dtype = 'float')
full_spec = np.zeros((np.size(files),int(nfft/2)), dtype = 'float')

# RFI masking in spectrum
mask = np.ones((int(nfft/2)), dtype = 'float')
mask[:2] = 0       # mask for DC

for filename in range(len(files)):
    print( str(filename)+'/'+str(len(files)), '  ',int(100*filename/(len(files))-1),'% complete.', end ='\r')  
    #    print(str(filename)+'/'+str(len(files)), end ='\r')
    with h5py.File(files[filename], "r") as hdf:
        base_item = list(hdf.items())
        raw = hdf.get('raw_')
        raw_items = list(raw.items())
        data = np.array(raw.get('data'))
        data = (data[ant_no][:(np.size(data) - (np.size(data) % nfft))])
        temp = data.reshape((chunk,int(nfft)))
        time[filename] = datetime.datetime.fromtimestamp(os.path.getmtime(str(files[filename])))
    for raw in range(chunk):
        p_spec = ((np.abs(np.fft.fft(temp[raw],nfft)))**2)[0:int(nfft/2)]
        spec[raw] = p_spec
    pwr_spec = np.mean(spec, axis = 0)
    full_spec[filename]  = pwr_spec*mask
    pwr[filename] = np.abs(np.sqrt(np.mean(full_spec[filename])))


grid = plt.GridSpec(16, 8, wspace= 0.2, hspace= 0.2)

plt.subplot(grid[0:14,0:7]) 
plt.imshow(10*np.log(np.transpose(full_spec)), cmap ='viridis',interpolation ='none', aspect="auto", extent=[0,len(files),BW,0])
#, extent=[0,len(files),0,BW] 
plt.ylabel('Frequency (MHz)')
plt.title(title_string)

plt.subplot(grid[15:16,0:7]) 
plt.plot(10*np.log(pwr))
plt.xlabel('Spectrum number')
plt.ylim(5,12)

plt.subplot(grid[0:14,7:8]) 
plt.plot(10*np.log(np.mean(full_spec, axis = 0)), transform= transforms.Affine2D().rotate_deg(270) + plt.gca().transData)
plt.tick_params( left = False, labelleft = False )
plt.xlabel('Avg.spec power')

plt.show()

