"""
Tools to enable plotms-like functionality
"""
import pylab as pl

from casatools import ms as mstool
ms = mstool()

def amp_vs_uvdist(msname, datacolumn='corrected_data', freqsel=slice(None),
                  data=None):
    if data is None:
        ms.open(msname)
        ms.selectinit(reset=True)
        data = ms.getdata(['model_data', 'data', 'corrected_data',
                          'uvdist', 'antenna1', 'antenna2'])
                          #'time', 'antenna1', 'antenna2',
                          #'axis_info', 'uvdist', 'weight', 'scan_number'])
        ms.close()

    autocorrs = data['antenna1'] == data['antenna2']

    meanamp = np.abs(data[datacolumn][:,freqsel,:]).mean(axis=(0,1))

    pl.plot(data['uvdist'][~autocorrs], meanamp[~autocorrs], ',')
    pl.xlabel("UV distance [m]")
    pl.ylabel("Amplitude")

def amp_vs_freq(msname, datacolumn='corrected_data', data=None):

    if data is None:
        ms.open(msname)
        ms.selectinit(reset=True)
        data = ms.getdata(['model_data', 'data', 'corrected_data',
                          'uvdist', 'antenna1', 'antenna2'])
                          #'time', 'antenna1', 'antenna2',
                          #'axis_info', 'uvdist', 'weight', 'scan_number'])
        ms.close()

    autocorrs = data['antenna1'] == data['antenna2']

    pl.plot(data['corrected_data'][:,:,~autocorrs].mean(axis=(0,2)))
