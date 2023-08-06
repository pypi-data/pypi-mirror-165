"""  
Threedi_raster_edits is a python toolbox for gis and threedi related processing.
Note that the only depedency for base processing should be gdal.

Release info for gdal:
https://github.com/OSGeo/gdal/blob/v3.4.1/gdal/NEWS.md

General imports from threedi_raster_edits are listed below:
    
E.g., from threedi_raster_edits import Raster

-- Use help(Raster) for further information
-- Use .modules for all possible imports of modules
-- Use .classes for all possible imports of classes
-- Use .functions for all possible imports of functions


gis-processing:
    - Raster
    - RasterGroup
    - Vector
    - VectorGroup
    - LineString
    - MultiLineString
    - Polygon
    - MultiPolygon
    - Point 
    - MultiPoint
    
threedi-processing
    - ThreediRasterGroup (used for the rasters of threedi)
    - ThreediEdits (used for the model database (.sqlite) of threedi)
    
threedi-grid (if threedigrid is installed)
    - Grid (simplification of threedigrid)
    
lizard
    - RasterExtraction (used for extraction of rasters from lizard)
    - UUID (Used for predefined UUID's, e.g., UUID.THREEDI_LANDUSE)
            
Philosophy:
    We want to create a simple api on a threedi database.
    Using as few dependencies as possible.
    
"""

from .utils.logging import show_console_logging

show_console_logging()

from .utils.dependencies import DEPENDENCIES

DEPENDENCIES.missing()


from osgeo import gdal, ogr

# options
gdal.SetConfigOption("SQLITE_LIST_ALL_TABLES", "YES")
gdal.SetConfigOption("PG_LIST_ALL_TABLES", "YES")

# Exceptions
gdal.SetConfigOption("CPL_LOG", "NUl")
ogr.UseExceptions()
gdal.UseExceptions()


# utils
from .utils.cache import GlobalCache

# gis
from . import gis
from .gis.raster import Raster
from .gis.rastergroup import RasterGroup
from .gis.vector import Vector
from .gis.vectorgroup import VectorGroup
from .gis.linestring import LineString, MultiLineString
from .gis.polygon import Polygon, MultiPolygon
from .gis.point import Point, MultiPoint
from .gis.geometries import geometry_factory

# Threedi
from . import threedi
from .threedi.rastergroup import ThreediRasterGroup
from .threedi.rastergroup import retrieve_soil_conversion_table
from .threedi.rastergroup import retrieve_landuse_conversion_table
from .threedi.edits import ThreediEdits
from .threedi.tables.templates import Templates

# Lizard
from . import lizard
from .lizard.rextract import RasterExtraction
from .lizard import uuid as UUID

# Logging
from . import utils
from .utils.progress import Progress
from .utils.project import log_time
from .utils.project import Files
from .utils.project import Functions
from .utils.project import Classes
from .utils.project import Modules
from .utils.project import Logger

# Examples
from .examples import get_examples

# structure
files = Files(__file__)
functions = Functions(__name__)
classes = Classes(__name__, local_only=False)
modules = Modules(__name__)

# Pyflakes
Raster
RasterGroup
VectorGroup
Vector
LineString
MultiLineString
Polygon
MultiPolygon
Point
MultiPoint
ThreediRasterGroup
retrieve_soil_conversion_table
retrieve_landuse_conversion_table
RasterExtraction
UUID
ThreediEdits
Progress
Logger
files
log_time
show_console_logging
gis
utils
threedi
lizard
get_examples
geometry_factory
GlobalCache
Templates
