#
#  This file is part of Healpy.
#
#  Healpy is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Healpy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Healpy; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#  For more information about Healpy, see http://code.google.com/p/healpy
#
"""Provides input and output functions for Healpix maps, alm, and cl.
"""
from __future__ import division

import six
import warnings
import astropy.io.fits as pf
import numpy as np

from healpy import pixelfunc
from healpy.pixelfunc import UNSEEN

standard_column_names = {
    1: "I_STOKES",
    3: ["%s_STOKES" % comp for comp in "IQU"],
    6: ["II", "IQ", "IU", "QQ", "QU", "UU"]
}


class HealpixFitsWarning(Warning):
    pass


def read_map(filename, field=0, dtype=np.float64, nest=False, partial=False, hdu=1, h=False, verbose=True,
             memmap=False, offset=0):
    """Read an healpix map from a fits file. Partial-sky files,
    if properly identified, are expanded to full size and filled with UNSEEN.

    Parameters
    ----------
    filename : str or HDU or HDUList
      the fits file name
    field : int or tuple of int, or None, optional
      The column to read. Default: 0.
      By convention 0 is temperature, 1 is Q, 2 is U.
      Field can be a tuple to read multiple columns (0,1,2)
      If the fits file is a partial-sky file, field=0 corresponds to the
      first column after the pixel index column.
      If None, all columns are read in.
    dtype : data type or list of data types, optional
      Force the conversion to some type. Passing a list allows different
      types for each field. In that case, the length of the list must
      correspond to the length of the field parameter. Default: np.float64
    nest : bool, optional
      If True return the map in NEST ordering, otherwise in RING ordering;
      use fits keyword ORDERING to decide whether conversion is needed or not
      If None, no conversion is performed.
    partial : bool, optional
      If True, fits file is assumed to be a partial-sky file with explicit indexing,
      if the indexing scheme cannot be determined from the header.
      If False, implicit indexing is assumed.  Default: False.
      A partial sky file is one in which OBJECT=PARTIAL and INDXSCHM=EXPLICIT,
      and the first column is then assumed to contain pixel indices.
      A full sky file is one in which OBJECT=FULLSKY and INDXSCHM=IMPLICIT.
      At least one of these keywords must be set for the indexing
      scheme to be properly identified.
      Note that this parameter has a lower priority than the OBJECT header card
      and is only used as fallback when the headers are not properly set.
    sparse : bool, optional
      If True, returns a `pandas.Series` object or a tuple of these, which are
      sparse unidimensional arrays. Useful only if you're reading partial-sky
      files with a high resolution and very few values, to save up on memory.
      You'll need the `pandas` library for this to work. Default: False.
    hdu : int, optional
      the header number to look at (start at 0)
    h : bool, optional
      If True, return also the header. Default: False.
    verbose : bool, optional
      If True, print a number of diagnostic messages
    memmap : bool, optional
      Argument passed to astropy.io.fits.open, if True, the map is not read into memory,
      but only the required pixels are read when needed. Default: False.

    Returns
    -------
    m | (m0, m1, ...) [, header] : array or a tuple of arrays, optionally with header appended
      The map(s) read from the file, and the header if *h* is True.
    """
    print("nest = %s" % str(nest))
    fits_hdu = _get_hdu(filename, hdu=hdu, memmap=memmap)

    nside = fits_hdu.header.get('NSIDE')
    if nside is None:
        warnings.warn("No NSIDE in the header file : will use length of array", HealpixFitsWarning)
    else:
        nside = int(nside)
    if verbose:
        print('NSIDE = {0:d}'.format(nside))

    if not pixelfunc.isnsideok(nside):
        raise ValueError('Wrong nside parameter.')
    ordering = fits_hdu.header.get('ORDERING', 'UNDEF').strip()
    print("ordering = %s" % ordering)
    if ordering == 'UNDEF':
        ordering = (nest and 'NESTED' or 'RING')
        warnings.warn("No ORDERING keyword in header file : "
                      "assume %s" % ordering)
    if verbose:
        print('ORDERING = {0:s} in fits file'.format(ordering))

    sz = pixelfunc.nside2npix(nside)
    ret = []

    # Detect whether the file is partial sky or not: check OBJECT
    obj = fits_hdu.header.get('OBJECT', 'UNDEF').strip()
    if obj != 'UNDEF':
        if obj == 'PARTIAL':
            partial = True
        elif obj == 'FULLSKY':
            partial = False

    # ... then check INDXSCHM
    schm = fits_hdu.header.get('INDXSCHM', 'UNDEF').strip()
    if schm != 'UNDEF':
        if schm == 'EXPLICIT':
            if obj == 'FULLSKY':
                raise ValueError('Incompatible INDXSCHM keyword')
            partial = True
        elif schm == 'IMPLICIT':
            if obj == 'PARTIAL':
                raise ValueError('Incompatible INDXSCHM keyword')
            partial = False

    if schm == 'UNDEF':
        schm = (partial and 'EXPLICIT' or 'IMPLICIT')
        warnings.warn("No INDXSCHM keyword in header file : assume {}".format(schm))
    if verbose:
        print('INDXSCHM = {0:s}'.format(schm))

    if field is None:
        field = range(len(fits_hdu.data.columns) - 1*partial)
    if not (hasattr(field, '__len__') or isinstance(field, str)):
        field = (field,)
    if partial:
        # increment field counters
        field = tuple(f if isinstance(f, str) else f+1 for f in field)
        try:
            pix = fits_hdu.data.field(0).astype(int, copy=False).ravel()
        except pf.VerifyError as e:
            print(e)
            print("Trying to fix a badly formatted header")
            fits_hdu.verify("fix")
            pix = fits_hdu.data.field(0).astype(int, copy=False).ravel()

    try:
        assert len(dtype) == len(field), "The number of dtypes are not equal to the number of fields"
    except TypeError:
        dtype = [dtype] * len(field)

    for ff, curr_dtype in zip(field, dtype):
        try:
            m = fits_hdu.data.field(ff).astype(curr_dtype, copy=False).ravel()
        except pf.VerifyError as e:
            print(e)
            print("Trying to fix a badly formatted header")
            m = fits_hdu.verify("fix")
            m = fits_hdu.data.field(ff).astype(curr_dtype).ravel()

        if partial:
            # if sparse:
            try:
                from scipy.sparse import coo_matrix
            except ImportError:
                raise ImportError("You need the `scipy` library in order "
                                  "to use the `sparse=True` feature.\n"
                                  "Try: pip install scipy")

            print('m.shape: ', m.shape)
            m -= offset

            mnew = coo_matrix((m, (np.zeros(len(m)), pix)), shape=(1, sz)).tocsr()

            if not nest is None:  # no conversion with None
                if nest and ordering == 'RING':
                    idx = pixelfunc.ring2nest(nside, pix)
                    print('Ordering converted to NEST')
                    mnew = coo_matrix((m, (np.zeros(len(m)), idx)), shape=(1, sz)).tocsr()
                elif (not nest) and ordering == 'NESTED':
                    idx = pixelfunc.nest2ring(nside, pix)
                    print('Ordering converted to RING')
                    mnew = coo_matrix((m, (np.zeros(len(m)), idx)), shape=(1, sz)).tocsr()
            # else:
            #    mnew = UNSEEN * np.ones(sz, dtype=curr_dtype)
            #    mnew[pix] = m
            m = mnew
            del mnew

#        if (not pixelfunc.isnpixok(m.size) or (sz>0 and sz != m.size)) and verbose:
#            print('nside={0:d}, sz={1:d}, m.size={2:d}'.format(nside,sz,m.size))
#            raise ValueError('Wrong nside parameter.')

        # no conversion with None
        if not partial and not nest is None:
            if nest and ordering == 'RING':
                print("converting to nest")
                idx = pixelfunc.nest2ring(nside, np.arange(sz, dtype=np.int32))
                print("end converting to nest")
                m = m[idx]
                del idx
                if verbose:
                    print('Ordering converted to NEST')
            elif (not nest) and ordering == 'NESTED':
                print("converting to ring")
                idx = pixelfunc.ring2nest(nside, np.arange(sz, dtype=np.int32))
                print("end converting to ring")
                m = m[idx]
                del idx
                if verbose:
                    print('Ordering converted to RING')

        try:
            if not partial:
                m[pixelfunc.mask_bad(m)] = UNSEEN
        except OverflowError:
            pass
        ret.append(m)

    if h:
        header = []
        for (key, value) in fits_hdu.header.items():
            header.append((key, value))

    if len(ret) == 1:
        if h:
            return ret[0], header
        else:
            return ret[0]
    else:
        if all(dt == dtype[0] for dt in dtype):
            ret = np.array(ret)
        if h:
            return ret, header
        else:
            return ret


# Generic functions to read and write column of data in fits file
def _get_hdu(input_data, hdu=None, memmap=None):
    """
    Return an HDU from a FITS file

    Parameters
    ----------
    input_data : str or HDUList or HDU instance
        The input FITS file, either as a filename, HDU list, or HDU instance.

    Returns
    -------
    fits_hdu : HDU
        The extracted HDU
    """

    if isinstance(input_data, six.string_types):
        hdulist = pf.open(input_data, memmap=memmap)
        return _get_hdu(hdulist, hdu=hdu)

    if isinstance(input_data, pf.HDUList):
        if isinstance(hdu, int) and hdu >= len(input_data):
            raise ValueError('Available hdu in [0-%d]' % len(input_data))
        else:
            fits_hdu = input_data[hdu]
    elif isinstance(input_data, (pf.PrimaryHDU, pf.ImageHDU, pf.BinTableHDU, pf.TableHDU, pf.GroupsHDU)):
        fits_hdu = input_data
    else:
        raise TypeError("First argument should be a input_data, HDUList instance, or HDU instance")

    return fits_hdu
