"""Calc_weights_catalog_proceess."""
import json
import logging
from typing import Any
from typing import Dict
from typing import Tuple

import geopandas as gpd
import pandas as pd
from pygeoapi.process.base import BaseProcessor

from gdptools.helpers import calc_weights_catalog

LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "calc_weights_catalog",
    "title": "Calculate weights for area-weighted aggregation",
    "description": "Calculate weights for OpenDAP endpoint and user-defined Features",
    "keywords": ["area-weighted intersections"],
    "links": [
        {
            "type": "text/html",
            "rel": "canonical",
            "title": "information",
            "href": "https://example.org/process",
            "hreflang": "en-CA",
        }
    ],
    "inputs": {
        "param_json": {
            "title": "param_json_string",
            "schema": {"type": "object"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "grid_json": {
            "title": "grid_json_string",
            "schema": {"type": "object"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_file": {
            "title": "shape_file_json_string",
            "schema": {"type": "object"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_crs": {
            "title": "shape_crs_string",
            "schema": {
                "type": "string",
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_poly_idx": {
            "title": "shape_poly_idx_string",
            "schema": {
                "type": "string",
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "wght_gen_proj": {
            "title": "Projection string (epsg code or proj string)",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
    },
    "outputs": {
        "weights": {
            "title": "Comma separated weights, id, i, j, weight",
            "schema": {"type": "object", "contentMediaType": "application/json"},
        }
    },
    "example": {
        "inputs": {
            "param_json": '{"id": {"11041": "terraclim"}, "grid_id": {"11041": 116.0}, "URL": {"11041": "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_terraclimate_aet_1958_CurrentYear_GLOBE.nc"}, "tiled": {"11041": ""}, "variable": {"11041": "aet"}, "varname": {"11041": "aet"}, "long_name": {"11041": "water_evaporation_amount"}, "T_name": {"11041": "time"}, "duration": {"11041": "1958-01-01/2020-12-01"}, "interval": {"11041": "1 months"}, "nT": {"11041": 756.0}, "units": {"11041": "mm"}, "model": {"11041": null}, "ensemble": {"11041": null}, "scenario": {"11041": "total"}}',  # noqa
            "grid_json": '{"grid_id": {"19": 116.0}, "X_name": {"19": "lon"}, "Y_name": {"19": "lat"}, "X1": {"19": -179.9792}, "Xn": {"19": 179.9792}, "Y1": {"19": 89.9792}, "Yn": {"19": -89.9792}, "resX": {"19": 0.0417}, "resY": {"19": 0.0417}, "ncols": {"19": 8640}, "nrows": {"19": 4320}, "proj": {"19": "+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs"}, "toptobottom": {"19": 0.0}, "tile": {"19": null}, "grid.id": {"19": null}}',  # noqa
            "shape_file": '{"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"id": 1, "poly_idx": "1"}, "geometry": {"type": "Polygon", "coordinates": [[[-70.60141212297273, 41.9262774500321], [-70.57199544021768, 41.91303994279233], [-70.5867037815952, 41.87626908934851], [-70.61906213262577, 41.889506596588284], [-70.60141212297273, 41.9262774500321]]]}}]}',  # noqa
            "shape_crs": "4326",
            "shape_poly_idx": "poly_idx",
            "wght_gen_proj": "6931",
        }
    },
}


class GDPCalcWeightsCatalogProcessor(BaseProcessor):  # type: ignore
    """Generate weights for grid-to-poly aggregation."""

    def __init__(self, processor_def: dict[str, Any]):
        """Initialize Processor.

        Args:
            processor_def (_type_): _description_
        """
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
        """Execute calc_weights_catalog web service."""
        pjson = str(data["param_json"])
        gjson = str(data["grid_json"])
        shpfile = str(data["shape_file"])
        shp_crs = str(data["shape_crs"])
        shp_poly_idx = str(data["shape_poly_idx"])
        wght_gen_proj = str(data["wght_gen_proj"])

        print(f"param_json: {pjson}  type: {type(pjson)}\n")
        print(f"grid_json: {gjson} type: {type(gjson)}\n")
        print(f"shp_file: {shpfile} type: {type(shpfile)}\n")
        print(f"shp_poly_idx: {shp_poly_idx} type: {type(shp_poly_idx)}\n")
        print(f"wght_gen_proj: {wght_gen_proj} type: {type(wght_gen_proj)}\n")

        param_json = pd.DataFrame.from_dict(json.loads(pjson))
        grid_json = pd.DataFrame.from_dict(json.loads(gjson))
        shp_file = gpd.GeoDataFrame.from_features(json.loads(shpfile))
        shp_file.set_crs(shp_crs, inplace=True)

        print(f"param_json: {param_json}  type: {type(param_json)}\n")
        print(f"grid_json: {grid_json} type: {type(grid_json)}\n")
        print(f"shp_file: {shp_file} type: {type(shp_file)}\n")

        wght = calc_weights_catalog(
            params_json=param_json,
            grid_json=grid_json,
            shp_file=shp_file,
            shp_poly_idx=shp_poly_idx,
            wght_gen_proj=wght_gen_proj,
        )

        return "application/json", json.loads(wght.to_json())

    def __repr__(self):  # type: ignore
        """Return representation."""
        return "<GDPCalcWeightsCatalogProcessor> {}".format(self.name)
