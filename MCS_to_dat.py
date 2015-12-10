
import numpy as np
import h5py
import sys
import os.path

h5_fname = sys.argv[1]
f = h5py.File(h5_fname, 'r')

d = f['/']
data = d['Data']
stream = data['Recording_0']['AnalogStream']['Stream_0']
cd = stream['ChannelData']  # this is the HDF5 stream containing the data
# this is the array of the info per channel, not used here but may be useful in the future
ci = stream['InfoChannel'][...]
data_array = cd[...].astype('int16')  # data are loaded as short integer
ch_map = np.genfromtxt('channelmap.csv')  # a csv file containing the channel mapping, for example as obtained in excel
ch_map -= 1  # make that 0-based
ch_map = ch_map.astype('int32')

data_array = np.transpose(data_array[ch_map, :])  # reshuffling the data in the right order and transposing them

outfile = os.path.splitext(h5_fname)[0] + '.dat'
data_array.tofile(outfile)  # save data in a .dat file
