# Numpy is your best friend when you have to handle numerical arrays of data.
import numpy as np

# Astropy offers some really nice FITS and conversion utils
# Our code requires astropy version >= 1.0
from astropy import units as u
from astropy.coordinates import SkyCoord, Galactic

# The TRUE Circle Constant (http://tauday.com/tau-manifesto).
TAU = np.pi * 2.


## SCIENCE ####################################################################


def _galactic2healpix(sky):
    """
    Acessing SkyCoord's properties is expensive, so we do it only once, and we
    also convert the coordinates to a spherical representation suitable
    for healpy. Also, note that sky properties are Quantities, with Units,
    and so are the returned values of this function.
    See astropy.units for more information about Quantities and Units.
    """
    lats = (90. * u.degree - sky.b) * TAU / 360.  # 90 is for colatitude
    lngs = sky.l * TAU / 360.

    return [lats, lngs]


def _wpix2hpix(coords, wcs, frame):
    """
    From WCS pixel referential (x/y) to HEALPix referential (lat/lon).

    coords: ndarray
        Of shape (2, ...)

    Returns two Quantities, each of shape (...) matching the input `coords`.
    """
    # The order of the axes for the result is determined by the CTYPEia
    # keywords in the WCS FITS header, therefore it may not always be of the
    # form (RA, dec). The lat, lng, lattyp and lngtyp members can be
    # used to determine the order of the axes.
    [lats, lngs] = wcs.all_pix2world(coords[0], coords[1], 0)
    sky = SkyCoord(lats, lngs, unit=u.degree, frame=frame)

    return _galactic2healpix(sky.transform_to(Galactic))


## SYSTEM #####################################################################


def _log(something):
    """
    Uninspired logging utility. Overwrite at will.
    Use the `logging` module instead of print ?
    """
    print("%s" % something)
