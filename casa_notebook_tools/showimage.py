from casatools import image
from astropy.visualization import simple_norm
import pylab as pl

ia = image()


def showimage(imagename, title=None, stretch='asinh', mask=None, **kwargs):
    if isinstance(imagename, str):
        ia.open(imagename)
        data = ia.getchunk().squeeze()
        ia.close()
    else:
        data = imagename

    if 'percentiles' in kwargs:
        min_percent, max_percent = kwargs.pop('percentiles')
        kwargs['min_percent'] = min_percent
        kwargs['max_percent'] = max_percent

    if mask is not None:
        data = data.squeeze().T * mask.T,
    else:
        data = data.squeeze().T

    im = pl.imshow(data, norm=simple_norm(data, stretch=stretch, **kwargs),
                   origin='lower', interpolation='none',)

    if title is not None:
        pl.title(title)
    pl.gca().set_xticklabels([])
    pl.gca().set_yticklabels([])
    pl.colorbar()

    return im
