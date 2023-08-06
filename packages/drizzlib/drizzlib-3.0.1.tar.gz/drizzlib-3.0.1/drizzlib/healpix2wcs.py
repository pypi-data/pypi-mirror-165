# Core imports
import os.path
import sys
from datetime import datetime

from math import sqrt, atan2
# Numpy is your best friend when you have to handle numerical arrays of data
import numpy as np

# Healpy reads and writes [HEALPix](http://healpix.sourceforge.net/) files
# Documentation for query_disc and query_polygon can be found with the source:
# https://github.com/healpy/healpy/blob/master/healpy/src/_query_disc.pyx
import healpy as hp
from astropy.io.fits import BinTableHDU
from astropy.io.fits.hdu.base import _BaseHDU

from .fitsfuncdrizzlib import read_map
from .fitsfuncdrizzlib import _get_hdu

# Astropy offers some really nice FITS and coordinates conversion utils
# This package requires astropy version >= 1.0
from astropy import units as u
from astropy.coordinates import SkyCoord, Galactic
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import wcs_to_celestial_frame

# From our local C extension `c_package/optimized.c`.
# Helps us compute the intersection area between WCS pixels and HEALPix pixels.
from optimized import intersection_area

# Our private utils
from .utils import TAU, _wpix2hpix, _log


class SparseList(list):
    def __setitem__(self, index, value):
        missing = index - len(self) + 1
        if missing > 0:
            self.extend([None] * missing)
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        try:
            return list.__getitem__(self, index)
        except IndexError:
            return None


class Healpix2wcs(object):

    def __init__(self, healpix, field=1, header=None, header_hdu=0, output=None, crpix=None, cdelt=None,
                 pixel_size=None, crval=None, ctype=None, image_size=None, equinox=2000., is_sigma=False,
                 ignore_blank=True, blank_value=-32768, clobber=False, col_ids=None):

        self.healpix = healpix
        self.field = field
        self.header = header
        self.header_hdu = header_hdu
        self.output = output
        self.crpix = crpix
        self.cdelt = cdelt
        self.crota = None
        self.pixel_size = pixel_size
        self.crval = crval
        self.ctype = ctype
        self.image_size = image_size
        self.equinox = equinox
        self.is_sigma = is_sigma
        self.ignore_blank = ignore_blank
        self.blank_value, self.blank = blank_value, None
        self.clobber = clobber
        self.col_ids, self.nb_cols, self.rows = col_ids, None, None

        self.w, self.x_dim, self.y_dim, self.z_dim, self.scale_factor = None, None, None, None, None
        self.m, self.h = None, None
        self.wbis = None
        self.partial, self.nside, self.frame = None, None, None
        self.x_corner, self.y_corner, self.lat_corners, self.lng_corners = None, None, None, None
        self.cors_gal_x, self.cors_gal_y = None, None
        self.hpix_polys, self.wrap_healpixs = None, None
        self.data = None

    def find_nb_cols(self):
        """
        Determine number of columns to extract
        """
        if self.col_ids is None:
            self.col_ids = [0]
        self.nb_cols = len(self.col_ids)

    def create_header_wcs(self):
        """
        Create the WCS header with :
            - information in function parameters
            - information in the healpix header
        """

        if self.header is not None:
            # Read the keywords from the WCS FITS file provided as a template header
            h = fits.getheader(self.header, self.header_hdu)
            # We privilege the CDELT1/CDELT2 & CROTA2 convention
            # If CDELT1 and CDELT2 are present, we remove the CDmatrix keywords
            print("Found template header")
            if "CDELT1" in h and "CDELT2" in h:
                if "CD1_1" in h:
                    h.remove("CD1_1")
                if "CD1_2" in h:
                    h.remove("CD1_2")
                if "CD2_1" in h:
                    h.remove("CD2_1")
                if "CD2_2" in h:
                    h.remove("CD2_2")
            else:
                if "CD1_1" in h and "CD1_2" in h and "CD2_1" in h and "CD2_2" in h:
                    cd1_1 = h["CD1_1"]
                    cd1_2 = h["CD1_2"]
                    cd2_1 = h["CD2_1"]
                    cd2_2 = h["CD2_2"]
                    h.remove("CD1_1")
                    h.remove("CD1_2")
                    h.remove("CD2_1")
                    h.remove("CD2_2")
                    det = cd1_1*cd2_2 - cd1_2*cd2_2
                    if det < 0:
                        sgn=-1.
                    else:
                        sgn=1.
                        
                    cdelt1 = sgn*sqrt(cd1_1 ** 2 + cd1_2 ** 2)
                    cdelt2 = sqrt(cd1_1 ** 2 + cd2_1 ** 2)
                    print('cdelt1: '+str(cdelt1))
                    print('cdelt2: '+str(cdelt2))
                    self.crota = atan2(-cd1_2, cd2_2) * 57.2958
                    h["CDELT1"] = cdelt1
                    h["CDELT2"] = cdelt2
                elif "CD1_1" in h and "CD2_2" in h:
                    h.rename_keyword("CD1_1", "CDELT1")
                    h.rename_keyword("CD2_2", "CDELT2")
                    self.crota = 0.
                else:
                    raise ValueError("Cannot determine CDELT1 and CDELT2 from input WCS header.")

            w = WCS(h, naxis=2)
            # Extract the dimensions of the image from the header
            x_dim = h['NAXIS1']
            y_dim = h['NAXIS2']
            # Sanity check on -0.002778the WCS headers.
            # You probably don't need this if you're not us, but it has minimal
            # effect on performance and it's very convenient for us.
            # We simply assert against the presence of both `CDELTn` and `CDn_n`.
            if 'CDELT1' in h and 'CD1_1' in h:
                raise ValueError(
                    "Provided WCS headers have both CDELTn and CDn_n.")
        else:
            # User wants to provide the header keyword directly as keyword arguments
            def _missing1(_property, _type='number'):
                raise ValueError("Provide either a FITS filepath in `header=`, "
                                 "or a %ss in the property `%s=`."
                                 % (_type, _property))

            def _missing2(_property, _type='number'):
                raise ValueError("Provide either a FITS filepath in `header=`, "
                                 "or a pair of %ss in the property `%s=`."
                                 % (_type, _property))

            if self.crval is None:
                _missing2('crval')
            if self.ctype is None:
                _missing2('ctype', 'string')
            if self.image_size is None:
                _missing2('image_size')
            if self.cdelt is None:
                if self.pixel_size is None:
                    _missing1('pixel_size')
                self.cdelt = (-self.pixel_size, self.pixel_size)
            if self.crpix is None:
                self.crpix = (self.image_size[0] / 2., self.image_size[1] / 2.)

            # Create a new WCS object from scratch
            w = WCS(naxis=2)
            w.wcs.crpix = self.crpix
            w.wcs.cdelt = self.cdelt
            w.wcs.crval = self.crval
            w.wcs.ctype = self.ctype
            w.wcs.equinox = self.equinox

            x_dim = self.image_size[0]
            y_dim = self.image_size[1]

        if 'CAR' in w.wcs.ctype[0] or 'CAR' in w.wcs.ctype[1]:
            if x_dim == 1 or y_dim == 1:
                _log("The pixel dimensions of the output map must be greater than 1 along both axes.")
                return 1
            self.wbis = w.deepcopy()
            w.wcs.ctype[0] = w.wcs.ctype[0].replace('CAR', 'TAN')
            w.wcs.ctype[1] = w.wcs.ctype[1].replace('CAR', 'TAN')
            print('The map will be created using the (\'' + str(w.wcs.ctype[0]) + '\',\'' + str(w.wcs.ctype[1]) +
                  '\') projection, but will be reprojected to CAR before output.')
            print('Make sure that the reproject package is installed. Type \'pip install reproject\' if not.')
            self.scale_factor = 1.5
            w.wcs.crpix = self.scale_factor * w.wcs.crpix
            x_dim = self.scale_factor * x_dim
            y_dim = self.scale_factor * y_dim

        self.w = w
        self.x_dim = int(x_dim)
        self.y_dim = int(y_dim)

    def check_partial(self):
        """
        Check the healpix header to determine whether the sky coverage is PARTIAL or FULLSKY
        """
        fits_hdu = _get_hdu(self.healpix, hdu=self.field)

        # Detect whether the file is partial sky or not: check OBJECT
        obj = fits_hdu.header.get('OBJECT', 'UNDEF').strip()
        if obj != 'UNDEF':
            if obj == 'PARTIAL':
                self.partial = True
            elif obj == 'FULLSKY':
                self.partial = False
        # By default, the object in the header is "FULLSKY"
        else:
            self.partial = False

        # ... then check INDXSCHM
        schm = fits_hdu.header.get('INDXSCHM', 'UNDEF').strip()
        if schm != 'UNDEF':
            if schm == 'EXPLICIT':
                if obj == 'FULLSKY':
                    raise ValueError('Incompatible INDXSCHM keyword')
                self.partial = True
            elif schm == 'IMPLICIT':
                if obj == 'PARTIAL':
                    raise ValueError('Incompatible INDXSCHM keyword')
                self.partial = False

    def read_healpix_file(self):

        # Debug
        _log("Using Python %s" % sys.version)

        # Make sure we can write to the output file
        if os.path.isfile(self.output) and not self.clobber:
            raise ValueError(
                "The output file '%s' already exists! "
                "Set clobber=True to overwrite." % self.output
            )

        if self.nb_cols == 1:
            rows = self.col_ids[0]
        else:
            self.z_dim = self.nb_cols
            rows = ()
            for col_id in self.col_ids:
                rows += (col_id,)
        self.rows = rows

        # Read the input HEALPix FITS file.  /!\ Expensive operation !
        self.m, self.h = read_map(self.healpix, h=True, field=self.rows, hdu=self.field, offset=self.blank_value)

    def determine_blank_value(self):
        """
        Determine if we ignore BLANK values or not
        """

        # Define a private tool for accessing HEALPix header keyword values
        # as the header h returned by the method above is only a list of tuples.
        def _get_hp_card(_name, _default=None):
            for (_card_name, _card_value) in self.h:
                if _name == _card_name:
                    return _card_value
            return _default

        # Ignore BLANK values only if they are defined in the header
        self.blank = _get_hp_card('BLANK') or self.blank_value  # or -32768
        if self.blank is None:
            self.ignore_blank = False
        if self.ignore_blank:
            _log("Ignoring BLANK HEALPix pixels of value %.0f." % self.blank)
        else:
            _log("Not ignoring any blank pixels.")

    def collect_information_about_healpix(self):
        """
        Collect information about the HEALPix geometry: NSIDE, Frame
        """
        # Collect information about the HEALPix geometry (it's faster to do this only once)
        if self.partial:
            self.nside = hp.npix2nside(self.m.shape[1])
            _log("%d Nside." % self.nside)
            _log("%d HEALPix pixels in the whole map." % self.m.shape[1])
        else:
            self.nside = hp.get_nside(self.m)
            _log("%d Nside." % self.nside)
            if self.nb_cols == 1:
                _log("%d HEALPix pixels in the whole map." % hp.get_map_size(self.m))
            else:
                _log("%d HEALPix pixels in the whole map." % hp.get_map_size(self.m[0]))

        # Guess the coordinates frame from the WCS header keywords.
        # We rely on astropy methods here, so this may choke on illegal headers.
        frame = wcs_to_celestial_frame(self.w)
        _log("Coordinates frame is '%s'." % frame)

    def init_out_data(self):
        """
        Initialize the output data with the correct dimensions
        """
        # Instantiate the output data
        if self.nb_cols == 1:
            data = np.ndarray((self.y_dim, self.x_dim))
        else:
            data = np.ndarray((self.z_dim, self.y_dim, self.x_dim))
        self.data = data

    def finalize_data_output(self, z):
        """
        Fill the output data
        """
        if self.wbis is not None:
            if 'CAR' in self.wbis.wcs.ctype[0] or 'CAR' in self.wbis.wcs.ctype[1]:
                from reproject import reproject_exact
                self.data, footprint = reproject_exact((self.data, self.w), self.wbis,
                                                       shape_out=[int(self.y_dim / self.scale_factor),
                                                                  int(self.x_dim / self.scale_factor)])
                print('Reprojecting map in (\'' + str(self.wbis.wcs.ctype[0]) + '\',\'' + str(
                    self.wbis.wcs.ctype[1]) + '\') to CAR')
                self.w = self.wbis

        if self.is_sigma:
            surf_hpx = hp.nside2pixarea(self.nside, True)  # in degrees^2
            surf_wcs = float(self.w.wcs.cdelt[0]) ** 2
            ratio = 1. / sqrt(surf_hpx / surf_wcs)
            self.data *= ratio

    def collect_hpx_coordinates(self):
        # FIRST PASS
        # Collect the HPX coordinates of the center and corners of each WCS pixel.
        # We use the corners to efficiently select the healpixels to be drizzled into
        # each WCS pixel in the third pass.
        self.x_corner = np.ndarray((4, self.y_dim, self.x_dim))
        self.y_corner = np.ndarray((4, self.y_dim, self.x_dim))

        # WARNING: optimal padding (currently set to 10%) has NOT been rigorously determined.
        #          if the padding value is too low, results are incorrect
        #          if it is too high, performance suffers
        #          the current value of 10% is a best guestimate that has not been rigorously tested.
        pad = 0.5 * 1.05  # bigger, to compensate the non-affine transformation

        for x in range(self.x_dim):
            for y in range(self.y_dim):
                self.x_corner[:, y, x] = np.array([x - pad, x + pad, x + pad, x - pad])
                self.y_corner[:, y, x] = np.array([y + pad, y + pad, y - pad, y - pad])

        # Transforming coordinates to the Galactic referential is faster with
        # one SkyCoord object than with many, hence this first pass, which enables
        # us to vectorize the transformation.
        self.frame = wcs_to_celestial_frame(self.w)
        [self.lat_corners, self.lng_corners] = _wpix2hpix([self.x_corner, self.y_corner], self.w, self.frame)

    def use_intersection_surface(self, z):
        # SECOND PASS : We use an intersection-surface weighed mean.
        # As converting our HEALPix polygons into pixel coords
        # is very expensive (approx 84% of total time), we vectorize this operation.
        # This means selecting the HEALPix pixels intersecting with our
        # WCS image in an initial step. We do this by creating a polygon around our WCS image,
        # and using that polygon with the `query_polygon` method of healpy. 
        # This makes the code harder to understand, but much faster.
        # Memoization holder for the cartesian vertices of HEALPix on
        # the flat plane of the projection.
        if self.partial:
            self.hpix_polys = SparseList()
        else:
            if self.nb_cols == 1:
                self.hpix_polys = [None] * hp.get_map_size(self.m)
            else:
                self.hpix_polys = [None] * hp.get_map_size(self.m[z])

        # The above list initialization is much, much faster than :
        # hpix_polys = [None for _ in range(hp.get_map_size(m))]

        # As the referential change from HEALPix to WCS is non-affine, a
        # rectangle of the size of the WCS image is not sufficient,
        # as it will miss some HEALPix pixels.
        # So we (arbitrarily!) pad it to make it a little bigger.
        # The optimal padding can probably be mathematically computed,
        # but we have other priorities for now.
        # WARNING: THIS WILL CRASH AND BURN WITH WHOLE SKY CAR PROJECTIONS
        pad = 0.05 * (self.x_dim + self.y_dim) / 2.
        wrap_poly_vertices = np.transpose(np.array([
            [-0.5 - pad, -0.5 - pad],
            [-0.5 - pad, self.y_dim - 0.5 + pad],
            [self.x_dim - 0.5 + pad, self.y_dim - 0.5 + pad],
            [self.x_dim - 0.5 + pad, -0.5 - pad],
        ]))
        wrap_poly_hp = _wpix2hpix(wrap_poly_vertices, self.w, self.frame)

        del self.frame
        del wrap_poly_vertices

        wrap_poly_hp = hp.ang2vec([v.value for v in wrap_poly_hp[0]],
                                  [v.value for v in wrap_poly_hp[1]])
        self.wrap_healpixs = hp.query_polygon(self.nside, wrap_poly_hp,
                                              inclusive=True)
        del wrap_poly_hp

        _log("%d HEALPix pixels in the WCS wrapper polygon." % len(self.wrap_healpixs))

        # Collect the vector coordinates of the corners in the hp ref.
        # [ [x1, x2, ..., xn], [y1, y2, ..., yn], [z1, z2, ..., zn] ]
        corners_hp_vec = np.ndarray((3, len(self.wrap_healpixs) * 4))
        for i in range(len(self.wrap_healpixs)):
            # [ [x1, x2, x3, x4], [y1, y2, y3, y4], [z1, z2, z3, z4] ]
            corners = hp.boundaries(self.nside, self.wrap_healpixs[i])
            j = i * 4
            corners_hp_vec[0][j:j + 4] = corners[0]
            corners_hp_vec[1][j:j + 4] = corners[1]
            corners_hp_vec[2][j:j + 4] = corners[2]

        # Convert the corners into (theta, phi) (still in hp ref.)
        # [ [t1, t2, ..., tn], [p1, p2, ..., pn] ]
        corners_hp_ang = hp.vec2ang(np.transpose(corners_hp_vec))

        del corners_hp_vec

        # Build the (expensive!) SkyCoord object with all our coords
        sky_b = -1 * (corners_hp_ang[0] * 360. / TAU - 90.)
        sky_l = corners_hp_ang[1] * 360. / TAU
        sky = SkyCoord(b=sky_b, l=sky_l, unit=u.degree, frame=Galactic)

        del corners_hp_ang

        # Convert the corners to WCS pixel space
        self.cors_gal_x, self.cors_gal_y = sky.to_pixel(self.w)

    def rastherize_healpixels(self, x, z):
        # THIRD PASS : rasterize healpixels on the (finite) WCS grid,
        # picking a mean weighted by the intersection area.
        # For each WCS pixel in the WCS image...
        for y in range(self.y_dim):

            # Vertices of the WCS pixel in WCS pixel space
            wpix_poly = np.array([
                [x - 0.5, y - 0.5],
                [x - 0.5, y + 0.5],
                [x + 0.5, y + 0.5],
                [x + 0.5, y - 0.5],
            ])

            # Tallies to compute the weighted arithmetic mean
            total = 0
            value = 0

            # Find all the HEALPix pixels that intersect with a polygon
            # slightly bigger than the pixel, whose vertices were computed
            # in the first pass.
            # Those are Quantity objects, so we pick their `value`.
            wrap_pix = hp.ang2vec(self.lat_corners[:, y, x].value,
                                  self.lng_corners[:, y, x].value)
            hpix_ids = hp.query_polygon(self.nside, wrap_pix, inclusive=True)
            # For each HEALPix pixel, we're going to figure out its
            # contribution to the WCS pixel (how much they intersect)
            for hpix_id in hpix_ids:

                # Healpy might return -1 when not found, ignore those.
                if hpix_id == -1:
                    continue

                if self.partial:
                    hpix_value = self.m[0, hpix_id]
                    hpix_value += self.blank_value
                else:
                    if self.nb_cols == 1:
                        hpix_value = self.m[hpix_id]
                    else:
                        hpix_value = self.m[z][hpix_id]
                # Ignore BLANK values if configuration allows.
                if self.ignore_blank and hpix_value == self.blank_value:
                    continue
                if self.ignore_blank and hpix_value == self.blank:
                    continue

                j = np.where(self.wrap_healpixs == hpix_id)
                j = 4 * j[0]

                hpix_poly = np.transpose([self.cors_gal_x[j[0]:j[0] + 4], self.cors_gal_y[j[0]:j[0] + 4]])

                if hpix_poly is None:
                    # Even though we try to index the polygons in one
                    # fell swoop to avoid the expensive instantiation of a
                    # SkyCoord object, some pixels might fall through the
                    # cracks and need to be converted on the fly.
                    # It's okay if this happens a couple of times,
                    # but if it happens too often, performance suffers.
                    _log("\nWarning: healpixel %s escaped optimization." % hpix_id)

                    corners = hp.boundaries(self.nside, hpix_id)
                    theta_phi = hp.vec2ang(np.transpose(corners))

                    sky_b = -1 * (theta_phi[0] * 360. / TAU - 90.)
                    sky_l = theta_phi[1] * 360. / TAU
                    sky = SkyCoord(b=sky_b, l=sky_l, unit=u.degree,
                                   frame=Galactic)

                    # Finally, make a list of (x, y) in pixel referential
                    hpix_poly = np.transpose(sky.to_pixel(self.w))
                    # ...which we memoize
                    self.hpix_polys[hpix_id] = hpix_poly

                # Optimized C implementation of Sutherland-Hodgeman
                # `intersection_area` is defined in `c_package/optimized.c`.
                # The intersection is computed in pixel space.
                shared_area = intersection_area(hpix_poly, 4, wpix_poly, 4)
                total += shared_area
                value += shared_area * hpix_value

            if total != 0:
                v_drizzle = value / total
            else:
                v_drizzle = np.nan
                _log("Warning: Sum of weights is 0 on pixel (%d, %d)." % (x, y))

            if self.nb_cols == 1:
                self.data[y, x] = v_drizzle
            else:
                self.data[z, y, x] = v_drizzle
        progress = x / float(self.x_dim)
        _log('Processing line {:3d}/{:d} ({:4.1f}%) [{:40s}]'.format(x, self.x_dim, 100 * progress,
                                                                     '#' * int(progress * 41)))

    def write_processing_line(self):
        """
        Report on progress in terms of lines processed
        """
        _log('Processed line  {:3d}/{:d} (100%)  [{:40s}]\n'.format(self.x_dim, self.x_dim, '#' * 40))

    def write_fits_res(self):
        """
        Write the output data into a WCS FITS
        """
                
        if self.output is not None:
            hdul = fits.PrimaryHDU(self.data)
            hdr = hdul.header
            hdr["WCSAXES"] = self.z_dim
            hdr["NAXIS1"] = self.x_dim
            hdr["NAXIS2"] = self.y_dim
            hdr["CRPIX1"] = self.w.wcs.crpix[0]
            hdr["CRPIX2"] = self.w.wcs.crpix[1]
            hdr["CDELT1"] = self.w.wcs.cdelt[0]
            hdr["CDELT2"] = self.w.wcs.cdelt[1]
            if self.crota is not None:
                hdr["CROTA2"] = self.crota
            hdr["CRVAL1"] = self.w.wcs.crval[0]
            hdr["CRVAL2"] = self.w.wcs.crval[1]
            hdr["CTYPE1"] = self.w.wcs.ctype[0]
            hdr["CTYPE2"] = self.w.wcs.ctype[1]

            if self.h is not None:
                print("found a header")
                tag_exclude_list = ['XTENSION','BITPIX','NAXIS','NAXIS1','NAXIS2','PCOUNT','GCOUNT','TFORM1','TTYPE1','PIXTYPE','TFIELDS','COMMENT','DATAMIN','DATAMAX','GRAIN','INDXSCHM','COORDSYS']
                for (_card_name, _card_value) in self.h:
                    if _card_name not in tag_exclude_list:
                        hdr[_card_name] = (_card_value, 'Inherited from Healpix header')

            current_time = str(datetime.now())
            hdr["HISTORY"] = 'This WCS extracted by CADE healpix2wcs.py '+current_time
            hdul.writeto(self.output, overwrite=self.clobber)


# Function healpix2wcs :
def healpix2wcs(
        healpix,
        field=1,
        header=None,
        header_hdu=0,
        output=None,
        crpix=None, cdelt=None,
        pixel_size=None,
        crval=None, ctype=None,
        image_size=None,
        equinox=2000.,
        is_sigma=False,  # fixme
        ignore_blank=True,
        blank_value=-32768,
        clobber=False,
        col_ids=None):
    """
    Extract a rectangular image in WCS format from the provided HEALPix.
    The characteristics of the output WCS image are determined either by a
    user-supplied template header (i.e. a WCS FITS file path, from which we extract header keywords),
    or directly by providing input parameters to this function.
    healpix: str
        The path to the input HEALPix file to read from. No default.
    field: int
        The id of the HDU (Header Data Unit) to read in the HEALPix FITS file. Defaults to 1.
    header: file path, file object, or file-like object
        A string with (path to the) WCS FITS file to use as a template.
        If an opened file object, its mode must be one of the following :
        `rb`, `rb+`, or `ab+`.
    header_hdu: int
        The id of the HDU (Header Data Unit) to read in the header of the template WCS FITS file. Defaults to 0.
    output: str
        The path to the output WCS FITS file that will be generated.
    crpix: float[2]
        Pixel coordinates of the image reference pixel. Equivalent to the CRPIXn WCS FITS keywords.
        A pair of floats in X,Y order.
        If you do not provide a template header, you should specify this value.
        By default, the (x,y) pixel coordinates of the center of the WCS image,
        determined using the image_size parameter.
    cdelt: float[2]
        Angular dimensions of one pixel. Equivalent to the CDELTn WCS FITS keywords. Unit: degrees.
        A pair of floats in X,Y order.
        If you do not provide a template header, you should specify this value or the
        pixel_size parameter.
        cdelt takes precedence over pixel_size if both are specified.
    pixel_size: float
        The angular size of a square pixel in the output WCS. Unit: degrees.
        Will be used to determine the cdelt keywords if it is not specified.
        If you do not provide a template WCS FITS header, you must specify this value or the
        cdelt parameter.
        pixel_size has a lower priority than cdelt if both are provided.
    crval: float[2]
        The celestial coordinates at the image reference pixel.
        Equivalent to the CRVALn WCS FITS keywords. Unit: degrees.
        A pair of floats in X,Y order.
        If you do not provide a template header, you must specify this value.
        As crpix defaults to the center of the image, this value should be
        the coordinates of the center of the output WCS image if you do not specify crpix.
    ctype: str[2]
        The coordinate type and projection of the image axes.
        Equivalent to the CTYPEn WCS FITS keywords.
        A pair of 8 character strings in X,Y order
        Recall that the FITS standard requires a string of format AAAABBBB
        where AAAA is the code for the coordinate system (RA--/DEC-, GLON/GLAT)
        and BBBB is the code for the projection (-SIN,-GLS,-TAN).
        Unused characters are replaced with - to specify the codes.
        e.g. ['RA---TAN','DEC--TAN']
        If you do not provide a template header, you must specify this value.
    image_size: int[2]
        The desired pixel size of the output image.
        Equivalent to the NAXISn WCS FITS keyword
        A pair of integers in X,Y order.
        If you do not provide a template header, you must specify this value.
    equinox: float
        Equivalent to the EQUINOX WCS FITS keyword. Defaults to 2000. (i.e. J2000 equinox)
        If you do not provide a template header, you should specify this value.
    is_sigma: bool
        Set to TRUE if the input HEALPix map is a map of the 1-sigma uncertainty.
        In this case, we scale the result by 1/sqrt(surf_heal/surf_wcs)` to obtain the 
        corresponding uncertainty in the WCS pixel.
        WARNING: We assume cdelt is specified in degrees for this operation.
        Default is FALSE.
    ignore_blank: boolean
        Set to TRUE if you want to ignore `BLANK` values in the input HEALPix data.
        If no `BLANK` keyword is defined in the HEALPix FITS metadata, this parameter has
        no effect.
        Default is TRUE.
    blank_value: int
        The BLANK value to use if it is not specified in the HEALPix header.
        Defaults to -32768.
    clobber: boolean
        Set to TRUE if you want to overwrite (aka. clobber) the existing output file
        Default is FALSE.
    col_ids: int[]
        Ids of rows to extract in the HEALPix file
    """
    # --- Call the Healpix2wcs class --- #
    healpix = Healpix2wcs(healpix, field, header, header_hdu, output, crpix, cdelt, pixel_size, crval, ctype,
                          image_size, equinox, is_sigma, ignore_blank, blank_value, clobber, col_ids)
    # --- Call all functions in the class to extract the WCS --- #
    # If the map is in CAR projection and the image size is */1 or 1/*,
    # Create WCS Header and collect information about the HEALPix file
    healpix.find_nb_cols()
    if healpix.create_header_wcs() == 1:
        return 1
    healpix.check_partial()
    healpix.read_healpix_file()
    healpix.determine_blank_value()
    healpix.collect_information_about_healpix()
    # Create and fill data output
    healpix.init_out_data()
    for z in range(healpix.nb_cols):
        healpix.collect_hpx_coordinates()
        healpix.use_intersection_surface(z)
        for x in range(healpix.x_dim):
            healpix.rastherize_healpixels(x, z)
        healpix.write_processing_line()
        healpix.finalize_data_output(z)
    healpix.write_fits_res()
