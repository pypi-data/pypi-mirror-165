"""#
Created on Fri Apr 26 16:39:50 2019

@author: chris.kerklaan

Vector wrapper used for GIS programming

Goals:
    1. Provide a better interface for ogr
    2. Provides a table and spatial index which grows and deletes with adding
    and deleting features
    3. Provides basic geoprocessing options: Clipping, dissolving etc.
    4. Provides appropriate fixing of geometries

TODO:
    1. Find out when ogr functions are good to use and when to use our own functions
    2. OGR index logics
    
Bugs:
    1. Multipart2singlepart does not write as single part file shape

Note:
    1. Fids cannot be derived faster then looping
    2. Ogr indices are created when copying the vector

Important Notes on pointers:
    Datasource is your pointer, pointer always needs to be present when
    data is edited in layer
    When a feature is created the feature is the pointer.

    Due to this pointers, gdal ds, layers and features are kept in place,
    hence the classs are not an extension of the object but built on top of them.
    If working with pure ogr, make sure that pointer are available:

        lines = Vector(TEST_DIRECTORY+"lines.shp")
        works:
            layer = lines.layer
            feature=layer[0]
            feature.geometry().Clone()
        does not work:
            layer = lines.layer
            feature.geometry().Clone()

    Also:
        works:
            for geometry in multipartgeometry:
                geometry.GetArea()
        does not work:
            for geometry in multipartgeometry:
                function(geometry)

            def function(geometry):
                geometry.GetArea()

    Functions outside the class can only use ogr-functions
    
Notes on gdal speed-ups
    - Function with 'Get' are the fastest gdal functions
        (GetFeature, GetGeometry) instead of indexing '[]' and .geometry() and .items()
        Use field_indices and feature_items to bypass and increase speed

"""
# First-party imports
import os
import logging
import bisect
import operator
import pathlib
import importlib
import numpy as np

# Third party imports
import osgeo
from osgeo import osr, ogr, gdal

HAS_SCIPY = importlib.util.find_spec("scipy") is not None
if HAS_SCIPY:
    from scipy import spatial

# Third party imports - not obligatory
try:
    import rtree

    HAS_RTREE = True
except ImportError:
    HAS_RTREE = False

# Local imports
from threedi_raster_edits.gis.geometry import (
    POLYGON,
    SINGLE_TYPES,
    SINGLE_TO_MULTIPLE,
    MULTI_TYPES,
    TRANSLATION as GEOMETRY_TRANSLATE,
    fix as fix_geometry,
    clip as clip_geometry,
    difference as difference_geometry,
    dissolve as dissolve_geometry,
)
from threedi_raster_edits.gis.polygon import centerline as centerline_geometry
from threedi_raster_edits.gis.geometries import Polygon
from threedi_raster_edits.gis.geometry import Geometry
from threedi_raster_edits.gis.fields import Fields
from threedi_raster_edits.gis.spatial_reference import SpatialReference
from threedi_raster_edits.gis.feature import Feature
from threedi_raster_edits.utils.project import Classes, Functions
from threedi_raster_edits.utils.progress import Progress

# structure
classes = Classes(__name__, local_only=True)
functions = Functions(__name__)


# Global DRIVERS
DRIVER_GDAL_MEM = gdal.GetDriverByName("MEM")
DRIVER_OGR_MEM = ogr.GetDriverByName("Memory")
DRIVER_OGR_GPKG = ogr.GetDriverByName("GPKG")
DRIVER_OGR_SHAPEFILE = ogr.GetDriverByName("ESRI Shapefile")
DRIVERS_SQL = ["PostgreSQL", "GPKG"]

# Memory counter
_mem_num = 0

# Logger
logger = logging.getLogger(__name__)


class Vector:
    """wrapper of ogr layer, input is ogr datasource, only one layer
    is expected
    """

    instance = "gis.vector.Vector"

    def __init__(
        self,
        path: str = None,
        layer_name=None,
        write=1,
        view=False,
        create_index=False,
        create_table=False,
        name=None,
        epsg=28992,
        ds=False,
        idx=None,
    ):
        self.create_index = create_index
        self.create_table = create_table
        self.layer_name = layer_name
        self.view = view
        self.standard_epsg = epsg
        self.has_rtree = HAS_RTREE

        if ds:
            self.ds = path
            if idx:
                self.idx = idx

        else:
            if not os.path.exists(str(path)) and not "vsimem" in str(path):
                raise FileNotFoundError("Vector not found")

            self.path = pathlib.Path(path)
            self.ext = self.path.suffix
            self.base_path = self.path.with_suffix("")
            if self.ext == ".shp":
                layer_name = self.path.stem
            self.ds = ogr.Open(str(path), write)
            index = import_index(self.base_path)
            if index:
                self.idx = index

        if layer_name:
            self.layer_name = layer_name
            self.layer = self.ds.GetLayer(layer_name)
        else:
            try:
                self.layer = self.ds[0]
                self.layer_name = self.layer.GetName()
            except TypeError:
                raise FileNotFoundError("No layer name, please define")

        if not name:
            name = self.layer_name
        self.name = name

        self.info(self.layer)

        if "vsimem" in str(path):
            logger.debug("loading vector in memory")

    @classmethod
    def from_pg(cls, host, port, user, password, dbname, layer_name, write=0, **kwargs):
        """
        returns a class from a postgres database
        takes a {"host":"x", "port":"x", "password":"x",
                 "user":"x", "host":"x"}
        """
        ogr_pg = ("PG:host={} port={} user='{}'" "password='{}' dbname='{}'").format(
            host, port, user, password, dbname
        )

        return cls(ogr.Open(ogr_pg, write), layer_name, ds=True, **kwargs)

    @classmethod
    def from_ds(cls, ogr_ds: ogr.DataSource = None, **kwargs):
        """returns a class from datasource input"""
        return cls(ogr_ds, ds=True, **kwargs)

    @classmethod
    def from_mem_path(cls, path: str = None, **kwargs):
        """returns a class from a memory path"""
        return cls(ogr.Open(path), ds=True, **kwargs)

    @classmethod
    def from_scratch(cls, layer_name: str, geometry_type: int, epsg: int, **kwargs):
        """Creates a layer from scratch
        Params:
            layer_name: name of the layer (str)
            geometry_type: 1 = point, 2 = linestring, 3 = polygon (int)
            epsg: spatial reference code (int)
        """
        ds, _ = mem_layer(layer_name, geometry_type=geometry_type, epsg=epsg)
        return cls(ds, layer_name, ds=True, **kwargs)

    def info(self, layer, **kwargs):
        """Returns info of an ogr layer(s)"""

        if layer:
            self.layer = layer
            self.original_count = self.count
        else:
            raise ValueError("Layer is None, check filename?")

        if len(kwargs) > 0:
            for key, value in kwargs.items():
                setattr(self, key, value)

        self.quiet = False
        settings = self.settings
        if not settings["view"]:
            if settings["create_index"]:
                self.set_index()

            if settings["create_table"]:
                self.set_table()

    def get_feature(self, fid=None, feature=None):
        """helper for retrieving features"""
        if fid is not None:
            return Feature(self.layer.GetFeature(fid), self.layer)
        if feature:
            return Feature(feature, self.layer)

    def __iter__(self):
        self.reset()
        for i in self.layer:
            yield self.get_feature(feature=i)

    def __getitem__(self, i):
        return self.get_feature(i)

    def __len__(self):
        return len(self.layer)

    def __setitem__(self, key, value):
        if key == "feature":
            self.set_feature(value)

    def __repr__(self):
        settings = self.settings
        settings["count"] = self.count
        return f"({self.instance}) {self.name}: {settings}"

    def __next__(self):
        return self.get_feature(feature=self.layer.GetNextFeature())

    @property
    def filepath(self):
        if hasattr(self, "path"):
            if os.path.exists(str(self.path)):
                return str(self.path)
        return None

    @property
    def filename(self):
        if hasattr(self, "base_path") and "vsimem" not in str(self.base_path):
            return str(self.base_path)
        return ""

    @property
    def drivers(self):
        if not hasattr(self, "_drivers"):
            self._drivers = driver_extension_mapping()
        return self._drivers

    @property
    def layers(self):
        return [layer.GetName() for layer in self.ds]

    @property
    def extent(self):
        return self.layer.GetExtent()

    @property
    def count(self):
        self.reset()
        return self.layer.GetFeatureCount()

    @property
    def fields(self):
        return Fields(self.layer)

    @property
    def keys(self):
        if not hasattr(self, "_keys"):
            self._keys = self.fields.keys
        return self._keys

    @property
    def field_indices(self):
        if not hasattr(self, "_field_indices"):
            self._field_indices = self.fields.indices
        return self._field_indices

    @property
    def layer_defn(self):
        return self.layer.GetLayerDefn()

    @property
    def geometry(self):
        return self[0].geometry

    @property
    def geometry_type(self):
        return self.layer.GetGeomType()

    @property
    def geometry_name(self):
        return ogr.GeometryTypeToName(self.geometry_type)

    @property
    def fids(self):
        return [x.GetFID() for x in self.layer]

    @property
    def fid_column(self):
        column = self.layer.GetFIDColumn()
        if column == "":
            return "id"
        return self.layer.GetFIDColumn()

    @property
    def driver(self):
        return self.ds.GetDriver().name

    @property
    def spatial_reference(self):
        sr = self.layer.GetSpatialRef()
        if not sr:
            return SpatialReference.from_epsg(self.standard_epsg)
        else:
            return SpatialReference.from_sr(sr)

    @property
    def epsg(self):
        return self.spatial_reference.epsg

    @property
    def extent_geometry(self):
        x1, x2, y1, y2 = self.layer.GetExtent()
        wkt = POLYGON.format(x1=x1, x2=x2, y1=y1, y2=y2)
        return Polygon(ogr.CreateGeometryFromWkt(wkt))

    @property
    def extent_vector(self):
        vector = Vector.from_scratch("extent", 3, self.epsg)
        vector.add(geometry=self.extent_geometry)
        return vector

    @property
    def extent_area(self):
        return self.extent_geometry.GetArea()

    @property
    def settings(self):
        return {
            "create_index": self.create_index,
            "create_table": self.create_table,
            "view": self.view,
            "layer_name": self.layer_name,
            "epsg": self.epsg,
            "name": self.name,
        }

    @property
    def as_gdal_dataset(self):
        """gdal and ogr not always compatible, we have to use openex"""
        mem_ds = mem_path() + ".shp"
        self.write(mem_ds, index=False)
        return gdal.OpenEx(mem_ds)

    @property
    def table(self):
        self.set_table()
        return self._table

    @property
    def index(self):
        if self.has_rtree:
            self.set_index()
            return self.idx
        else:
            return None

    @property
    def has_ogr_index(self):
        return self.layer.TestCapability("FastSpatialFilter")

    @property
    def has_geometry(self):
        return self.geometry_type != 100

    def reset(self):
        self.layer.ResetReading()

    def add_field(self, name, ogr_type):
        self.fields.add(name, ogr_type)

        if hasattr(self, "_table"):
            self.table[name] = [None for table in self.table["fid"]]

        if hasattr(self, "_keys"):
            del self._keys
        if hasattr(self, "_field_indices"):
            del self._field_indices

    def delete_field(self, *field_names):
        for field_name in field_names:
            self.fields.delete(field_name)

    def add(
        self,
        feature=None,
        geometry=None,
        fid=-1,
        skip_irrelevant_items=True,
        fid_latest=False,
        fid_count=False,
        **items,
    ):
        # unpack feature
        if isinstance(feature, Feature):
            geometry = feature.geometry
            items = feature.items

        # pick up items from kwargs
        attr = {}
        if "items" in items:
            attr = items["items"]
            del items["items"]
        attr.update(items)
        items = attr

        # account for none attributes
        if skip_irrelevant_items:
            if len(items) != 0:
                irrelevant = [k for k in items.keys() if k not in self.keys]
                for key in irrelevant:
                    del items[key]

        # convert geometry if needed
        if geometry:
            geometry = ogr_geometry(geometry)

        self.layer, fid = add_feature(
            self.layer,
            self.layer_defn,
            geometry,
            items,
            fid,
            fid_latest,
            fid_count,
        )

        if hasattr(self, "idx"):
            self.add_index_feature(self.layer.GetFeature(fid))

        if hasattr(self, "_table"):
            self.add_table_feature(self.layer.GetFeature(fid))

        return fid

    def delete(self, feature):
        """deletes by using feature ids
        Input can be a single feature id or of type Feature class
        """

        if type(feature) == int:
            feature = self[feature]

        feature = ogr_feature(feature)

        if self.driver == "PostgreSQL":
            self.layer.ResetReading()
            self.ds.StartTransaction()

        if hasattr(self, "idx"):
            self.delete_index_feature(feature)

        if hasattr(self, "_table"):
            self.delete_table_feature(feature)

        self.layer.DeleteFeature(feature.GetFID())

        if self.driver == "PostgreSQL":
            self.ds.CommitTransaction()

    def delete_all(self):
        self.reset()
        for feature in self:
            self.delete(feature)

        # actually deletes the features
        self.layer.SyncToDisk()
        self.ds.FlushCache()

        self.layer = None
        self.layer = self.ds.GetLayer(self.layer_name)

    def set_feature(self, feature):
        self.layer.SetFeature(ogr_feature(feature))

    def copy(
        self,
        geometry_type=None,
        shell=False,
        fields=True,
        index=True,
        table=True,
        driver="Memory",
    ):
        """In memory ogr object, with features
        params:
            geometry_type: change the geometry type
            shell: Does not add the features
            fields: Set to True is fields have to be included
        """

        if type(geometry_type) == str:
            geometry_type = GEOMETRY_TRANSLATE[geometry_type]

        if not geometry_type:
            geometry_type = self.geometry_type

        ds, layer, path = mem_layer(
            self.layer_name,
            self.layer,
            geometry_type=geometry_type,
            shell=shell,
            fields=fields,
            sr=self.spatial_reference,
            return_path=True,
            driver=driver,
        )

        self.path = path
        settings = self.settings
        if index == False:
            settings["create_index"] = False

        if table == False:
            settings["create_table"] = False

        # This is the same c++ point, please copy the idx somehow
        # if hasattr(self,"idx") and shell==False:
        #    settings["idx"] = self.idx

        return Vector.from_ds(ds, **settings)

    def write(self, path, index=False, overwrite=False):
        """write is done by creating a new file and copying features"""
        path = str(path)  # pathlib

        driver = self.identify_driver(path)
        driver_name = driver.name

        # check shapefile length, raise an error if incorrect
        self.check_driver_field_length(driver, raise_error=True)

        if overwrite:
            if os.path.exists(path):
                driver.DeleteDataSource(path)

        # create output file
        out_ds = driver.CreateDataSource(path)
        out_layer = out_ds.CreateLayer(
            self.layer_name, self.spatial_reference, self.geometry_type
        )

        # add fields
        for i in range(self.layer_defn.GetFieldCount()):
            out_layer.CreateField(self.layer_defn.GetFieldDefn(i))

        # use out layer definition
        layer_defn = out_layer.GetLayerDefn()

        # if uploading to sql based drivers, we have to commit once in a while
        sql = driver_name in DRIVERS_SQL
        if sql:
            out_layer.StartTransaction()

        for i, feature in enumerate(self):

            add_feature(
                out_layer,
                layer_defn,
                ogr_geometry(feature.geometry),
                feature.items,
            )
            if sql and (i % 1500 == 0):  # commit once every 1500 features
                out_layer.CommitTransaction()
                out_layer.StartTransaction()

        if sql:
            out_layer.CommitTransaction()

        out_layer = None
        out_ds.Destroy()

        if index:
            create_index_streamed(self.layer, str(pathlib.Path(path).with_suffix("")))

    def close(self):
        self.layer = None
        self.ds.Destroy()

    """tables and index"""

    def set_ogr_index(self):
        """Set the ogr index based on the driver
        Note that gpkg drivers seem to have spatial filter automatically
        """
        if self.has_ogr_index:
            return

        if self.driver == "ESRI Shapefile":
            sql = [
                f"CREATE SPATIAL INDEX ON {self.layer_name}",
                f"REPACK {self.layer_name}",
                f"RECOMPUTE EXTENT ON {self.layer_name}",
            ]
            for s in sql:
                self.ds.ExecuteSQL(s)

    def set_index(self, reset=False):
        """sets the rtree index and ogr idex if not exist"""
        if not hasattr(self, "idx") and self.has_rtree:
            self.create_index = True
            self.update_index = True
            self.idx = create_index_streamed(self.layer, self.filename)

        if reset:
            self.idx = create_index_streamed(self.layer, self.filename)

        self.set_ogr_index()

    def add_index_feature(self, feature):
        """adds a feature to the index"""
        ogr_feat = ogr_feature(feature)

        # if multiple geometry fields are present
        geometry = ogr_feat.geometry()
        if geometry == None:
            geometry = ogr_feat.GetGeomFieldRef(1)

        self.idx.insert(ogr_feat.GetFID(), geometry.GetEnvelope())

    def delete_index_feature(self, feature):
        """deletes a feature in the index the index"""

        ogr_feat = ogr_feature(feature)

        geometry = ogr_feat.geometry()
        if geometry == None:
            geometry = ogr_feat.GetGeomFieldRef(1)

        self.idx.delete(ogr_feat.GetFID(), geometry.GetEnvelope())

    def write_index(self, path, quiet=True):
        """writes an index to the path"""
        create_index_streamed(self.layer, path)

    def set_table(self):
        """sets the table if not exists"""
        if not hasattr(self, "_table"):
            self.create_table = True
            self.update_table = True
            self.table_fields = self.fields.names + ["fid"]
            self._table = {field: [] for field in self.table_fields}
            self.layer.ResetReading()
            for feature in self.layer:
                self.add_table_feature(feature)

    def add_table_feature(self, feature: ogr.Feature):
        """updates the table using an ogr feature"""
        if not feature:
            return

        feature = ogr_feature(feature)
        for i, key in enumerate(self.keys):
            self._table[key].append(feature.GetField(i))

        self._table["fid"].append(feature.GetFID())

    def delete_table_feature(self, feature: ogr.Feature):
        """delete a feature in the table"""
        feature = ogr_feature(feature)
        idx = self._table["fid"].index(feature.GetFID())
        for key in self._table.keys():
            del self._table[key][idx]

    """spatial and table filters"""

    def spatial_filter(
        self,
        geometry,
        method="Intersect",
        use_ogr=True,
        return_fid=False,
        return_vector=False,
        return_feature=True,
        quiet=True,
    ):
        """Takes a geometry or vector and returns fids based on method
        params:
            geometry: ogr.Geometry or Vector class
            method: 'Intersect' or 'Within' or 'Extent'
            filter: Setting a spatial filter on the layer
            use_ogr: True or False
            return_fid: Return the feature id
            return_vector: Returns a vector object
            return_feature: Returns a feature.
            quiet: verbosity

        Note on ogr/rtree. Somehow ogr shows a more accurate spatial filter
        at on tiles. Rtree is, I think, better on polygons.

        """

        if hasattr(geometry, "ds"):
            return self.spatial_filter_vector(geometry, method, use_ogr, quiet)

        if not (isinstance(geometry, Geometry) or isinstance(geometry, ogr.Geometry)):
            raise ValueError(
                f"{type(geometry)}, must be an ogr or gis.geometry or vector"
            )

        fids = self._sfilter(geometry, method, use_ogr, quiet)
        if return_fid:
            return fids
        elif return_vector:
            return self.vector_from_fids(fids)
        elif return_feature:
            return [self.get_feature(i) for i in fids]

    def _sfilter(self, geometry, method="Intersect", use_ogr=True, quiet=True):
        """returns spatially filtered fids, depending on the method
        params:
            geometry: ogr.geometry
            method: 'Intersect' or 'Within' or 'Extent'
            use_ogr: uses ogr set spatial filter
            quiet: verbose or not
        """

        if use_ogr:
            index = None
        else:
            index = self.index

        # do a fast pass over general geometries using ogr or rtree
        generator = spatial_filter_generator(self.layer, geometry, index)

        output = []
        for loop, feature in enumerate(generator):
            feature_geometry = feature.GetGeometryRef()
            if method == "Intersect":
                add = feature_geometry.Intersects(geometry)
            elif method == "Within":
                add = feature_geometry.Within(geometry)
            elif method == "Extent":
                add = feature
            else:
                logger.info("please select either 'Within' or 'Intersect'")
                raise ValueError(
                    "Incorrect method choose between: 'Within, Intersect or Extent'"
                )

            if loop % 100000 == 0 and loop > 0:
                print(f"Doing Spatial filter at feature {loop}")

            if add:
                output.append(feature.GetFID())

        return output

    def set_spatial_filter(self, geometry):
        self.layer.SetSpatialFilter(geometry)
        self.info(self.layer)

    def spatial_filter_vector(self, vector, method, use_ogr, quiet=True):
        output = self.copy(shell=True)
        for feature in Progress(vector, f"{method} filter", quiet):
            for part in self.spatial_filter(feature.geometry, method, use_ogr):
                output.add(part)
        return output

    def clusters(self):
        """returns all spatially intersecting features"""
        return spatial_clusters(self.layer)

    def set_attribute_filter(self, key, value=None):
        if key is None:
            self.layer.SetAttributeFilter(None)
            return
        self.layer.SetAttributeFilter(f"{key} = {value}")

    def filter(self, return_fid=False, return_vector=False, **filtering):
        """Params:
            fid_only: returns the fid only
            filtering: Can be a dictionary e.g.,:**{
                                        field1:field_value1
                                            }
                       Or filled in as argument e.g.,:
                           percentile=1,
                           klasse=100
        returns a list
        """
        self.set_table()

        # get first field
        for field_key, field_value in filtering.items():
            break

        if len(self.table) == 0:
            return []

        table_fids = self.table["fid"]
        loop_fids = table_fids
        for i, (field_key, field_value) in enumerate(filtering.items()):

            if i == 0:
                loop_table_values = self.table[field_key]
            else:
                table_values = self.table[field_key]
                loop_table_values = [
                    lookup_ordered(fid, table_fids, table_values) for fid in loop_fids
                ]

            loop_fids = lookup_unordered(field_value, loop_table_values, loop_fids)
        fids = set(loop_fids)

        if return_fid == True:
            return list(fids)
        elif return_vector == True:
            return self.vector_from_fids(fids)
        else:
            return [self.get_feature(i) for i in fids]

    def vector_from_fids(self, fids):
        """fastest way to retrieve fids is via attribute filter
        Exceptions are returned when fid is single, due to '(fid,)' comma
        Also when there are more fids that +- 4000 it'll return an error
        Then a normal copy is done, which is a lot slower.
        """
        if len(fids) == 0:
            return self.copy(shell=True)

        try:
            self.layer.SetAttributeFilter("FID IN {}".format(tuple(fids)))
            out = self.copy()
            self.layer.SetAttributeFilter(None)
        except Exception:
            out = self.copy(shell=True)

            for fid in fids:
                out.add(self.get_feature(fid))
        return out

    def identify_driver(self, path):
        name = self.drivers[os.path.splitext(path)[1]]
        return ogr.GetDriverByName(name)

    def check_driver_field_length(self, driver, raise_error=True):
        """
        Check if field names have a the correct length,
        raises an error otherwise
        """
        if driver.GetName() == "ESRI Shapefile":
            for field_name in self.fields.names:
                if len(field_name) > 10:
                    if raise_error:
                        raise ValueError(
                            f"""
                            Fieldname '{field_name}' over 10 length.
                            Write as gpkg or short field names.
                            
                            """
                        )

    def rasterize(
        self,
        rows=None,
        columns=None,
        geotransform=None,
        resolution=None,
        nodata=-9999,
        field=None,
        extent=None,
        all_touches=False,
        options=None,
        return_ds=True,
        data_type=gdal.GDT_Float32,
    ):
        """Rasterizes the vector as a boolean,
        If field or all touches is given that is used
        """

        if not columns and not rows:
            if not resolution:
                logger.error("please provide resolution")
                return
            if not extent:
                extent = self.extent
            x1, x2, y1, y2 = extent
            columns = int((x2 - x1) / resolution)
            rows = int((y2 - y1) / resolution)
            geotransform = (x1, resolution, 0, y2, 0, -resolution)

        if data_type == float:
            data_type = gdal.GDT_Float32
        elif data_type == int:
            data_type = gdal.GDT_Int32

        return rasterize(
            self.layer,
            rows,
            columns,
            geotransform,
            self.spatial_reference.wkt,
            nodata,
            field,
            all_touches,
            options,
            return_ds,
            data_type,
        )

    def interpolate(
        self,
        field,
        resolution,
        algorithm="invdist",
        nodata_value=-9999,
        quiet=True,
        **arguments,
    ):
        """
        Returns a gdal datasource.  Can be loaded with Raster.

        Interpolates vector points using gdal grid
        https://gdal.org/programs/gdal_grid.html#interpolation-algorithms


        params:
            field: Fields of which is used to interpolate
            resolution: Resulution of the final raster
            algorithm: See the above link to see how it can be filled.
            argument: See the above link to how it can be filled.

        """
        logger.debug("vector - interpolate - Start")
        progress = Progress(total=100, message="GDALGrid Interpolate", quiet=quiet)
        argument = ""
        for k, v in arguments.items():
            argument = argument + f"{k}={v}:"

        if len(argument) == 0:
            raise ValueError(
                "Please fill in an arguments, look at (https://gdal.org/programs/gdal_grid.html#interpolation-algorithms)"
            )

        assert field in self.fields

        extent = self.extent
        width = int((extent[1] - extent[0]) / resolution)
        height = int((extent[3] - extent[2]) / resolution)
        grid_options = gdal.GridOptions(
            zfield=field,
            algorithm=f"{algorithm}:{argument}",
            width=width,
            height=height,
            callback=progress.gdal,
        )

        path = mem_path()
        ds = gdal.Grid(
            destName=path,
            srcDS=self.as_gdal_dataset,
            options=grid_options,
        )

        # The raster which is extracted from the gdalGrid is acutally upside
        # down with epsg 28992.
        # So we have to flip the array and change the geotransform.

        # We will now reverse it to the left upper corner.
        transform = list(ds.GetGeoTransform())
        transform[3] = transform[3] + (height * resolution)
        transform[-1] = -transform[-1]
        ds.SetGeoTransform(tuple(transform))

        band = ds.GetRasterBand(1)
        array = band.ReadAsArray()
        band.WriteArray(np.flip(array, 0), 0, 0)

        # set nodata value
        band.SetNoDataValue(-9999)

        band = None
        ds = None

        return gdal.Open(path)

    def pgupload(
        self,
        host,
        port,
        user,
        password,
        dbname,
        layer_name,
        schema="public",
        overwrite="yes",
        spatial_index="GIST",
        fid_column="ogc_fid",
        geometry_name="the_geom",
        force_multi=True,
        quiet=True,
    ):
        ogr_pg = ("PG:host={} port={} user='{}'" "password='{}' dbname='{}'").format(
            host, port, user, password, dbname
        )
        upload(
            ogr.Open(ogr_pg),
            self.layer,
            layer_name,
            schema,
            overwrite,
            spatial_index,
            fid_column,
            geometry_name,
            force_multi,
            quiet,
        )

    def fix(self, geometry_type=None, quiet=True):
        """
        Fixes the geometries of a layer.
        Invalid geometries but also 3D features will be
        set to the layers' geometry type.
        params:
            geometry_type: Sets the target geometry type
            quiet: Shows the progress

        """
        return Vector.from_ds(fix(self.layer, geometry_type, quiet))

    def clip(
        self,
        vector=None,
        geometry=None,
        quiet=True,
        use_ogr=False,
        to_multi=False,
        skip_failures=False,
    ):
        """
        Clip off areas that are not covered by the input vector.
        params:
            quiet: Shows the progress
            use_ogr: uses the ogr variant of this function
        """
        if geometry:
            vector = Vector.from_scratch("", 3, geometry.epsg)
            vector.add(geometry=geometry)

        if use_ogr:
            ds = ogr_clip(self.layer, vector.layer, to_multi, skip_failures, quiet)
        else:
            ds = clip(self.layer, vector.layer, quiet, vector.index)
        return Vector.from_ds(ds)

    def symmetrical_difference(
        self,
        vector,
        quiet=True,
        ignore_errors=False,
        to_multi=False,
        skip_failures=False,
    ):
        ds = sym_difference_ogr(self.layer, vector.layer, to_multi, skip_failures)
        return Vector.from_ds(ds)

    def difference(
        self, vector, quiet=True, use_ogr=False, to_multi=False, ignore_errors=False
    ):
        if use_ogr:
            ds = difference_ogr(
                self.layer, vector.layer, quiet, to_multi, ignore_errors
            )
        else:
            ds = difference(
                self.layer, vector.layer, quiet, vector.index, ignore_errors
            )
        return Vector.from_ds(ds)

    def dissolve(self, field=None, intersecting=True, quiet=True):
        """
        Dissolves features in a layer based on either a field,
        intersecting features, or all.
        params:
            field: None, if set to the field name, dissolves on this field
            intersecting: True, if intersects spatially, dissolves.
            quiet: if True, shows progress of function
        """
        if self.geometry_type != 3:
            intersecting = False

        return Vector.from_ds(
            dissolve(self.layer, field, intersecting, self.index, quiet)
        )

    def union(
        self,
        vector,
        quiet=True,
        to_multi=False,
        skip_failures=False,
        keep_lower_dimensions=True,
    ):
        ds = union_ogr(
            self.layer,
            vector.layer,
            quiet,
            to_multi,
            skip_failures,
            keep_lower_dimensions,
        )
        return Vector.from_ds(ds)

    def buffer(self, buffer_size, layer=None, quiet=True):
        return Vector.from_ds(buffer(self.layer, buffer_size, quiet))

    def to_single(self, quiet=True):
        return Vector.from_ds(multiparts_to_singleparts(self.layer, quiet))

    def centroid(self, layer=None, quiet=True):
        return Vector.from_ds(centroid(self.layer, quiet))

    def reproject(self, epsg, quiet=True):
        return Vector.from_ds(reproject(self.layer, epsg, quiet))

    def polygon_to_lines(self, quiet=True):
        return Vector.from_ds(polygon_to_lines(self.layer, quiet))

    def simplify(self, factor, quiet=True):
        return Vector.from_ds(simplify(self.layer, factor, quiet))

    def vonoroi(self, buffer=1):
        return Vector.from_ds(vonoroi(self.layer, buffer))

    def centerlines(self, resolution=0.5, quiet=True):
        return Vector.from_ds(centerlines(self.layer, resolution, quiet))


def ogr_feature(feature):
    """Translates a Feature to an ogr_feature"""
    try:
        feature = feature.ptr
    except Exception:
        pass
    return feature


def ogr_geometry(geometry):
    if hasattr(geometry, "ogr"):
        geometry = geometry.ogr
    return geometry


def lookup_unordered(value, table, lookup_table):
    """fastest way to lookup a value by using an index in a unordered list
    Looping over a list only once
    returns a list of matching values
    """

    values = []

    if value not in table:
        return values

    index = 0

    # last index of value in table
    end = len(table) - operator.indexOf(reversed(table), value) - 1

    # when the first value is the only one
    if end == 0:
        return [lookup_table[0]]

    while index <= end:
        index = table.index(value, index)
        values.append(lookup_table[index])
        index += 1

    return values


def lookup_ordered(value, table, lookup_table):
    """fastest way to returns a lookup table value for an ordered list given,
    using bisect
    table must be ordered
    if not unique only the first index is returned
    """
    return lookup_table[bisect.bisect_left(table, value)]


def mem_path(extension=None):
    """Generates a new vsimem path with or without an extension"""
    global _mem_num
    location = f"/vsimem/mem{_mem_num}"
    _mem_num += 1
    if extension is not None:
        location = location + "." + extension
    return location


def mem_ds(driver_name="Memory"):
    """creates a new ogr datasource base on a driver name"""
    driver = ogr.GetDriverByName(driver_name)
    meta = driver.GetMetadata()
    extension = meta.get("DMD_EXTENSION")
    location = mem_path(extension)
    ds = driver.CreateDataSource(location)
    return ds, location


def mem_layer(
    layer_name: str,
    layer: ogr.Layer = None,
    geometry_type: int = None,
    epsg: int = None,
    sr: osr.SpatialReference = None,
    shell: bool = True,
    fields: bool = True,
    options: list = ["SPATIAL_INDEX=YES"],
    return_path: bool = False,
    driver="Memory",
):
    """
    Standard creates a 'shell' of another layer,
    To create a new memory layer,
    or to create a memory copy of a layer
    params:
        epsg/sr: one can choose between epsg/sr
        shell: if True, returns a shell with no  feature
        field: if False, returns a shell without the fields
    returns:
        ds : ogr.Datasource
    """
    ds, path = mem_ds(driver)

    if not shell and layer is not None:
        new_layer = ds.CopyLayer(layer, layer_name)
        if return_path:
            return ds, new_layer, path
        else:
            return ds, new_layer

    if epsg:
        sr = SpatialReference.from_epsg(epsg)
    elif sr == None:
        sr = layer.GetSpatialRef()

    if not geometry_type and layer:
        geometry_type = layer.GetGeomType()

    new_layer = ds.CreateLayer(layer_name, sr, geometry_type, options)

    if fields and layer:
        layer_defn = layer.GetLayerDefn()
        for i in range(layer_defn.GetFieldCount()):
            new_layer.CreateField(layer_defn.GetFieldDefn(i))

    if return_path:
        return ds, new_layer, path
    else:
        return ds, new_layer


def index_generator(layer):
    layer.ResetReading()
    for i, feature in enumerate(layer):
        if feature:
            geometry = feature.GetGeometryRef()
            if not geometry:
                geometry = feature.GetGeomFieldRef(1)
            if not geometry:
                continue
            xmin, xmax, ymin, ymax = geometry.GetEnvelope()
            yield (i, (xmin, xmax, ymin, ymax), None)


def create_index_streamed(layer, path=""):
    if layer.GetFeatureCount() == 0:
        return rtree.index.Index("")
    else:
        properties = rtree.index.Property()
        generator = index_generator(layer)
        index = rtree.index.Index(
            path, generator, interleaved=False, properties=properties
        )

    if path != "":
        index.close()
        index = rtree.index.Index(path)

    layer.ResetReading()
    return index


def import_index(base_path):
    """Imports index if valid and larger than 0, else returns None"""
    if os.path.exists(str(base_path) + ".idx") and HAS_RTREE:
        try:
            index = rtree.index.Index(str(base_path))
        except Exception:
            logger.debug("Found invalid index")
            print("Invalid index, not loaded")

        if index.get_size() == 0:
            return None

        return index

    return None


def add_feature(
    layer,
    layer_defn,
    geometry,
    attributes,
    fid=-1,
    fid_latest=False,
    fid_count=False,
):
    """Append geometry and attributes as new feature, starting at 0

    for fid=-1 there are three options:
        1. fid is similar to the current count: exisiting fids = [1,4,10], new fid  = 3
        2. fid is 'next number in line': exisiting fids = [1,10], new fid  = 2
        3. fid continues at the latest number: exisiting fids = [1,10], new fid = 11

    standard is number 2, number 3 takes the most time

    """
    feature = ogr.Feature(layer_defn)

    if fid == -1:
        if fid_latest:
            for i in layer:
                pass
            feature.SetFID(i.GetFID() + 1)
        elif fid_count:
            feature.SetFID(layer.GetFeatureCount())
        else:
            feature.SetFID(-1)
    else:
        feature.SetFID(fid)

    if geometry != None:
        feature.SetGeometryDirectly(geometry.Clone())

    for key, value in attributes.items():
        try:
            feature.SetField(key, value)
        except Exception as e:
            raise ValueError("error:", e, "key", key, "value", value)

    try:
        layer.CreateFeature(feature)
    except RuntimeError as e:
        raise RuntimeError("error:", e, "geom:", geometry, "attributes:", attributes)
    finally:
        fid = feature.GetFID()
        feature.Destroy()

    return layer, fid


def rasterize(
    layer,
    rows,
    columns,
    geotransform,
    spatial_reference_wkt,
    nodata=-9999,
    field=None,
    all_touches=False,
    options=None,
    return_ds=False,
    data_type=gdal.GDT_Float32,
):
    target_ds = DRIVER_GDAL_MEM.Create("", columns, rows, 1, data_type)

    # set nodata
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(nodata)
    band.Fill(nodata)
    band.FlushCache()

    # set metadata
    target_ds.SetProjection(spatial_reference_wkt)
    target_ds.SetGeoTransform(geotransform)

    # set options
    gdal_options = []

    if field:
        logger.info(field)
        gdal_options.append(f"ATTRIBUTE={field}")

    if all_touches:
        gdal_options.append("ALL_TOUCHES=TRUE")

    if options:
        gdal_options.extend(options)

    if len(gdal_options) == 0:
        gdal.RasterizeLayer(target_ds, (1,), layer, burn_values=(1,))
    else:
        gdal.RasterizeLayer(target_ds, [1], layer, options=gdal_options)

    if return_ds:
        return target_ds
    else:
        array = target_ds.ReadAsArray()
        target_ds = None
        return array


def fix(in_layer: ogr.Layer, geometry_type=None, quiet: bool = True):
    """fixes geometries by buffering etc"""

    if not geometry_type:
        geometry_type = in_layer.GetGeomType()

    out_datasource, out_layer = mem_layer("fixes", in_layer, geometry_type)
    out_layer_defn = out_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    in_layer.ResetReading()
    for out_feature in Progress(in_layer, "Geometry fixes", quiet):
        clone = out_feature.GetGeometryRef().Clone()
        geometry = fix_geometry(clone, geometry_type)
        if not geometry:
            logger.info("Found invalid geometry, skipping")
            continue

        items = feature_items(out_feature, indices)
        add_feature(out_layer, out_layer_defn, geometry, items)

    out_layer = None
    return out_datasource


def buffer(in_layer: ogr.Layer, buffer_size: float, quiet: bool = True):
    """Buffers a layer, output is always a polygon"""
    out_datasource, out_layer = mem_layer("buffer", in_layer, ogr.wkbPolygon)
    out_layer_defn = out_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    in_layer.ResetReading()
    for out_feature in Progress(in_layer, "Buffer", quiet):
        geometry = out_feature.GetGeometryRef()
        buffered_geometry = geometry.Buffer(buffer_size)
        items = feature_items(out_feature, indices)
        add_feature(out_layer, out_layer_defn, buffered_geometry, items)

    out_layer = None
    return out_datasource


def centroid(in_layer: ogr.Layer, quiet: bool = True):
    """Takes a ogr layer and returns a centroid ogr layer"""
    out_datasource, out_layer = mem_layer("centroid", in_layer, ogr.wkbPoint)
    out_layer_defn = out_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    in_layer.ResetReading()
    for out_feat in Progress(in_layer, "Centroid", quiet):
        out_geom = out_feat.GetGeometryRef().Centroid()
        items = feature_items(out_feat, indices)
        add_feature(out_layer, out_layer_defn, out_geom, items)

    out_layer = None
    return out_datasource


def simplify(in_layer: ogr.Layer, simple_factor: float, quiet: bool = True):
    """Takes a layer and simplifies all geometryies, return ogr ds"""
    out_datasource, out_layer = mem_layer("simplify", in_layer)
    out_layer_defn = out_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    in_layer.ResetReading()
    for out_feature in Progress(in_layer, "Simplify", quiet):
        out_geometry = out_feature.GetGeometryRef().Simplify(simple_factor)
        items = feature_items(out_feature, indices)
        add_feature(out_layer, out_layer_defn, out_geometry, items)

    out_layer = None
    return out_datasource


def multiparts_to_singleparts(in_layer: ogr.Layer, quiet=True):
    """converts multiparts to single parts"""
    geom_type = SINGLE_TYPES[in_layer.GetGeomType()]
    out_datasource, out_layer = mem_layer("multi2single", in_layer, geom_type)
    out_layer_defn = out_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    in_layer.ResetReading()
    for feature in Progress(in_layer, "Multi2single", quiet):
        items = feature_items(feature, indices)
        geometry = feature.GetGeometryRef()
        if "MULTI" in geometry.GetGeometryName():
            for geometry_part in geometry:
                add_feature(
                    out_layer,
                    out_layer_defn,
                    geometry_part,
                    items,
                )
        else:
            add_feature(
                out_layer,
                out_layer_defn,
                geometry,
                items,
            )
    out_layer = None
    return out_datasource


def reproject(in_layer: ogr.Layer, epsg: int, quiet=True):
    """Takes an ogr layer, reprojects and returns an ogr datasource"""
    in_spatial_ref = in_layer.GetSpatialRef()
    spatial_ref_out = osr.SpatialReference()
    spatial_ref_out.ImportFromEPSG(int(epsg))

    if int(osgeo.__version__[0]) >= 3:
        # GDAL 3 axis order: https://github.com/OSGeo/gdal/issues/1546
        in_spatial_ref.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)
        spatial_ref_out.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)

    out_datasource, out_layer = mem_layer("reproject", in_layer, epsg=epsg)
    out_layer_defn = out_layer.GetLayerDefn()
    reproject = osr.CoordinateTransformation(in_spatial_ref, spatial_ref_out)
    indices = field_indices(in_layer)

    for feature in Progress(in_layer, "Reproject", quiet):
        geometry = feature.GetGeometryRef()
        geometry.Transform(reproject)
        items = feature_items(feature, indices)
        add_feature(out_layer, out_layer_defn, geometry, items)
    out_layer = None
    return out_datasource


def polygon_to_lines(in_layer: ogr.Layer, quiet=True):
    """Takes a polygon in layer and returns a linestring ogr datsource"""
    out_datasource, out_layer = mem_layer("poly2lines", in_layer, ogr.wkbLineString)
    out_layer_defn = out_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    in_layer.ResetReading()
    for feature in Progress(in_layer, "Poly2lines", quiet):
        boundary = feature.geometry().Boundary()
        items = feature_items(feature, indices)
        add_feature(out_layer, out_layer_defn, boundary, items)

    out_layer = None
    return out_datasource


def union_ogr(
    in_layer,
    union_layer,
    quiet=True,
    to_multi=False,
    skip_failures=True,
    keep_geom_type=True,
    keep_lower_dimensions=False,
    use_prepared_geometries=False,
):
    progress = Progress(total=100, message="OGR: Union", quiet=quiet)

    if to_multi == False:
        to_multi = "NO"
    else:
        to_multi = "YES"

    if skip_failures == False:
        skip_failures = "NO"
    else:
        skip_failures = "YES"

    if keep_lower_dimensions == False:
        lower_dimensions = "NO"
    else:
        lower_dimensions = "YES"

    if use_prepared_geometries == False:
        prepared_geometries = "NO"
    else:
        prepared_geometries = "YES"

    options = [
        f"PROMOTE_TO_MULTI={to_multi}",
        f"SKIP_FAILURES={skip_failures}",
        f"KEEP_LOWER_DIMENSION_GEOMETRIES={lower_dimensions}",
        f"USE_PREPARED_GEOMETRIES={prepared_geometries}",
    ]

    out_datasource, out_layer = mem_layer("union", in_layer)
    in_layer.Union(union_layer, out_layer, options, progress.gdal)

    # Output can be geometry collection of points and linestrings
    # Which are begin removed
    if keep_geom_type:
        out_layer = remove_foreign_geometry(out_layer)

    return out_datasource


def dissolve(
    in_layer: ogr.Layer, field=None, intersecting=False, rtree_index=None, quiet=True
):
    """
    Dissolved the vector layer into a single multipolygon feature.
    Value can be filled to used certain field.
    """

    out_datasource, out_layer = mem_layer("dissolve", in_layer)
    out_layer_defn = out_layer.GetLayerDefn()
    geom_type = in_layer.GetGeomType()

    multi_type = MULTI_TYPES[geom_type]
    in_layer.ResetReading()
    if field:
        # Dissolve per field.
        # First finds the fields then dissolves based on this

        unique = {feature[field]: [] for feature in in_layer}
        in_layer.ResetReading()
        for feature in in_layer:
            unique[feature[field]].append(feature.GetFID())

        for field_value, fid_list in Progress(
            unique.items(), f"Dissolve field {field}", quiet
        ):
            multi = ogr.Geometry(multi_type)
            for fid in fid_list:
                feature = in_layer[fid]
                multi.AddGeometry(feature.GetGeometryRef())

            dissolved = dissolve_geometry(multi)
            add_feature(out_layer, out_layer_defn, dissolved, {field: field_value})

    elif intersecting:
        # This dissolves only intersecting features, leaves the rest.
        # Considerably faster then dissolving all as it takes only a few
        # geometries per dissolve.
        # also adds ids column to show what is dissolved

        out_layer.CreateField(ogr.FieldDefn("diss_ids", ogr.OFTString))
        clusters, geometries = spatial_clusters(in_layer)
        for cluster, geometry in zip(clusters, geometries):
            id_string = "_".join([str(c) for c in cluster])
            add_feature(
                out_layer,
                out_layer_defn,
                geometry,
                {"diss_ids": id_string},
            )

    else:
        # here we are just dissolving all
        multi = ogr.Geometry(multi_type)
        in_layer.ResetReading()
        for feature in Progress(in_layer, "Dissolve", quiet):
            geometry = feature.GetGeometryRef()
            if geometry.GetGeometryType() > 3:  # multi
                for single_geom in geometry:
                    multi.AddGeometry(single_geom)
            else:
                multi.AddGeometry(geometry)

        add_feature(out_layer, out_layer_defn, dissolve_geometry(multi), {})

    out_layer = None
    return out_datasource


def sym_difference_ogr(
    in_layer,
    difference_layer,
    quiet=True,
    to_multi=False,
    skip_failures=True,
    keep_geom_type=True,
):
    progress = Progress(total=100, message="OGR: Symmetric Difference", quiet=quiet)

    if to_multi == False:
        to_multi = "NO"
    else:
        to_multi = "YES"

    if skip_failures == False:
        skip_failures = "NO"
    else:
        skip_failures = "YES"

    options = [f"PROMOTE_TO_MULTI={to_multi}", f"SKIP_FAILURES={skip_failures}"]

    out_datasource, out_layer = mem_layer("difference", in_layer)
    in_layer.SymDifference(difference_layer, out_layer, options, progress.gdal)

    # Output can be geometry collection of points and linestrings
    # Which are begin removed
    if keep_geom_type:
        out_layer = remove_foreign_geometry(out_layer)

    return out_datasource


def difference_ogr(
    in_layer,
    difference_layer,
    quiet=True,
    to_multi=False,
    skip_failures=True,
    keep_geom_type=True,
):
    """uses symmetrical difference but deletes the difference_layers results"""
    progress = Progress(total=100, message="OGR: Erase", quiet=quiet)

    if to_multi == False:
        to_multi = "NO"
    else:
        to_multi = "YES"

    if skip_failures == False:
        skip_failures = "NO"
    else:
        skip_failures = "YES"

    options = [f"PROMOTE_TO_MULTI={to_multi}", f"SKIP_FAILURES={skip_failures}"]

    out_datasource, out_layer = mem_layer("difference", in_layer)
    in_layer.Erase(difference_layer, out_layer, options, progress.gdal)

    # Output can be geometry collection of points and linestrings
    # Which are begin removed
    if keep_geom_type:
        out_layer = remove_foreign_geometry(out_layer)
    return out_datasource


def difference(
    in_layer: ogr.Layer,
    mask_layer: ogr.Layer,
    quiet=True,
    rtree_index=None,
    ignore_errors=False,
):
    """
    This function takes a difference between vector layer and difference layer.
    - Takes into account multiparts and single parts.
    - It also leaves geometries which are not valid.

    """
    in_layer_geom_type = in_layer.GetGeomType()

    geometry_types = SINGLE_TO_MULTIPLE[in_layer_geom_type]
    out_datasource, out_layer = mem_layer("difference", in_layer)
    in_layer_defn = in_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    in_layer.ResetReading()
    for in_feature in Progress(in_layer, "Difference", quiet):

        if in_feature:
            in_items = feature_items(in_feature, indices)
            in_geom = in_feature.GetGeometryRef()

            masks = spatial_filter_generator(mask_layer, in_geom, rtree_index)

            difference = in_geom
            for loop, mask in enumerate(masks):
                mask_geometry = mask.GetGeometryRef()
                difference = difference_geometry(
                    difference, mask_geometry, ignore_errors
                )

                # print if multiplication of 1000 features
                if loop % 5000 == 0 and loop > 0:
                    print(f"Doing difference at {loop} mask features")

            diff_part_type = difference.GetGeometryType()
            if diff_part_type not in geometry_types:
                if diff_part_type == ogr.wkbGeometryCollection:
                    for part in difference:
                        if part.GetGeometryType() == in_layer_geom_type:
                            add_feature(
                                out_layer,
                                in_layer_defn,
                                part,
                                in_items,
                            )

            else:
                add_feature(
                    out_layer,
                    in_layer_defn,
                    difference,
                    in_items,
                )

    out_layer = None
    return out_datasource


def ogr_clip(
    in_layer,
    mask_layer,
    to_multi=False,
    skip_failures=False,
    quiet=True,
    keep_geom_type=True,
):
    """Fast, but not transparant
    Geometry collections can be an output, this is not what we want
    params:
        to_multi: promotes all to multi
        skip_failures: Skips all failures
        keep_geom_type: Removes all geometry types which are not
        the same as the original
    """
    progress = Progress(total=100, message="OGR: Clip", quiet=quiet)

    if to_multi == False:
        to_multi = "NO"
    else:
        to_multi = "YES"

    if skip_failures == False:
        skip_failures = "NO"
    else:
        skip_failures = "YES"

    options = [f"PROMOTE_TO_MULTI={to_multi}", f"SKIP_FAILURES={skip_failures}"]

    out_datasource, out_layer = mem_layer("clip", in_layer)
    in_layer.Clip(mask_layer, out_layer, options, progress.gdal)

    # Output can be geometry collection of points and linestrings
    # Which are begin removed
    if keep_geom_type:
        out_layer = remove_foreign_geometry(out_layer)

    return out_datasource


def clip(
    in_layer: ogr.Layer,
    mask_layer: ogr.Layer,
    quiet: bool = True,
    rtree_index=None,
):
    """
    Takes two ogr layer and returns a clipped layer
    We are skipping features without geometries.
    If the feature falls outside of the masks, the will not be included as well

    """
    out_datasource, out_layer = mem_layer("clip", in_layer)
    out_layer_defn = out_layer.GetLayerDefn()
    geom_type = in_layer.GetGeomType()

    in_layer.ResetReading()
    for in_feature in Progress(in_layer, "clip", quiet):
        in_geometry = in_feature.GetGeometryRef()

        if in_geometry:
            mask_generator = spatial_filter_generator(
                mask_layer, in_geometry, rtree_index
            )
            for mask in mask_generator:
                mask_geometry = mask.GetGeometryRef()
                clipped_geometries = clip_geometry(
                    in_geometry, mask_geometry, output_type=geom_type
                )

                if clipped_geometries:
                    items = in_feature.items()
                    for geometry in clipped_geometries:
                        add_feature(
                            out_layer,
                            out_layer_defn,
                            geometry,
                            items,
                        )

    return out_datasource


def merge(vector_path_list: list, simplify: float = 0, quiet=True):
    """merges list of vector paths and return as ogr datasource"""
    if type(vector_path_list[0]) == str:
        ds = ogr.Open(vector_path_list[0])
        layer = ds[0]
    else:
        ds = vector_path_list[0]
        layer = ds.layer

    geom_type = layer.GetGeomType()
    out_datasource, out_layer = mem_layer("merge", layer, geom_type)
    for file in Progress(vector_path_list, "Poly2lines", quiet):
        if type(file) == str:
            ds = ogr.Open(file)
        else:
            ds = file.ds

        if ds is None:
            logger.error("dataset is None")
            continue

        layer = ds[0]
        layer_defn = layer.GetLayerDefn()

        layer.ResetReading()
        for feat in layer:
            if feat:
                geometry = feat.GetGeometryRef().Clone()
                geometry = geometry.Simplify(simplify)
                attributes = feat.items()
                add_feature(out_layer, layer_defn, geometry, attributes)
    return out_datasource


def upload(
    pgds: ogr.DataSource,
    layer: ogr.Layer,
    layer_name: str,
    schema="public",
    overwrite="YES",
    spatial_index="GIST",
    fid_column="ogc_fid",
    geometry_name="the_geom",
    force_multi=True,
    quiet=False,
):
    """Takes uploading the data to a postgres database with different features
    writing with sql-statements so that we can understand what is happening
    params:
        layer: input layer
        layer_name: writes to this name

    """

    options = [
        f"OVERWRITE={overwrite}",
        f"SCHEMA={schema}",
        f"SPATIAL_INDEX={spatial_index}",
        f"FID={fid_column}",
        f"GEOMETRY_NAME={geometry_name}",
    ]

    sr = layer.GetSpatialRef()
    sr.AutoIdentifyEPSG()

    new_layer = pgds.CreateLayer(layer_name, sr, layer.GetGeomType(), options)
    for x in range(layer.GetLayerDefn().GetFieldCount()):
        new_layer.CreateField(layer.GetLayerDefn().GetFieldDefn(x))
    new_layer_defn = new_layer.GetLayerDefn()

    layer.ResetReading()
    for loop, feature in Progress(layer, "Upload", quiet, enum=True):
        add_feature(
            new_layer,
            new_layer_defn,
            feature.geometry(),
            feature.items(),
        )


def vonoroi(in_layer: ogr.Layer, buffer=1):
    """Create vonoroi polygons based on a point layer
    params:
        in_layer: ogr point Layer
        quiet: Boolean
        Buffer: used to include outer points
    """
    out_datasource, out_layer = mem_layer("vonoroi", in_layer, 3)
    out_layer = out_datasource[0]
    out_layer_defn = out_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    x1, x2, y1, y2 = in_layer.GetExtent()
    wkt = POLYGON.format(x1=x1, x2=x2, y1=y1, y2=y2)
    extent_geometry = ogr.CreateGeometryFromWkt(wkt)

    point_list = []
    point_items = {}
    for fid, feature in Progress(in_layer, "Vonoroi - Setting input points", enum=True):
        geom = feature.GetGeometryRef()
        point_list.append([*geom.GetPoints()[0]])
        point_items[fid] = feature_items(feature, indices)

    # add extent to properly add edge points
    for line in extent_geometry:
        for point in line.GetPoints():
            point_list.append([point[0], point[1]])

    vor = spatial.Voronoi(point_list)
    for id, region_index in Progress(
        vor.point_region, "Vonoroi - Processing output polygons", enum=True
    ):
        rpoints = []
        for vertex_index in vor.regions[region_index]:
            if vertex_index != -1:  # the library uses this for infinity
                rpoints.append(list(vor.vertices[vertex_index]))
        rpoints.append(rpoints[0])
        if len(rpoints) < 4 or id > len(point_items) - 1:  # anders geen polygon
            continue

        polygon = Polygon.from_points(rpoints)
        if not polygon.Within(extent_geometry):
            polygon = polygon.Intersection(extent_geometry)

        add_feature(out_layer, out_layer_defn, polygon, point_items[id])

    return out_datasource


def spatial_clusters(in_layer):
    """
    Returns a list of ids of geometries that intersect each other.
    and also returns a list of multipolygons of clustered geometries.

    We are Rtree directly in the script to increase the speed of clustering.

    """

    work_ds, work_layer = mem_layer("work", in_layer, shell=False)
    work_index = create_index_streamed(work_layer, "")

    total = work_layer.GetFeatureCount()
    progress = Progress(message="Spatial clustering", total=total)

    cluster_list = []
    cluster_list_geometries = []

    # keep repeating until the work layer is empty
    while work_layer.GetFeatureCount() != 0:

        # new cluster id list
        cluster_ids = []
        cluster_geometry = ogr.Geometry(ogr.wkbMultiPolygon)

        # get first feature, geometry, first spatial filter, delete from work
        feature = work_layer.GetNextFeature()
        geometry = feature.GetGeometryRef().Clone()

        cluster_ids.append(feature.GetFID())
        work_layer.DeleteFeature(feature.GetFID())
        work_index.delete(feature.GetFID(), geometry.GetEnvelope())

        cluster_geometry.AddGeometry(geometry)
        cluster_geometry = ogr.ForceToMultiPolygon(cluster_geometry.UnionCascaded())

        # keep repeating until no more growth of the cluster
        while True:

            growth = False  # we are not growing
            intersecting = work_index.intersection(cluster_geometry.GetEnvelope())
            for intersect_id in intersecting:
                # get next intersecting feature
                intersect = work_layer.GetFeature(intersect_id)

                # check if it intersects with the original feature
                intersect_geometry = intersect.GetGeometryRef().Clone()
                if intersect_geometry.Intersects(cluster_geometry):

                    # we are growing
                    growth = True

                    # add this to the cluster
                    cluster_ids.append(intersect_id)
                    cluster_geometry.AddGeometry(intersect_geometry)
                    cluster_geometry = ogr.ForceToMultiPolygon(
                        cluster_geometry.UnionCascaded()
                    )

                    # delete from input
                    work_layer.DeleteFeature(intersect_id)
                    work_index.delete(intersect_id, intersect_geometry.GetEnvelope())

            if not growth:  # no more growth
                break

        # add the cluster to the cluster_list
        cluster_list.append(cluster_ids)
        cluster_list_geometries.append(cluster_geometry)
        progress.show(custom_add=len(cluster_ids))

    return cluster_list, cluster_list_geometries


def centerlines(in_layer, resolution, quiet):
    """creates centerlines from polygons"""
    out_datasource, out_layer = mem_layer("centerlines", in_layer, geometry_type=2)
    out_layer_defn = out_layer.GetLayerDefn()
    indices = field_indices(in_layer)

    in_layer.ResetReading()
    for in_feature in Progress(in_layer, "centerlines", quiet):
        in_geometry = in_feature.GetGeometryRef()
        out_geometry = centerline_geometry(in_geometry, resolution)

        in_items = feature_items(in_feature, indices)
        add_feature(
            out_layer,
            out_layer_defn,
            out_geometry,
            in_items,
        )

    return out_datasource


def driver_extension_mapping():
    """return driver extensions for ogr based on small name"""
    ext = {}
    for i in range(ogr.GetDriverCount()):
        drv = ogr.GetDriver(i)
        if (
            drv.GetMetadataItem("DCAP_VECTOR") == "YES"
            and drv.GetMetadataItem("DCAP_CREATE") == "YES"
        ):
            driver = drv.GetMetadataItem("DMD_EXTENSION")
            if driver:
                ext["." + driver] = drv.GetName()
    return ext


def remove_foreign_geometry(layer):
    """removes geometrie types other than the one of the layer"""
    geom_type = layer.GetGeomType()
    for feature in layer:
        geometry = feature.GetGeometryRef()
        if geometry.GetGeometryType() != geom_type:
            layer.DeleteFeature(feature.GetFID())
    return layer


# speed-up funtions
def spatial_filter_generator(
    mask_layer, in_geom, rtree_index, yield_feature=True, reset=True
):
    """creates a spatially filtered features
    uses rtree in rtree is present

        Not that mem_layer usually slows it doen when a very large
        shape present.
    """
    if rtree_index is not None:
        xmin, xmax, ymin, ymax = in_geom.GetEnvelope()
        for i in rtree_index.intersection((xmin, xmax, ymin, ymax)):
            if yield_feature:
                yield mask_layer.GetFeature(i)
            else:
                yield i
    else:
        mask_layer.SetSpatialFilter(in_geom)
        if not reset:
            layer = mask_layer
        else:
            ds, layer = mem_layer("", mask_layer, shell=False)
            mask_layer.SetSpatialFilter(None)

        for feature in layer:
            if yield_feature:
                yield feature
            else:
                yield feature.GetFID()


def field_indices(layer):
    """using a dictionary increases add_feature speed by a few fold"""
    indices = {}
    defn = layer.GetLayerDefn()
    for i in range(defn.GetFieldCount()):
        name = defn.GetFieldDefn(i).GetName()
        indices[name] = i
    return indices


def feature_items(feature, indices):
    """unpacking items in this way is the most speedy"""
    return {n: feature.GetField(i) for n, i in indices.items()}
