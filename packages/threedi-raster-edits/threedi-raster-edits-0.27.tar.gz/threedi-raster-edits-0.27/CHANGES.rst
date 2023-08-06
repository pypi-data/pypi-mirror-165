Changelog of threedi-raster-edits
===================================================


0.27 (2022-08-29)
-----------------

- Bugfix: For raster tiles everything is not done in memory anymore.
- Cleanup for lizard including dependency installation.
- Updated for postgres upload. Works again.
- Updated blocksize estimation.
- Differences between stacked and adjacent rasters.
- No automatic console logging.


0.26 (2022-07-11)
-----------------

- Geometry field changes of connection nodes.


0.25 (2022-07-08)
-----------------

- Hotfix: removed aggregation_in_space in the v2_aggregation_settings


0.24 (2022-07-08)
-----------------

- Hotfix: requirements.txt


0.23 (2022-07-07)
-----------------

- Added two extra dependencies.


0.22 (2022-07-07)
-----------------

- Removed 3Di results. 
- Removed 3Di scenarios.
- Klondike support.


0.21 (2022-03-22)
-----------------

- Scenarios > 3.8.0


0.20 (2022-03-22)
-----------------

- QGIS changes for raster conversions.
- Include global cache, for storage in a pickle.
- Added easy threedi scenario downloads.

0.19 (2022-02-28)
-----------------

- Increased speed of vector loops
- Added examples in scripts
- Added intuitive progress bars inclusing for gdal


0.18 (2021-11-29)
-----------------

- Changed input for rextract.


0.17 (2021-11-29)
-----------------

- Added threading to lizard rextract
- Also qgis compatible way of showing progress
- Simulations now in queue


0.16 (2021-10-28)
-----------------

- Fixed release error


0.15 (2021-10-28)
-----------------

- More efficient loading of threedirastergroup


0.14 (2021-10-28)
-----------------

- ThreediAPI and ThreediResults are now optional.


0.13 (2021-10-19)
-----------------

- Fixed vector reprojections
- Added inflated rasterloops for rasters
- Added rasterloops for rastergroups
- Added inflated rasterloops for rastergroups
- Added bbox clipping for rasters


0.12 (2021-09-13)
-----------------

- Improved difference algorithm
- Remove geometry fixed at every call, now call once with veotor.fix()
- fid= -1 will result in a fid which is the count


0.11 (2021-09-06)
-----------------

- Token release


0.10 (2021-09-06)
-----------------

- Added sqlite-model support
- Added api support


0.9 (2021-05-06)
----------------

- Changed black format.


0.8 (2021-05-06)
----------------

- Added clips for rasters
- Added custom line string lengths
- Added vector interpolation
- Added (partly) fix threedi rasters


0.7 (2021-03-26)
----------------

- Fixed release process (same for 0.6/0.6).


0.4 (2021-03-26)
----------------

- Fixed release process.
- Fixed tests.
- Added logging.
- Better memory usage of rasters.
- Small changes in vector, geometries.

0.3 (2021-03-25)
----------------

- Automated pypi release.


0.2 (2021-03-12)
----------------

- Changed the syntax of raster class
- Changed the imports to the main script: E.g., from threedi_raster_edits import raster, rastergroup etc.
- Changed the readme.
- Rewritten the geometry structure.


0.1 (2021-03-11)
----------------

- Initial project structure created with cookiecutter and
  https://github.com/nens/cookiecutter-python-template
