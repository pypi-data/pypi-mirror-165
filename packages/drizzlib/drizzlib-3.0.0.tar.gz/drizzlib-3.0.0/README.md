DRIZZLIB
========

Drizzlib is a [HEALPix] to [WCS] FITS conversion python package.

It allows the user to project a subset of the [HEALPix] image into [WCS] FITS format, 
with the field-of-view, projection and pixel size of their choice.

Unlike many common reprojection methods, the drizzling library computes the surface of each pixel intersection
in the input and output maps. This strategy guarantees the photometric accuracy of the transformation and leads to minimal
information loss during the transformation between HEALPix and WCS FITS.

Drizzlib has been tested on python 2.6, 2.7 (drizzlib-1.2.6.3) and 3.5, 3.6 and 3.7 (drizzlib-2.1.2).

MORE INFORMATION
================

[HEALPix]:   http://healpix.jpl.nasa.gov
[WCS]:       http://fits.gsfc.nasa.gov/fits_wcs.html
[drizzling]: http://en.wikipedia.org/wiki/Drizzle_(image_processing)
[pip]:       http://www.pip-installer.org

INSTALLATION: QUICK GUIDE
=========================

Using pip: recommended
----------------------

This is the simplest way to install `drizzlib` if you do not want to modify the code
and simply use it as-is.

    % pip install numpy
    % pip install drizzlib

You need to install `numpy` first because we're linking to some of its C
extensions _during_ the setup of drizzlib.
If you know of a way to avoid this, please tell us how.

From source
-----------

### Where to download the source code

The source files are available :

(1) as a tarball on the CADE homepage, http://cade.irap.omp.eu/dokuwiki/doku.php?id=drizzlib

(2) via git, i.e. git clone https://gitlab.irap.omp.eu/cade/drizzlib-python.git

### Installing dependencies

`drizzlib` requires several python packages (such as `numpy`, `astropy`, and 
`healpy`). These are defined in *requirements.txt* in order to install them with [pip].

### Installation Instructions (User-mode)

You can use a virtual environment or not depending on your needs.

##### Installation with a virtual environment

1. Go to the drizzlib directory

2. Create and activate the virtual environment. The exact command will depend on your installation, but e.g.
 
```
% python3 -m venv /path/to/venv
% source /path/to/venv/bin/activate
```

3. Install the dependencies. 

```
(venv) % pip install -r requirements.txt
```

4. Install drizzlib

```
(venv) % python setup.py install
```

##### Installation without a virtual environment

1. Go to the drizzlib directory

2. Install the dependencies. You can do this as a user or as root.

As user:
```
% pip install --user -r requirements.txt  
```

As root:
```
% pip install -r requirements.txt
```

3. Install drizzlib

As user:
```
% python setup.py install --user
```

As root:
```
% sudo python setup.py install
```

### Installation Instructions (Developer-mode)

You can use pip to install the package and yet keep it editable :

```
pip install --editable .
```


Installation Troubleshooting
----------------------------

- `The following required packages can not be built: freetype, png`
  Older versions of healpy require old matplotlib that requires freetype :
  `sudo apt-get install pkg-config libfreetype*`

- `fatal error: Python.h`
  You need python's development packages, too :
  `sudo apt-get install python-dev`

- `no lapack/blas resources found`
  On Debian-based systems, install the following system packages :
  `sudo apt-get install gfortran libopenblas-dev liblapack-dev`

- `UnicodeEncodeError`
  Make sure the directory in which you uncompressed drizzlib does not contain
  non-ascii characters in its path.


BASIC INSTRUCTIONS FOR RUNNING DRIZZLIB
=======================================

The `doc/TUTORIAL.md` file distributed with the source code contains a more extensive example.

### Running from the python interpreter

``` 
>>> from drizzlib.healpix2wcs import healpix2wcs

# Read `my_healpix.fits`, extract a subset of the data falling within the sky region 
# corresponding to the header of `wcs_config.fits`, and write the result to `my_wcs.fits`.

>>> healpix2wcs('my_healpix.fits', header='wcs_config.fits', output='my_wcs.fits')
```

### Running from the command line

Online help is available with the -h flag, i.e.

```
% healpix2wcs [-h] 
```


The basic syntax is 
```
$ healpix2wcs [-h] [-f] <healpix> <header> <out>
```
positional arguments:
  <healpix>         A HEALPIx FITS file to read from.
  <header>          A FITS file with a WCS header to read configuration from.
  <out>             The filepath of the output FITS file with the data
                    from the healpix file in the region specified by
                    the header file.
                    This file must not exist, or you must specify
                    the -f option to overwrite it.

optional arguments:
  -h, --help        show this help message and exit
  --hdu HEADER_HDU  Id of the HDU (Header Data Unit) to read
                    in the header FITS file. (default: 0)
  -f, --force       Overwrite output if existing (default: do not overwrite)


The simplest possible example:

```
% healpix2wcs my_healpix.fits wcs_config.fits my_wcs.fits
```


HOW TO DISTRIBUTE
=================

Bump the `VERSION`, and then run :

```
$ python setup.py sdist
```

This will create a source distribution tarball in the `dist` directory.
It uses `MANIFEST.in` to exclude files that we want to exclude from distribution.


GUIDELINES
==========

Versioning
----------

We use [semantic versioning](http://semver.org/).

Code formatting
---------------

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Documentation
-------------

Write your documentation in
[Markdown](https://daringfireball.net/projects/markdown/).


CHANGELOG
=========

2.1.2
---
- Call create_wcs_header as a function, not as a variable

2.1.1
---
- Fix bug with the function create_wcs_header

2.1
---
- [healpix2wcs] split in several parts the function
- Add a warning to extract linear map

2.0
---
- new version using python3
- possibility to extract files with several columns

1.2.6.3
-------
- reduce logs in order to fix a bug with large images.

1.2.6.2
-------
- fix bug of inverted crpix1 and crpix2 

1.2.6.1
-------

- fix bug if not car projection

1.2.6
-----
- fix bug in the order of the x,y image size
- add optimization with CAR projection

1.2.5
-----

- add several projections

1.2.4
-----

- Improve partial healpix computation

1.2.3
-----

- minor changes

1.2.2
-----

- Fix bug for the computation of sigma healpix map

1.2.1
-----

- Fix pip dependencies in the setup script.


1.2.0
-----

- Set up python 3 compatibility. (hopefully)
- Add an `is_sigma` parameter for noise maps in `healpix2wcs`.


1.0.1
-----

- Fix the source distribution.


1.0.0
-----

- Initial release of `healpix2wcs`.
- Fix all of the bugs©.


0.5.0
-----

- Basic `wcs2healpix`.


0.4.0
-----

- Add a `healpix2wcs` executable.
- [healpix2wcs] Fix some more bugs.
- [healpix2wcs] Ignore `BLANK` values in input HEALPix.


0.3.0
-----

- Embark a Sutherland-Hodgman clipping algorithm written in C, to optimize further.


0.2.0
-----

- Optimize a lot thanks to the `line_profiler`.


0.1.0
-----

- [healpix2wcs] Initial project skeleton files.
- [healpix2wcs] Non-optimized conversion using `healpy`.


THE SCIENCE
===========

Related Papers
--------------

TODO: @Deborah, reference your paper(s) here.


Healpix
-------

Learn more about the awesome HEALPix pixelation here :
http://healpix.sourceforge.net/


Drizzling
---------

Learn more about [drizzling].

Here are some polygon clipping algorithms:

- We're using: http://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm
- Faster: http://en.wikipedia.org/wiki/Cohen%E2%80%93Sutherland_algorithm
- Even faster : http://en.wikipedia.org/wiki/Liang%E2%80%93Barsky_algorithm


