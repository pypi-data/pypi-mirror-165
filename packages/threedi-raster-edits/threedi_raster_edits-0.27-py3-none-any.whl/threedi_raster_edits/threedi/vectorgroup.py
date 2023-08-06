# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 08:52:16 2021

@author: chris.kerklaan

#TODO:
    
# The current threedi_model_checker has needs an 'migrated sqlite'. However,
when you update the migrated sqlite, you increase
    
"""

# First-party imports
import shutil
import pathlib
import logging

# Third-party imports
from osgeo import ogr
from osgeo import osr

# from threedi_modelchecker.exporters import format_check_results
# from threedi_modelchecker import ThreediModelChecker
# from threedi_modelchecker import ThreediDatabase


# Local imports
import threedi_raster_edits as tre
from threedi_raster_edits.threedi.tables.constants import TABLES, Properties
from threedi_raster_edits.threedi.tables.models import MODEL_MAPPING
from threedi_raster_edits.threedi.utils.exceptions import ThreediConnectedTableError
from threedi_raster_edits.gis.vectorgroup import VectorGroup
from threedi_raster_edits.gis.vector import Vector

# Globals
FILE_PATH = pathlib.Path(__file__)
EMPTY_SQLITE_PATH = str(FILE_PATH.parent / "data" / "empty_klondike.sqlite")

# Drivers
OGR_SQLITE_DRIVER = ogr.GetDriverByName("SQLite")

# Logger
logger = logging.getLogger(__name__)


class ThreediVectorGroup(VectorGroup):
    """ThreediVectorGroup's base is always made up from  constants fields
    if a new 'sqlite' gets added it will always be transfered to the in memory object
    params:
        ogr_ds: ogr.DataSource
        mode:
            'write': Used to write a file
            'empty': Returns an empty in-mem ogr threedi model
            'memory': The threedimodel is copied into memory, makes speedy edits
            'read': Used for reading a model only


    """

    instance = "threedi.vectorgroup.VectorGroup"

    def __init__(self, ogr_ds, mode="memory"):

        if mode == "write":
            super().__init__(ogr_ds=ogr_ds, memory=False, write=True)
        elif mode == "read":
            super().__init__(ogr_ds=ogr_ds, memory=False, write=False)
        elif mode == "empty":
            super().__init__(ogr_ds=create_empty_model().ds, memory=False)
        elif mode == "memory":
            super().__init__(ogr_ds=self.from_ds(ogr_ds), memory=False)

        logger.debug(f"Opened threedi model in {mode} mode")

        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(4326)
        self.mode = mode

    def __str__(self):
        return f"3Di model, tables: {self.tables}"

    def __repr__(self):
        return f"({self.instance}) 3Di model, tables: {self.tables}"

    def __iter__(self):
        for table_name in TABLES["all"]:
            if table_name in self.layers:
                yield self.get_table(table_name)

    def from_ds(self, new_ogr_ds):
        group = create_empty_model()
        for table_name in TABLES["all"]:
            logger.info(f"Loading {table_name}")
            layer = new_ogr_ds.GetLayerByName(table_name)
            if not layer:
                logger.info(f"could load {table_name}")
                continue

            base_layer = group[table_name]
            for feature in layer:
                base_layer.add(
                    items=feature.items(),
                    geometry=feature.geometry(),
                    fid=feature.GetFID(),
                )
        return group.ds

    @property
    def tables(self):
        return [l for l in TABLES["all"] + self.layers if "v2" in l]

    def get_table(self, table_name):
        """loads a table without requirements 'None'"""

        table_class = MODEL_MAPPING[table_name]

        if hasattr(table_class, "required"):
            return MODEL_MAPPING[table_name](self.ds, table_name, None)
        else:
            return MODEL_MAPPING[table_name](self.ds, table_name)

    def __getitem__(self, table):
        return self.get_table(table)

    def pre_write_checks(self):
        """Some fast checks"""
        for table in self:
            self.check_connected_table(table)

    def check_connected_table(self, table):
        if not "connected_tables" in table.properties:
            return

        table_properties = table.properties["connected_tables"]
        for connected_name, connected_fields in table_properties.items():

            connected_table = self[connected_name]
            connected_fids = connected_table.fids
            for feature in table:
                for field in connected_fields:
                    try:
                        feature[field]
                    except Exception as e:
                        print(e, field, connected_table)

                    if not feature[field] in connected_fids:
                        raise ThreediConnectedTableError(
                            """id not found""",
                            table.name,
                            connected_table.name,
                            field,
                            feature[field],
                        )

    def create_output_model(self, path):
        """Creates an empty sqlite"""
        shutil.copyfile(EMPTY_SQLITE_PATH, path)
        output = ThreediVectorGroup(ogr.Open(path, 1), mode="write")
        empty_tables = [
            "v2_global_settings",
            "v2_aggregation_settings",
            "v2_numerical_settings",
        ]
        for empty_table in empty_tables:
            table = output[empty_table]
            for fid in table.fids:
                table.delete(fid)
            table = None
        return output

    def write_model(self, path, check=True):
        """whilst copy layer is faster than iterating over every feature,
        we want check the feature on field types and use the sqlite constraints
        therefore iteration is chosen here"""

        # check connections
        if check:
            self.pre_write_checks()

        output = self.create_output_model(path)
        current_layers = output.layers

        for table in self:
            if (
                table.name not in current_layers
            ):  # Some layers have been removed, so there are more in constants than here.
                continue
            # output.ds.CopyLayer(table.layer, table.name, options=["OVERWRITE=YES", "GEOMETRY_FIELD=the_geom",
            #                                                       "FID=id"])

            """ iterating over feature method to do checks"""
            table_output = output[table.name]
            for feature in tre.Progress(
                table, f"Writing {table.name} ({table.count} rows)"
            ):
                table_output.add(feature, custom_fid=None)

        table_output = None
        output = None

        # if check:
        #    return check_model(path)


def create_empty_model():
    """creates a ThreediModelBase from scratch"""
    group = VectorGroup.from_scratch(name="Threedi Model")
    for name, threedi_property in Properties():
        # create vector, with the right geometry and fields
        if "the_geom" in threedi_property:
            geometry_type = threedi_property["the_geom"]["type"]
        else:
            geometry_type = ogr.wkbUnknown

        vector = Vector.from_scratch(name, geometry_type, 4326)

        for i, (field_name, field_values) in enumerate(threedi_property.items()):
            if field_name in ["connected_tables", "the_geom", "id"]:
                continue
            vector.add_field(field_name, field_values["type"])

        # add to the group
        group.add(vector, name)

    return group


# def check_model(path):
#     """Checks the model using ThreediModelChecker"""
#     logger.info(" Running ThreediModelChecker")
#     database = ThreediDatabase(
#         connection_settings={"db_path": path}, db_type="spatialite"
#     )
#     model_checker = ThreediModelChecker(database)
#     errors = []
#     for check, error in model_checker.errors(level="WARNING"):
#         errors.append(format_check_results(check, error))

#     if len(errors) == 0:
#         logger.info(" No errors found.")
#     else:
#         logger.info(f" Found errors: {errors}")
#     return errors
