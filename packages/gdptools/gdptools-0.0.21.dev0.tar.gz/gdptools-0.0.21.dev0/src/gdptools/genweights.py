"""Function to generate weights for area-weighted poly-to-poly mapping."""
from typing import Any
from typing import Union

import geopandas as gpd
import pandas as pd
import xarray as xr

from gdptools.ancillary import _get_cells_poly
from gdptools.helpers import generate_weights

# from gdptools.helpers import generate_weights2


def calc_weights(
    x_coord: str,
    y_coord: str,
    var: str,
    data_file: str,
    data_crs: str,
    shp_file: Union[str, gpd.GeoDataFrame],
    shp_crs: str,
    whgt_gen_file: str,
    wght_gen_crs: Any,
) -> bool:
    """Calculate weights for poly-to-poly area weighted mapping.

    Args:
        x_coord (str): _description_
        y_coord (str): _description_
        var (str): _description_
        data_file (str): _description_
        data_crs (str): _description_
        shp_file (str): _description_
        shp_crs (str): _description_
        whgt_gen_file (str): _description_
        wght_gen_crs (Any): _description_

    Returns:
        bool: _description_
    """
    data = xr.open_dataset(data_file)  # type: ignore
    gdf_grid = _get_cells_poly(data, x=x_coord, y=y_coord, var=var, crs_in=data_crs)

    # gdf_grid = gpd.GeoDataFrame.from_features(grid_poly)

    if isinstance(shp_file, str):
        gdf_in = gpd.read_file(shp_file)
    else:
        gdf_in = shp_file.copy()
    poly_idx = gdf_in.columns[0]

    wght_gen = generate_weights(
        poly=gdf_in,
        poly_idx=poly_idx,
        grid_cells=gdf_grid,
        filename=whgt_gen_file,
        wght_gen_crs=wght_gen_crs,
    )
    if isinstance(wght_gen, pd.DataFrame):
        success = True
    else:
        success = False
    return success
