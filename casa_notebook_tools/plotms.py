"""
Tools to enable plotms-like functionality
"""
import pylab as pl

from casatools import ms as mstool
ms = mstool()

def amp_vs_uvdist(msname, datacolumn='corrected_data', freqsel=slice(None),
                  data=None, weighted=False, flagthreshold=0.5):
    if data is None:
        ms.open(msname)
        ms.selectinit(reset=True)
        if weighted:
            data = ms.getdata(['model_data', 'data', 'corrected_data',
                              'uvdist', 'antenna1', 'antenna2', 'flag', 'weight'])
        else:
            data = ms.getdata(['model_data', 'data', 'corrected_data',
                              'uvdist', 'antenna1', 'antenna2', 'flag'])
        ms.close()

    autocorrs = data['antenna1'] == data['antenna2']

    if weighted:
        meanamp = np.abs(data[datacolumn][:,freqsel,:]).mean(axis=(0,1)) * data['weight'].mean(axis=0)
    else:
        meanamp = np.abs(data[datacolumn][:,freqsel,:]).mean(axis=(0,1))

    meanflag = data['flag'].mean(axis=(0,1))
    flagmask = meanflag > 0.5

    pl.plot(data['uvdist'][flagmask & ~autocorrs], meanamp[flagmask & ~autocorrs], 'r,')
    pl.plot(data['uvdist'][~flagmask & ~autocorrs], meanamp[~flagmask & ~autocorrs], ',')
    pl.xlabel("UV distance [m]")
    pl.ylabel("Amplitude")

def amp_vs_freq(msname, datacolumn='corrected_data', data=None):

    if data is None:
        ms.open(msname)
        ms.selectinit(reset=True)
        data = ms.getdata(['model_data', 'data', 'corrected_data',
                          'uvdist', 'antenna1', 'antenna2', 'flag'])
                          #'time', 'antenna1', 'antenna2',
                          #'axis_info', 'uvdist', 'weight', 'scan_number'])
        ms.close()

    autocorrs = data['antenna1'] == data['antenna2']

    pl.plot(data['corrected_data'][:,:,~autocorrs].mean(axis=(0,2)))
