# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 08:43:02 2020

@author: chris.kerklaan

ThreediEdits is a class based on vector.py and raster.py to edit threedi models
The class always edits the model in memory and you'll have to write the model
to show the results

# TODO:
    1. Add check and migration from threedi_modelchecker.
    2. correcte types moeten al in model zitten, voordat je het model from scratch maakt
    3. Laad je gehele model in geheugen, voor de snelheid, 
    wanneer een connectie wordt gemaakt met de postgrestabellen maak je weer verbinding
# Bug:
    
# Bugs solved

# Opmerkingen

"""

__version__ = "0.1"
__author__ = "Chris Kerklaan - Nelen & Schuurmans"

# System imports
import os
import copy
import logging
import pathlib

# Third-party imports
from osgeo import ogr
from cached_property import cached_property

# Local imports
import threedi_raster_edits as tre
from threedi_raster_edits.gis.vector import Vector
from threedi_raster_edits.threedi.rastergroup import ThreediRasterGroup
from threedi_raster_edits.threedi.vectorgroup import ThreediVectorGroup
from threedi_raster_edits.threedi.tables.constants import TABLES, raster_fields
from threedi_raster_edits.threedi.tables.models import MODEL_MAPPING
from threedi_raster_edits.utils.dependencies import DEPENDENCIES
from threedi_raster_edits.utils.project import Classes, Functions


# structure
classes = Classes(__name__, local_only=True)
functions = Functions(__name__)

# Globals
# Drivers
OGR_SQLITE_DRIVER = ogr.GetDriverByName("SQLite")
OGR_MEM_DRIVER = ogr.GetDriverByName("Memory")
SCENARIO = 1  # since klondike it is always 1.

# logger
logger = logging.getLogger(__name__)


class ThreediEdits(ThreediVectorGroup):
    """An object for editing a threedi model,
    can be openen from scratch, from any ogr format (sqlite, postgres, geopackage).

        mode:
            'write': Used to write a file
            'empty': Returns an empty in-mem ogr threedi model
            'memory': Used when a full threedimodel is presented in memory
            'read': Used for reading a model only

    """

    instance = "threedi.edits.ThreediEdits"

    def __init__(
        self,
        sqlite_path=None,
        mode="read",
        pg_str=None,
    ):

        if sqlite_path is not None and not os.path.exists(str(sqlite_path)):
            raise FileNotFoundError("Path does not exist")

        if sqlite_path:
            ogr_ds = ogr.Open(str(sqlite_path), 0)
            self.model_dir = os.path.dirname(sqlite_path) + "/"
            self.name = pathlib.Path(sqlite_path).stem
            self.path = os.path.join(os.getcwd(), sqlite_path)

        if pg_str:
            ogr_ds = ogr.Open(pg_str, 0)

        if mode == "empty":
            ogr_ds = None

        super().__init__(ogr_ds, mode)

    @classmethod
    def from_pg(
        cls,
        dbname,
        host="nens-3di-db-03.nens.local",
        port="5432",
        user="threedi",
        password="1S418lTYWLFsYxud4don",
    ):

        pg_str = ("PG:host={} port={} user='{}'" "password='{}' dbname='{}'").format(
            host, port, user, password, dbname
        )
        return cls(pg_str=ogr.Open(pg_str))

    @classmethod
    def from_scratch(cls):
        return cls(mode="empty")

    def __getitem__(self, table):
        table_model = MODEL_MAPPING[table]

        if hasattr(table_model, "required"):
            required = copy.deepcopy(table_model.required)
            for key, value in table_model.required.items():
                required[key] = getattr(self, key)
        else:
            required = {}
        return MODEL_MAPPING[table](self.ds, table, **required)

    def __setitem__(self, table_name, ogr_layer):
        """replaces an entire table"""
        self.ds.DeleteLayer(table_name)
        self.ds.CreateLayer(ogr_layer)

    @property
    def empty(self) -> bool:
        """
        Returns true or false based on the first global setting row
        """
        layer = self.ds.GetLayerByName("v2_global_settings")
        return layer.GetFeatureCount() == 0

    @property
    def _get_raster_files(self) -> dict:
        """Retrieves all raster files from the global settings,
        Returns empty dict if no global settings.

        """

        if self.empty:
            return {}

        global_settings = self.ds.GetLayerByName("v2_global_settings")
        gs = global_settings.GetFeature(SCENARIO)
        paths = {field: gs[field] for field in raster_fields if field in gs.keys()}
        infiltration_settings = self.ds.GetLayerByName("v2_simple_infiltration")
        infiltration_id = gs["simple_infiltration_settings_id"]
        if type(infiltration_id) == int:
            infiltration = infiltration_settings.GetFeature(infiltration_id)
            if infiltration is not None:
                paths["infiltration_rate_file"] = infiltration["infiltration_rate_file"]
                paths["max_infiltration_capacity_file"] = infiltration[
                    "max_infiltration_capacity_file"
                ]
        return paths

    @property
    def _existing_raster_paths(self) -> dict:
        """
        Retrieves raster files if they exist.
        Return an empty dictionary otherwise.
        """
        if not hasattr(self, "model_dir"):
            return {}
        else:
            paths = {}
            for k, v in self._get_raster_files.items():
                if v is None:
                    continue
                if v == "":
                    continue

                if os.path.exists(self.model_dir + v):
                    paths[k] = self.model_dir + v
            return paths

    @property
    def placed_rasters(self):
        return self.rasters.count > 0

    @property
    def has_existing_rasters(self):
        return len(self._existing_raster_paths) > 0

    @cached_property
    def rasters(self):
        return ThreediRasterGroup(**self._existing_raster_paths)

    def set_rasters(self, value):
        self.__dict__["rasters"] = value

    @cached_property
    def extent(self):
        return self.rasters.dem.extent

    @cached_property
    def extent_geometry(self):
        return self.rasters.dem.extent_geometry

    @cached_property
    def extent_vector(self):
        extent = Vector.from_scratch("", 3, self.rasters.dem.epsg)
        extent.add(geometry=self.rasters.dem.extent_geometry)
        return extent

    def write(self, path, check=True, rasters=False, rasters_correct=True):
        path = str(path)

        if (self.has_existing_rasters or self.placed_rasters) and rasters:
            group = self.rasters
            if rasters_correct:
                group.correct()
            group.write(str(pathlib.Path(path).parent), self._get_raster_files)

        self.write_model(path, check)

    @property
    def epsg(self):
        return self.global_setting["epsg"]

    @cached_property
    def nodes(self):
        return self["v2_connection_nodes"]

    @cached_property
    def manholes(self):
        return self["v2_manhole"]

    @cached_property
    def pipes(self):
        return self["v2_pipe"]

    @cached_property
    def global_setting(self):
        return self["v2_global_settings"][SCENARIO]

    @cached_property
    def global_settings(self):
        return self["v2_global_settings"]

    @cached_property
    def simple_infiltration(self):
        return self["v2_simple_infiltration"]

    @cached_property
    def numerical_settings(self):
        return self["v2_numerical_settings"]

    @cached_property
    def aggregation_settings(self):
        return self["v2_aggregation_settings"]

    @cached_property
    def obstacles(self):
        return self["v2_obstacle"]

    @cached_property
    def channels(self):
        return self["v2_channel"]

    @cached_property
    def cross_section_definitions(self):
        return self["v2_cross_section_definition"]

    @cached_property
    def cross_section_locations(self):
        return self["v2_cross_section_location"]

    @cached_property
    def grid_refinement_areas(self):
        return self["v2_grid_refinement_area"]

    @cached_property
    def grid_refinements(self):
        return self["v2_grid_refinement"]

    @cached_property
    def boundary_conditions_1d(self):
        return self["v2_1d_boundary_conditions"]

    @cached_property
    def laterals_1d(self):
        return self["v2_1d_lateral"]

    @cached_property
    def laterals_2d(self):
        return self["v2_2d_lateral"]

    @cached_property
    def pumpstations(self):
        return self["v2_pumpstation"]

    @cached_property
    def levees(self):
        return self["v2_levee"]

    @cached_property
    def weirs(self):
        return self["v2_weir"]

    @cached_property
    def orifices(self):
        return self["v2_orifice"]

    @cached_property
    def culverts(self):
        return self["v2_culvert"]

    @cached_property
    def calculation_points(self):
        return self["v2_calculation_point"]

    @cached_property
    def connected_points(self):
        return self["v2_connected_pnt"]

    @cached_property
    def control(self):
        return self["v2_control"]

    @cached_property
    def control_group(self):
        return self["v2_control_group"]

    @cached_property
    def control_measure_group(self):
        return self["v2_control_measure_group"]

    @cached_property
    def control_measure_map(self):
        return self["v2_control_measure_map"]

    @cached_property
    def control_table(self):
        return self["v2_control_table"]

    @cached_property
    def control_memory(self):
        return self["v2_control_memory"]

    @cached_property
    def impervious_surface(self):
        return self["v2_impervious_surface"]

    @cached_property
    def interflow(self):
        return self["v2_interflow"]

    @property
    def dem(self):
        if self.has_existing_rasters:
            return self.rasters.dem

    @dem.setter
    def dem(self, raster):
        self.__dict__["rasters"]["dem"] = raster

    @property
    def friction(self):
        return self.rasters.friction

    @friction.setter
    def friction(self, raster):
        self.__dict__["rasters"]["friction"] = raster

    @property
    def interception(self):
        return self.rasters.interception

    @interception.setter
    def interception(self, raster):
        self.__dict__["rasters"]["interception"] = raster

    @property
    def initial_waterlevel(self):
        return self.rasters.initial_waterlevel

    @initial_waterlevel.setter
    def initial_waterlevel(self, raster):
        self.__dict__["rasters"]["initial_waterlevel"] = raster

    @property
    def infiltration(self):
        return self.rasters.infiltration

    @infiltration.setter
    def infiltration(self, raster):
        self.__dict__["rasters"]["infiltration"] = raster

    @property
    def max_infiltration_capacity(self):
        return self.rasters.max_infiltration_capacity

    @max_infiltration_capacity.setter
    def max_infiltration_capacity(self, raster):
        self.__dict__["rasters"]["max_infiltration_capacity"] = raster

    @property
    def node_view(self, data=False):
        return create_node_view(self, data)

    def nodes_height(self):
        dem = self.dem
        dem.return_raster = True
        return sample_nodes(self, dem.reproject(4326))

    def nodes_sample(self, raster):
        return sample_nodes(self, raster)

    def filter(self, table, node_fid=None, code=None):
        """searches a certain table"""
        return search_table(table, node_fid, code)

    def spatial_filter(self, geometry):
        """filter the model on connection nodes"""
        nodes = self.nodes.spatial_filter(geometry)
        filtered = {}
        for table in self:
            filtered[table.name] = []
            for node in nodes:
                filtered[table.name].append(self.node_view[node.id])
        return filtered

    def derive_raster_extent(self, raster, threshold=0, idx=1):
        """polygonizes raster based on data/nodata"""
        self.raster_extent = raster.polygonize(quiet=False)
        return self.raster_extent

    def delete_tables(self, deletes=None, quiet=True):
        delete_tables(self, deletes, quiet)

    def delete_node(self, node_id, clear=True):
        """deletes the node and all its associates"""
        delete_node(self, node_id, clear)

    def clip(self, vector, rasters=True):
        """clips a model, including the rasters on a vector"""
        clip(self, vector, rasters)

    def add_breach(
        self,
        point,
        channel,
        exchange_level,
        levee_id,
        code,
        initial_waterlevel,
        cross_section_definition_id,
        calculation_type=102,
        dist_calc_points=100,
        storage_area=0,
        reference_level=-10,
        bank_level=10,
        friction_type=2,
        friction_value=0.26,
        zoom_category=1,
    ):

        """adds:
            - start and end nodes
            - channel
            - cross section location
            - calculation points
            - connected points

        based on a line geometry and a point geometry and a cross section definition id
        please add the boundary yourself
        point geometry is the connected_pnt, the line geometry becomes the dummy channel
        """

        add_breach(
            self,
            point,
            channel,
            exchange_level,
            levee_id,
            code,
            initial_waterlevel,
            cross_section_definition_id,
            calculation_type,
            dist_calc_points,
            storage_area,
            reference_level,
            bank_level,
            friction_type,
            friction_value,
            zoom_category,
        )

    # Optional

    @cached_property
    def grid(self):
        if DEPENDENCIES.threedigrid_builder.installed:
            return tre.threedi.grid.make_grid(self)
        else:
            raise ImportError("Please install threedigrid builder!")


def sample_nodes(model, raster):
    return {node.fid: raster.read(node.geometry) for node in model.nodes}


def search_table(table, node_fid=None, code=None):
    """should be a general fast search of a random field in a certain table"""
    if code:
        filtering = {"code": code}
    elif node_fid:
        filtering = {"fid": node_fid}

    if table.layer_name in TABLES["single"]:
        return table.filter(return_fid=True, **filtering)

    if table.layer_name in TABLES["start_end"]:
        if node_fid:
            start = table.filter(connection_node_start_id=node_fid, return_fid=True)
            end = table.filter(connection_node_end_id=node_fid, return_fid=True)
            return end + start
        elif code:
            return table.filter(return_fid=True, **filtering)


def create_node_view(model, data=False):
    """creates a dictionary based on node ids"""
    nodes = model.nodes
    nodes.set_table()
    node_table = nodes.table
    new_dict = {fid: {} for fid in node_table["fid"]}

    # add connection node info
    for i in range(0, nodes.count):
        new_dict[node_table["fid"][i]]["v2_connection_nodes"] = {
            key: node_table[key][i] for key in node_table
        }

    for table in TABLES["single"] + TABLES["start_end"]:
        model_table = model[table]
        model_table.set_table()

        add = model_table.table
        for i in range(len(model[table])):

            if table in TABLES["single"]:
                node_table = new_dict[add["connection_node_id"][i]]

                if data:
                    node_table[table] = {key: add[key][i] for key in add}
                else:
                    if table not in node_table:
                        node_table[table] = []

                    node_table[table].append(add["fid"][i])
            else:

                node_table_start = new_dict[add["connection_node_start_id"][i]]
                node_table_end = new_dict[add["connection_node_end_id"][i]]

                if data:
                    if add["connection_node_start_id"][i]:
                        node_table_start[table + "_start"] = {
                            key: add[key][i] for key in add
                        }

                    if add["connection_node_end_id"][i]:
                        node_table_end[table + "_end"] = {
                            key: add[key][i] for key in add
                        }
                else:

                    if table not in node_table_start:
                        node_table_start[table] = []

                    if table not in node_table_end:
                        node_table_end[table] = []

                    node_table_start[table].append(add["fid"][i])
                    node_table_end[table].append(add["fid"][i])

    return new_dict


def clip(model: ThreediEdits, vector, rasters):
    """
    Clips a model based on the geometry

    Parameters
    ----------
    db : ThreediEdits
    geometry : ogr.Geometry

    Returns
    -------
    None.

    """

    assert vector.epsg == 4326

    for feature in vector:
        geometry = feature.geometry

        # Find connection nodes in the area
        print("Finding nodes outside of the area")
        nodes = model.nodes.spatial_filter(geometry, return_fid=True)
        total_nodes = model.nodes.fids
        delete_nodes = list(set(total_nodes) - set(nodes))

        print("Removing tables associated with these nodes")
        deletes = {k: [] for k in TABLES["order"]}
        for node in delete_nodes:
            for table, values in delete_node(model, node, clear=False).items():
                deletes[table].extend(values)

        unique = {k: list(set(v)) for k, v in deletes.items()}
        model.delete_tables(unique, quiet=False)

        print("Finding  and deleting none existing cross section locations")
        # non existing cross section locations
        for csl_id in model.channels.non_existing_cross_section_locations():
            model.cross_section_locations.delete(csl_id)

        # levees
        print("Deleting levees outside of the area")
        levees = model.levees.spatial_filter(geometry, return_fid=True)
        delete_levees = list(set(model.levees.fids) - set(levees))
        for delete_levee in delete_levees:
            model.levees.delete(delete_levee)

        print("Deleting grid refinements outside of the area")
        grid_refinements = model.grid_refinements.spatial_filter(
            geometry, return_fid=True
        )
        delete_refinements = list(
            set(model.grid_refinements.fids) - set(grid_refinements)
        )
        for delete_refinement in delete_refinements:
            model.grid_refinements.delete(delete_refinement)

    if rasters:
        group = model.rasters
        group.clip(vector)
        model.rasters = group


def delete_tables(model: ThreediEdits, deletes: dict = None, quiet=True):
    """
    Deletes features in tabels in the correct order
    Parameters
    ----------
    db : ThreediEdits
    deletes : dict
        dict with the table name and fids to delete e.g., {'v2_pipe': [1,2,3,4]}.
    quiet : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    None.

    """
    for table in TABLES["order"]:
        if deletes:
            if table not in deletes:
                continue

            fids = deletes[table]
        else:
            fids = model[table].fids

        for fid in fids:
            model[table].delete(fid)


def delete_node(db: ThreediEdits, node_id: int, clear=True):
    """
    Deletes a node and all its assciates
    """

    view = db.node_view[node_id]
    deletes = {k: [] for k in TABLES["order"]}
    for delete_table in deletes:
        if delete_table in view:
            if type(view[delete_table]) == dict:
                fid = view[delete_table]["fid"]
                if not fid in deletes[delete_table]:
                    deletes[delete_table].append(fid)
            else:
                for fid in view[delete_table]:
                    if not fid in deletes[delete_table]:
                        deletes[delete_table].append(fid)
    # associates = [(i, deletes[i]) for i in deletes if len(deletes[i]) > 0]
    logger.info("Deleting associates f{associates}")

    if clear:
        db.delete_tables(deletes, quiet=True)
    else:
        return deletes


def add_breach(
    model: ThreediEdits,
    point,
    channel,
    exchange_level,
    levee_id,
    code,
    initial_waterlevel,
    cross_section_definition_id,
    calculation_type=102,
    dist_calc_points=100,
    storage_area=0,
    reference_level=-10,
    bank_level=10,
    friction_type=2,
    friction_value=0.26,
    zoom_category=1,
):

    """adds:
        - nodes,
        - channel
        - cross section location
        - calculation points
        - connected points

    based on a line geometry and a point geometry

    point geometry is the connected_pnt, the line geometry becomes the dummy channel
    """

    # add channel to model
    channels = model.channels
    connection_nodes = model.nodes
    calculation_points = model.calculation_points
    connected_points = model.connected_points
    cross_section_locations = model.cross_section_locations

    start_node = connection_nodes.add(
        items={
            "code": code,
            "initial_waterlevel": initial_waterlevel,
            "storage_area": storage_area,
        },
        geometry=channel[0].geometry.start_point,
    )

    # add end point
    end_node = connection_nodes.add(
        items={
            "code": code,
            "initial_waterlevel": initial_waterlevel,
            "storage_area": storage_area,
        },
        geometry=channel[0].geometry.end_point,
    )

    # add channels with these connection nodes
    channel_id = channels.add(
        items={
            "connection_node_end_id": end_node,
            "connection_node_start_id": start_node,
            "display_name": code,
            "code": code,
            "dist_calc_points": dist_calc_points,
            "calculation_type": calculation_type,
            "zoom_category": zoom_category,
        },
        geometry=channel[0].geometry,
    )

    cross_section_locations.add(
        items={
            "code": code,
            "reference_level": reference_level,
            "bank_level": bank_level,
            "friction_type": friction_type,
            "friction_value": friction_value,
            "channel_id": channel_id,
            "definition_id": cross_section_definition_id,
        },
        geometry=channel[0].geometry.middle_point(),
    )

    calc_points = channels.predict_calculation_points(channel_id)
    new_calc_points = []
    for calc_point in calc_points:
        fid = calculation_points.add(items=calc_point, geometry=calc_point["the_geom"])
        new_calc_points.append(fid)

    # add connected points
    connected_points.add(
        items={
            "exchange_level": exchange_level,
            "calculation_pnt_id": new_calc_points[0],
            "levee_id": levee_id,
        },
        geometry=point.geometry,
    )
