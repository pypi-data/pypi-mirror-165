# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:22:18 2022

@author: chris.kerklaan
"""
import tempfile
from osgeo import ogr
import logging
import threedi_raster_edits as tre

logger = logging.getLogger(__name__)
from threedi_raster_edits.utils.dependencies import DEPENDENCIES

# Third-party imports
if DEPENDENCIES.threedigrid_builder.installed:
    import threedigrid_builder

    def make_grid(model, existing_sqlite_path=None):

        if model.mode == "read":
            sqlite_path = model.path
        else:
            tempdir = tempfile.TemporaryDirectory()
            temp = tempdir.name
            sqlite_path = temp + "/model.sqlite"
            model.write(sqlite_path, rasters=True)

        dem_path = temp + f"/{model._get_raster_files['dem_file']}"
        grid = threedigrid_builder.make_grid(sqlite_path, dem_path)

        grid_group = tre.VectorGroup.from_scratch("grid")
        geometry_fields = ["cells", "lines", "nodes"]
        for grid_field in geometry_fields:
            logger.info(f" Adding {grid_field} to grid.")
            grid_part = grid[grid_field]

            sample_geometry = ogr.CreateGeometryFromWkb(grid_part["geometry"][0])
            sample_geometry_type = sample_geometry.GetGeometryType()

            python_types = {}
            grid_vector = tre.Vector.from_scratch(
                grid_field, sample_geometry_type, tre.Raster(dem_path).epsg
            )
            for field in grid_part:
                if field != "geometry":
                    sample = grid_part[field][0]
                    python_type = getattr(sample, "tolist", lambda: sample)()
                    grid_vector.add_field(field, type(python_type))
                    python_types[field] = type(python_type)

            for i in grid_part["id"]:
                i = i - 1
                items = {}
                for field in grid_part:
                    if field != "geometry":
                        items[field] = python_types[field](grid_part[field][i])

                geometry = ogr.CreateGeometryFromWkb(grid_part["geometry"][i])
                grid_vector.add(fid=i, geometry=geometry, **items)

            grid_group.add(grid_vector, grid_field)

        if model.mode != "read":
            tempdir.cleanup()

        return grid_group
