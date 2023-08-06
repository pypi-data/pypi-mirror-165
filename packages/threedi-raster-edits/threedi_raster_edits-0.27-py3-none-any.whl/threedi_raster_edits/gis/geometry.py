# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:49:48 2021

@author: chris.kerklaan

Wrapper for an ogr geometry

TODO:
    1. Convert/fix geometry should have an input geom_type and a target_geom_type
    2. Geometry testing

Note that gdal.UseExceptions() and ogr.UseExceptions() must be on
"""
# First-party imports
import logging

# Third-party imports
from osgeo import ogr

# Local imports
from .spatial_reference import SpatialReference


# GLOBALS
logger = logging.getLogger(__name__)

POLYGON = "POLYGON (({x1} {y1},{x2} {y1},{x2} {y2},{x1} {y2},{x1} {y1}))"
POINT = "POINT ({x1} {y1})"
LINESTRING = "LINESTRING ({x1} {y1}, {x2} {y2})"

TRANSLATION = {
    "point": ogr.wkbPoint,
    "line": ogr.wkbLineString,
    "polygon": ogr.wkbPolygon,
    "multipoint": ogr.wkbMultiPoint,
    "multiline": ogr.wkbMultiLineString,
    "multiPolygon": ogr.wkbMultiPolygon,
}

SINGLE_TYPES = {
    ogr.wkbMultiSurface: ogr.wkbPolygon,
    ogr.wkbMultiPolygon: ogr.wkbPolygon,
    ogr.wkbMultiLineString: ogr.wkbLineString,
    ogr.wkbMultiPoint: ogr.wkbPoint,
    ogr.wkbPolygon: ogr.wkbPolygon,
    ogr.wkbLineString: ogr.wkbLineString,
    ogr.wkbPoint: ogr.wkbPoint,
}

MULTI_TYPES = {
    ogr.wkbPoint: ogr.wkbMultiPoint,
    ogr.wkbLineString: ogr.wkbMultiLineString,
    ogr.wkbPolygon: ogr.wkbMultiPolygon,
    ogr.wkbMultiPoint: ogr.wkbMultiPoint,
    ogr.wkbMultiLineString: ogr.wkbMultiLineString,
    ogr.wkbMultiPolygon: ogr.wkbMultiPolygon,
}

SINGLE_TYPES_INVERT = dict(map(reversed, SINGLE_TYPES.items()))
SINGLE_TO_MULTIPLE = {1: [1, 4], 2: [2, 5], 3: [3, 6], 4: [4], 5: [5], 6: [6]}
ALLOWED = {1: [1, 4], 2: [2, 5], 3: [3, 6], 4: [4, 1], 5: [5, 2], 6: [6, 3]}


class Geometry(ogr.Geometry):
    """
    Extension of an ogr geometry

    Copies the input of a geomtry, hence the pointer connection is lost
    and geometries must be set via set_feature

    Every function always leaves the original geometry untouched

    """

    def __init__(self, geometry, geometry_type=ogr.wkbPoint):

        super().__init__(wkb=geometry.ExportToWkb())
        self.AssignSpatialReference(geometry.GetSpatialReference())

    def __repr__(self):
        return f"{self.wkt}"

    def check_type(self, types):
        if not self.type in types:
            raise TypeError(f"Wrong ogr geom type {self.name} {self.type_name}")

    @property
    def area(self):
        return self.GetArea()

    @property
    def length(self):
        return self.Length()

    @property
    def name(self):
        return self.GetGeometryName()

    @property
    def type(self):
        return self.GetGeometryType()

    @property
    def is_multi(self):
        return self.type > 3

    @property
    def type_name(self):
        return ogr.GeometryTypeToName(self.type)

    @property
    def valid(self):
        return self.IsValid()

    @property
    def fixed(self):
        return fix(self)

    @property
    def points(self):
        return self.GetPoints()

    @property
    def envelope(self):
        return self.GetEnvelope()

    @property
    def wkt(self):
        return self.ExportToWkt()

    @property
    def wkb(self):
        return self.ExportToWkb()

    @property
    def wkb_size(self):
        return self.WkbSize()

    @property
    def point_on_surface(self):
        return Geometry(self.PointOnSurface())

    @property
    def centroid(self):
        return Geometry(self.Centroid())

    @property
    def boundary(self):
        return Geometry(self.GetBoundary())

    @property
    def spatial_reference(self):
        return SpatialReference.from_sr(self.GetSpatialReference(), self.centroid)

    @spatial_reference.setter
    def spatial_reference(self, sr_input):
        """takes an epsg or a spatial_reference input"""
        if type(sr_input) == int:
            sr_input = SpatialReference.from_epsg(sr_input)
        self.AssignSpatialReference(sr_input)

    @property
    def epsg(self):
        return self.spatial_reference.epsg

    @property
    def ogr(self):
        """returns a pure ogr geometry"""
        return release(self)

    def copy(self):
        return Geometry(geometry=self)

    def buffer(self, size):
        return Geometry(self.Buffer(size))

    def simplify(self, simplification):
        return Geometry(self.Simplify(simplification))

    def difference(self, geometry, ignore_errors=False):
        """returns a differenced geometry, or none if invalid or not intersects"""
        return Geometry(difference(self, geometry, ignore_errors))

    def clip(self, mask):
        """returns a list of clipped geometry in the correct output type
        or none
        """
        clipped = clip(self, mask, self.type)
        if clipped:
            return [Geometry(i) for i in clipped]
        else:
            return

    def reproject(self, out_epsg, use_points=False):
        """reprojects the geometries"""
        geometry = self.ogr
        geometry.Transform(self.spatial_reference.transform(out_epsg))
        return Geometry(geometry, self.type)

    def dissolve(self):
        """dissolved geometry, returns a single geometry"""
        return Geometry(dissolve(self), SINGLE_TYPES[self.type])

    def to_single(self):
        """creates single parts, returns a list or none"""
        return [Geometry(i) for i in multipart_to_singlepart(self)]

    def fix(self, geometry_type=None):
        return fix(self, target_geom_type=geometry_type)

    def union(self, geometry):
        return Geometry(self.Union(geometry))

    def intersection(self, geometry):
        return Geometry(self.Intersection(geometry))


def release(geometry: ogr.Geometry):
    """releases the c pointer from the geometry"""
    output = ogr.CreateGeometryFromWkb(geometry.ExportToWkb())
    output.AssignSpatialReference(geometry.GetSpatialReference())
    return output


def convert_geometry(geometry, target_geom_type):
    """
    converts geometry to target type to it's logical output type
    if ambiguous output type, it is converted to target_geom_type
    e.g., when it is a geometry collection

    We only use planar and linear geometries.
    """
    geom_type = geometry.GetGeometryType()
    is_3d = geometry.Is3D()
    if geom_type == target_geom_type and not is_3d:
        return geometry

    # convert from curve to linear
    if geometry.HasCurveGeometry():
        geometry = geometry.GetLinearGeometry()

    if is_3d:
        geometry.FlattenTo2D()

    if geom_type in [
        ogr.wkbGeometryCollection,
        ogr.wkbGeometryCollection25D,
        ogr.wkbGeometryCollectionM,
        ogr.wkbGeometryCollectionZM,
    ]:
        logger.debug("Found a geometry collection, retrieving only the first geometry")
        for geom in geometry:
            if geom.GetGeometryType() == target_geom_type:
                geometry = geom
                break

    return geometry


def fix(geometry, target_geom_type=None):
    """
    First converts a geometry to type 1,2,3,4,5,6
    Fixes a geometry to ogr geom types 1,2,3,4,5,6:
        1. pointcount for  linestrings
        2. self intersections for polygons
        3. 3D polygon

    if a geometry collection is given, it can convert to a geom_type by
    setting target_geom_type = something

    Params:
        geometry : ogr geometry
        target_geom_type: = None, fixes it until this geometry type
    Returns
        geometry: ogr geometry or None if no geometry is present
        bool: geometry validity


    """
    if geometry is None:
        return None

    if not target_geom_type:
        target_geom_type = geometry.GetGeometryType()

    geometry = convert_geometry(geometry, target_geom_type)

    if geometry.IsValid():
        return geometry

    # Transforms multipolugon into geometry collection
    # geometry = geometry.MakeValid()
    # if geometry.IsValid():
    # return geometry, True

    geom_type = geometry.GetGeometryType()
    if geom_type == ogr.wkbPoint:
        pass

    elif geom_type == ogr.wkbLineString:
        if geometry.GetPointCount() == 1:
            logger.debug("Geometry point count of linestring = 1")
            return geometry, False

    elif geom_type == ogr.wkbPolygon:
        geometry = geometry.Buffer(0)

    elif geom_type == ogr.wkbMultiPoint:
        pass

    elif geom_type == ogr.wkbMultiLineString:
        pass

    elif geom_type == ogr.wkbMultiPolygon:
        geometry = geometry.Buffer(0)

    geom_type = geometry.GetGeometryType()
    geom_name = ogr.GeometryTypeToName(geom_type)

    geometry_valid = geometry.IsValid()

    if not geometry_valid:
        logger.warning(
            f"failed fix invalid ogr geometry type: {geom_name}, {geom_type}, target {target_geom_type} "
        )
        return None
    return geometry


def multipart_to_singlepart(geometry: ogr.Geometry):
    """returns a list of geometries, if invalid none"""
    if "MULTI" in geometry.GetGeometryName():
        return [release(part) for part in geometry]
    else:
        return [geometry]


def clip(geometry: ogr.Geometry, mask: ogr.Geometry, output_type: int):
    """Clips a single geometry on a mask
    returns invalid geoms as none
    returns a geometry of an allowed output type
    returns a list
    """
    within = geometry.Within(mask)

    # check for the boundary
    if geometry.Intersects(mask) and not within:
        intersect = geometry.Intersection(mask)
        intersect_type = intersect.GetGeometryType()
        if intersect_type not in ALLOWED[output_type]:
            logger.debug("Output has incorrect geometry type")
            return

        if intersect_type > 3:
            return [intersect]
        else:
            return multipart_to_singlepart(intersect)

    elif within:
        return [geometry]

    else:
        logger.debug("Outside of geometry")
        return  # outside


def difference(geometry: ogr.Geometry, mask: ogr.Geometry, ignore_errors=False):
    """checks if intersects before doing difference"""

    try:
        if geometry.Intersects(mask):
            return geometry.Difference(mask)
    except RuntimeError:
        if not ignore_errors:
            raise RuntimeError("Difference")
        logger.debug("Geometry difference runtime error - ignore = True")

    # if not intersects or ignore errors return original geometry
    return geometry


def dissolve(multigeometry: ogr.Geometry):
    """dissolves a multigeometry into a single geometry"""
    geometry_type = multigeometry.GetGeometryType()

    if geometry_type == ogr.wkbMultiPolygon:
        union = multigeometry.UnionCascaded()
    else:
        union = ogr.Geometry(SINGLE_TYPES[geometry_type])
        for geometry in multigeometry:
            union = union.Union(geometry)

    return union
