threedi-raster-edits
==========================================

Introduction

Threedi Raster Edits is used internally at NENS for raster conversion, edits and checks.
Currently it includes the functions as alignment, replace_nodata, alignment checks, property checks and raster conversions to friction, interception and others.

Usage
------------
We can download rasters::

  >>> import threedi_raster_edits as tre
  >>> landuse = tre.UUID.THREEDI_LANDUSE
  >>> vector = tre.Vector(vector_path)
  >>> feature = vector[0]
  >>> rextract = tre.RasterExtraction(lizard_api_key)
  >>> rextract.run("ouput/raster.tif", landuse_uuid, feature.geometry, cellsize=0.5, threads=1)

Raster conversion::

  >>> from threedi_raster_edits import ThreediRasterGroup
  >>> group = ThreediRasterGroup(dem_path, landuse_path=landuse_path, soil_path=soil_path)
  >>> group.load_landuse_conversion_table(csv_landuse_path)
  >>> group.load_soil_conversion_table(csv_soil_path)
  >>> group.generate_friction()
  >>> group.generate_permeability()
  >>> group.generate_interception()
  >>> group.generate_crop_type()
  >>> group.generate_max_infiltration()
  >>> group.generate_infiltration()
  >>> group.generate_hydraulic_conductivity()
  >>> group.friction.write("friction.tif")

Raster checks::

  >>> group = ThreediRasterGroup(dem_path, friction_path="friction.tif")
  >>> align_checks = group.check_alignemnt()
  >>> property_checks = group.check_properties()

Building interception can also be generated::

  >>> from threedi_raster_edits import Vector
  >>> buildings = Vector("buildings.shp")
  >>> group = ThreediRasterGroup(dem_path, buildings=buildings)
  >>> group.generate_building_interception(10)
  >>> group.interception.write("interception.tif")

One can also use the internal raster class for easy raster processing as reproject, clipping, resampling, aligning, reading geometries and creating copies::

  >>> from threedi_raster_edits import Raster
  >>> import numpy as np
  >>> raster = Raster("dem.tif")
  >>> raster.reproject(28992)
  >>> raster.resample(1,1)
  >>> raster.clip(Vector("clip.shp"))
  >>> raster.align(Raster("template.tif"))
  >>> copy = raster.copy(shell=True)
  >>> clip = Vector("clip.shp")
  >>> geometry = clip[0].geometry # geometry of first feature
  >>> clip_values = np.nansum(raster.read(clip))

For more advanced/larger processing you can also use raster loops::

  >>> output = raster.copy(shell=True)
  >>> for tile in raster:
  >>>     array = tile.array
  >>>     array[array==1] = 20
  >>>     output.array = array, tile.location
  >>> output.write("tiles_adding.tif")

Or just do something with the array::

  >>> output = raster.copy(shell=True)
  >>> array = raster.array
  >>> array = array *100
  >>> output.array = array
  >>> output.write("output.tif")


Installation
------------

We can be installed with::

  $ pip install threedi-raster-edits

(TODO: after the first release has been made)


Development installation of this project itself
-----------------------------------------------
GDAL is not automatically installed, hence not available in the requirement,so please install gdal 3.2.0 yourself or use anaconda::

  $ conda create -n threedi_raster_edits python=3 gdal=3.2.0 rtree black pytest

We use python's build-in "virtualenv" to get a nice isolated directory. You
only need to run this once::

  $ python3 -m venv --system-site-packages .

A virtualenv puts its commands in the ``bin`` directory. So ``bin/pip``,
``bin/pytest``, etc. Set up the dependencies like this::

  $ bin/pip install -r requirements.txt

There will be a script you can run like this::

  $ bin/run-threedi-raster-edits

It runs the `main()` function in `threedi-raster-edits/scripts.py`,
adjust that if necessary. The script is configured in `setup.py` (see
`entry_points`).

In order to get nicely formatted python files without having to spend manual
work on it, run the following command periodically::

  $ bin/black threedi_raster_edits

Run the tests regularly. This also checks with pyflakes, black and it reports
coverage. Pure luxury::

  $ bin/pytest

The tests are also run automatically `on "github actions"
<https://githug.com/nens/threedi-raster-edits/actions>`_ for
"master" and for pull requests. So don't just make a branch, but turn it into
a pull request right away:

- Prepend the title with "[WIP]", work in progress. That way you make clear it
  isn't ready yet to be merged.

- **Important**: it is easy to give feedback on pull requests. Little comments
  on the individual lines, for instance. So use it to get early feedback, if
  you think that's useful.

- On your pull request page, you also automatically get the feedback from the
  automated tests.

There's also
`coverage reporting <https://coveralls.io/github/nens/threedi-raster-edits>`_
on coveralls.io (once it has been set up).

If you need a new dependency (like ``requests``), add it in ``setup.py`` in
``install_requires``. Local development tools, like "black", can be added to the
``requirements.txt`` directoy. In both cases, run install again to actuall
install your dependency::

  $ bin/pip install -r requirements.txt


Releasing the project
---------------------

To make a release, first install zest.releaser (globally)::

  $ pip install zest.releaser

Make sure you're on master and that you've updated the changelog. Then release
it with "fullrelease". You can press "enter" at every question::

  $ fullrelease

The github action ought to upload the fresh package to pypi.


Steps to do after generating with cookiecutter
----------------------------------------------

- Add a new project on https://github.com/nens/ with the same name. Set
  visibility to "public" and do not generate a license or readme.

  Note: "public" means "don't put customer data or sample data with real
  persons' addresses on github"!

- Follow the steps you then see (from "git init" to "git push origin master")
  and your code will be online.

- Go to
  https://github.com/nens/threedi-raster-edits/settings/collaboration
  and add the teams with write access (you might have to ask someone with
  admin rights to do it).

- Update this readme. Use `.rst
  <http://www.sphinx-doc.org/en/stable/rest.html>`_ as the format.

- Ask Reinout to configure travis and coveralls.

- Remove this section as you've done it all :-)
