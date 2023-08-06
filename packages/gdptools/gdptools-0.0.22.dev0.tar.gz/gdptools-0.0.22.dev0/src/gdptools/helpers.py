"""Primary functions for poly-to-poly area-weighted mapping."""
from __future__ import annotations

import logging
import sys
import time
from collections import defaultdict
from pathlib import Path
from types import MappingProxyType
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import geopandas as gpd
import netCDF4
import numpy as np
import numpy.typing as npt
import pandas as pd
import pyproj
import xarray as xr
from metpy.units import units as mpunits
from pygeos import GEOSException
from shapely.geometry import box
from shapely.geometry import Point
from shapely.geometry import Polygon

from gdptools.ancillary import _check_for_intersection
from gdptools.ancillary import _get_cells_poly
from gdptools.ancillary import _get_crs
from gdptools.ancillary import _get_data_via_catalog
from gdptools.ancillary import _get_print_on
from gdptools.ancillary import _get_shp_file
from gdptools.ancillary import _get_wieght_df
from gdptools.ancillary import _quadrat_cut_geometry
from gdptools.ancillary import _read_shp_file
from gdptools.gdp_data_class import CatGrids
from gdptools.gdp_data_class import CatParams
from gdptools.stats import get_average
from gdptools.stats import get_average_wtime
from gdptools.stats import get_ma_average
from gdptools.stats import get_ma_average_wtime

# from numba import jit

logger = logging.getLogger(__name__)


def get_cells_poly_2d(
    xr_a: xr.Dataset, lon_str: str, lat_str: str, in_crs: Any
) -> gpd.GeoDataFrame:
    """Get cell polygons associated with 2d lat/lon coordinates.

    Args:
        xr_a (xr.Dataset): _description_
        lon_str (str): _description_
        lat_str (str): _description_
        in_crs (Any): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    lon = xr_a[lon_str]
    lat = xr_a[lat_str]
    count = 0
    poly = []
    lon_n = [
        lon[i, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_jm1 = [
        lon[i, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1_jm1 = [
        lon[i + 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1 = [
        lon[i + 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1_jp1 = [
        lon[i + 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_jp1 = [
        lon[i, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1_jp1 = [
        lon[i - 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1 = [
        lon[i - 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1_jm1 = [
        lon[i - 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]

    lat_n = [
        lat[i, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_jm1 = [
        lat[i, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1_jm1 = [
        lat[i + 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1 = [
        lat[i + 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1_jp1 = [
        lat[i + 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_jp1 = [
        lat[i, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1_jp1 = [
        lat[i - 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1 = [
        lat[i - 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1_jm1 = [
        lat[i - 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]

    # print(len(lon_n), len(lat_n), type(lon_n), np.shape(lon_n))
    numcells = len(lon_n)
    index = np.array(range(numcells))
    i_index = np.empty(numcells)
    j_index = np.empty(numcells)
    count = 0
    for i in range(1, lon.shape[0] - 1):
        for j in range(1, lon.shape[1] - 1):
            i_index[count] = i
            j_index[count] = j
            count += 1

    tpoly_1_lon = [
        [lon_n[i], lon_jm1[i], lon_ip1_jm1[i], lon_ip1[i]] for i in range(numcells)
    ]
    tpoly_1_lat = [
        [lat_n[i], lat_jm1[i], lat_ip1_jm1[i], lat_ip1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_1_lon), tpoly_1_lon[0])
    newp = [Polygon(zip(tpoly_1_lon[i], tpoly_1_lat[i])) for i in range(numcells)]
    p1 = [p.centroid for p in newp]
    # print(type(newp), newp[0], len(p1))

    tpoly_2_lon = [
        [lon_n[i], lon_ip1[i], lon_ip1_jp1[i], lon_jp1[i]] for i in range(numcells)
    ]
    tpoly_2_lat = [
        [lat_n[i], lat_ip1[i], lat_ip1_jp1[i], lat_jp1[i]] for i in range(numcells)
    ]
    print(len(tpoly_2_lon), tpoly_2_lon[0])
    newp = [Polygon(zip(tpoly_2_lon[i], tpoly_2_lat[i])) for i in range(numcells)]
    p2 = [p.centroid for p in newp]

    tpoly_3_lon = [
        [lon_n[i], lon_jp1[i], lon_im1_jp1[i], lon_im1[i]] for i in range(numcells)
    ]
    tpoly_3_lat = [
        [lat_n[i], lat_jp1[i], lat_im1_jp1[i], lat_im1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [Polygon(zip(tpoly_3_lon[i], tpoly_3_lat[i])) for i in range(numcells)]
    p3 = [p.centroid for p in newp]

    tpoly_4_lon = [
        [lon_n[i], lon_im1[i], lon_im1_jm1[i], lon_jm1[i]] for i in range(numcells)
    ]
    tpoly_4_lat = [
        [lat_n[i], lat_im1[i], lat_im1_jm1[i], lat_jm1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [Polygon(zip(tpoly_4_lon[i], tpoly_4_lat[i])) for i in range(numcells)]
    p4 = [p.centroid for p in newp]

    lon_point_list = [[p1[i].x, p2[i].x, p3[i].x, p4[i].x] for i in range(numcells)]
    lat_point_list = [[p1[i].y, p2[i].y, p3[i].y, p4[i].y] for i in range(numcells)]

    poly = [Polygon(zip(lon_point_list[i], lat_point_list[i])) for i in range(numcells)]

    df = pd.DataFrame({"i_index": i_index, "j_index": j_index})
    # tpoly_1 = [Polygon(x) for x in newp]
    # p1 = tpoly_1.centroid
    return gpd.GeoDataFrame(df, index=index, geometry=poly, crs=in_crs)


def generate_feature_weight(
    spind: gpd.GeoSeries.sindex,
    grid_cells: gpd.GeoDataFrame,
    row: gpd.GeoDataFrame,
    poly_idx: str,
    row_index: int,
) -> Tuple[List[str], List[int], List[int], List[float]]:
    """Generate feature weights.

       Uses original method that intersects all cells whithin bounding box.

    Args:
        spind (gpd.GeoSeries.sindex): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        row (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        row_index (int): _description_

    Returns:
        Tuple[List[str], List[int], List[int], List[float]]: _description_
    """
    hru_area = row["geometry"].area
    try:
        possible_matches_index = list(spind.query(row["geometry"].values[0]))
    except AttributeError:
        print(f"User feature Attribute error index: {row_index} has an error")

    if possible_matches_index:
        possible_matches = grid_cells.iloc[possible_matches_index]
        try:
            precise_matches = possible_matches[
                possible_matches.intersects(row["geometry"].values[0])
            ]
        except GEOSException:
            print(f"User feature GEOSException error: index={row_index}")
        except TypeError:
            print(f"User feature Type error: index={row_index}")
        if len(precise_matches) != 0:

            res_intersection = row.overlay(precise_matches, how="intersection")
            wghts = res_intersection.geometry.area.values / hru_area.values[0]
            i_index = res_intersection["i_index"].astype(int).to_list()
            j_index = res_intersection["j_index"].astype(int).to_list()

    else:
        print("no intersection: ", row_index, flush=True)
    num_cells = len(wghts)
    p_index = [row[poly_idx].values[0]] * num_cells
    return p_index, i_index, j_index, wghts


def generate_feature_weight2(
    spind: gpd.GeoSeries.sindex,
    grid_cells: gpd.GeoDataFrame,
    row: gpd.GeoDataFrame,
    poly_idx: str,
    row_index: int,
    quadrat_width: Any,
) -> Tuple[List[str], List[int], List[int], List[float]]:
    """Generate feature weights.

       Calcs individually points within and crossing, only calculates intersections
       on points crossing.

    Args:
        spind (gpd.GeoSeries.sindex): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        row (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        row_index (int): _description_
        quadrat_width(Any): _description_

    Returns:
        Tuple[List[str], List[int], List[int], List[float]]: _description_
    """
    hru_area = row["geometry"].area
    multipoly = _quadrat_cut_geometry(
        row["geometry"].values[0], quadrat_width=quadrat_width
    )
    geoms = set()
    precise_matches = []
    # print(f'Number of sub-polygons {len(multipoly.geoms)}')

    for spindex, poly in enumerate(multipoly.geoms):

        try:
            possible_matches_index = list(spind.intersection(poly.bounds))
        except AttributeError:
            print(
                f"User feature Attribute error index: {row_index} \
                    subpoly_index: {spindex} has an error"
            )

        if possible_matches_index:
            possible_matches = grid_cells.iloc[possible_matches_index]
            try:
                precise_matches = possible_matches[possible_matches.intersects(poly)]
            except GEOSException:
                print(
                    f"User feature GEOSException error: index={row_index}, \
                    sub_poly={spindex}"
                )
            except TypeError:
                print(
                    f"User feature Type error: index={row_index}, \
                    sub_poly={spindex}"
                )
            geoms.update(precise_matches.index)
        else:
            print("no intersection: ", row_index, spindex, flush=True)
    i_index = []
    j_index = []
    p_index = []
    wghts = []
    if len(precise_matches) != 0:
        res_intersection = row.overlay(grid_cells.iloc[list(geoms)], how="intersection")
        wghts.extend(res_intersection.geometry.area.values / hru_area.values[0])
        i_index.extend(res_intersection["i_index"].astype(int).to_list())
        j_index.extend(res_intersection["j_index"].astype(int).to_list())

    num_cells = len(wghts)
    p_index = [row[poly_idx].values[0]] * num_cells
    return p_index, i_index, j_index, wghts


def generate_weights2(
    poly: gpd.GeoDataFrame,
    poly_idx: str,
    grid_cells: gpd.GeoDataFrame,
    wght_gen_crs: str,
    filename: Optional[str] = None,
    verbose: Optional[bool] = False,
) -> pd.DataFrame:
    """Generate weights for aggragations of poly-to-poly mapping.

    Args:
        poly (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        wght_gen_crs (str): _description_
        filename (Optional[str], optional): _description_. Defaults to None.
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        pd.DataFrame: _description_
    """
    # check if poly_idx in in poly
    if poly_idx not in poly.columns:
        error_string = (
            f"Error: poly_idx ({poly_idx}) is not found in the poly ({poly.columns})"
        )
        raise ValueError(error_string)

    if not poly.crs:
        error_string = f"polygons don't contain a valid crs: {poly.crs}"
        raise ValueError(error_string)

    if not grid_cells.crs:
        error_string = f"grid_cells don't contain a valid crs: {grid_cells.crs}"
        raise ValueError(error_string)

    grid_out_crs = _get_crs(wght_gen_crs)

    start = time.perf_counter()
    grid_cells.to_crs(grid_out_crs, inplace=True)
    gc_meanarea = grid_cells.area.mean()

    npoly = poly.to_crs(grid_out_crs)
    end = time.perf_counter()
    print(
        f"Reprojecting to epsg:{wght_gen_crs} finished in {round(end-start, 2)}"
        " second(s)"
    )

    start = time.perf_counter()
    spatial_index = grid_cells.sindex
    # print(type(spatial_index))
    end = time.perf_counter()
    print(f"Spatial index generations finished in {round(end-start, 2)} second(s)")
    start = time.perf_counter()

    numrows = len(npoly.index)
    print_on = _get_print_on(numrows)

    # in order, i_index, j_index, poly_index, weight values
    i_index = []
    j_index = []
    p_index = []
    wghts = []

    for index, row in npoly.iterrows():
        tstart = time.perf_counter()
        tp, ti, tj, tw = generate_feature_weight2(
            spind=spatial_index,
            grid_cells=grid_cells,
            row=npoly.iloc[[index]],
            poly_idx=poly_idx,
            row_index=index,
            quadrat_width=np.sqrt(10.0 * gc_meanarea),
        )
        tend = time.perf_counter()
        if verbose:
            print(f"    feature: {index}, {tend - tstart:0.4f} seconds")
        p_index.extend(tp)
        i_index.extend(ti)
        j_index.extend(tj)
        wghts.extend(tw)

        if index % print_on == 0:
            print(
                f"Calculating weights index: {index} and for feature {row[poly_idx]}",
                flush=True,
            )

    wght_df = pd.DataFrame(
        {
            poly_idx: p_index,
            "i": i_index,
            "j": j_index,
            "wght": wghts,
        }
    )
    wght_df = wght_df.astype({"i": int, "j": int, "wght": float, poly_idx: str})
    wght_df.set_index(poly_idx, inplace=True)
    if filename:
        wght_df.to_csv(filename)
    end = time.perf_counter()
    print(f"Weight generations finished in {round(end-start, 2)} second(s)")
    return wght_df


def generate_weights(
    poly: gpd.GeoDataFrame,
    poly_idx: str,
    grid_cells: gpd.GeoDataFrame,
    wght_gen_crs: str,
    filename: Optional[str] = None,
    verbose: Optional[bool] = False,
) -> pd.DataFrame:
    """Generate weights for aggragations of poly-to-poly mapping.

    Args:
        poly (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        wght_gen_crs (str): _description_
        filename (Optional[str], optional): _description_. Defaults to None.
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        pd.DataFrame: _description_
    """
    # check if poly_idx in in poly
    if poly_idx not in poly.columns:
        error_string = (
            f"Error: poly_idx ({poly_idx}) is not found in the poly ({poly.columns})"
        )
        raise ValueError(error_string)

    if not poly.crs:
        error_string = f"polygons don't contain a valid crs: {poly.crs}"
        raise ValueError(error_string)

    if not grid_cells.crs:
        error_string = f"grid_cells don't contain a valid crs: {grid_cells.crs}"
        raise ValueError(error_string)

    grid_out_crs = _get_crs(wght_gen_crs)

    start = time.perf_counter()
    # grid_cells.set_crs(grid_in_crs, inplace=True)
    grid_cells.to_crs(grid_out_crs, inplace=True)

    npoly = poly.to_crs(grid_out_crs)
    end = time.perf_counter()
    print(
        f"Reprojecting to epsg:{wght_gen_crs} finished in {round(end-start, 2)}"
        " second(s)"
    )

    start = time.perf_counter()
    spatial_index = grid_cells.sindex
    # print(type(spatial_index))
    end = time.perf_counter()
    print(f"Spatial index generations finished in {round(end-start, 2)} second(s)")
    start = time.perf_counter()

    numrows = len(npoly.index)
    print_on = _get_print_on(numrows)

    # in order, i_index, j_index, poly_index, weight values
    i_index = []
    j_index = []
    p_index = []
    wghts = []

    # for index, row in npoly.iterrows():
    for index in np.arange(numrows):
        tstart = time.perf_counter()
        tp, ti, tj, tw = generate_feature_weight(
            spind=spatial_index,
            grid_cells=grid_cells,
            row=npoly.iloc[[index]],
            poly_idx=poly_idx,
            row_index=index,
        )
        tend = time.perf_counter()
        if verbose:
            print(f"   feature: {index}, {tend - tstart:0.4f} seconds")
        p_index.extend(tp)
        i_index.extend(ti)
        j_index.extend(tj)
        wghts.extend(tw)

        if index % print_on == 0:
            print(
                f"Calculating weights index: {index} and for \
                    feature {npoly.loc[index, poly_idx]}",
                flush=True,
            )

    wght_df = pd.DataFrame(
        {
            poly_idx: p_index,
            "i": i_index,
            "j": j_index,
            "wght": wghts,
        }
    )
    wght_df = wght_df.astype({"i": int, "j": int, "wght": float, poly_idx: str})
    wght_df.set_index(poly_idx, inplace=True)
    if filename:
        wght_df.to_csv(filename)
    end = time.perf_counter()
    print(f"Weight generations finished in {round(end-start, 2)} second(s)")
    return wght_df


def run_weights(
    var: str,
    t_name: str,
    ds: xr.Dataset,
    wght_file: Union[str, pd.DataFrame],
    shp: gpd.GeoDataFrame,
    geom_id: str,
) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Any]]:
    """Run aggregation mapping ds to shp.

    Args:
        var (str): _description_
        t_name (str): _description_
        ds (xr.Dataset): _description_
        wght_file (Union[str, pd.DataFrame]): _description_
        shp (gpd.GeoDataFrame): _description_
        geom_id (str): _description_

    Raises:
        KeyError: _description_

    Returns:
        Tuple[gpd.GeoDataFrame, npt.NDArray[Any]]: _description_
    """
    wghts = _get_wieght_df(wght_file, geom_id)

    shp.reset_index(drop=True, inplace=True)
    gdf = shp.sort_values(geom_id).dissolve(by=geom_id)

    geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
    n_geo = len(geo_index)

    print_on = _get_print_on(n_geo)
    unique_geom_ids = wghts.groupby(geom_id)
    ds_vars = list(ds.data_vars)
    if var not in ds_vars:
        raise KeyError(f"var: {var} not in ds vars: {ds_vars}")

    # nts = len(ds.coords[time].values)
    nts = ds.coords[t_name].values.size
    # try:
    native_dtype = ds[var].dtype
    # except KeyError:
    #     print(f"var: {var} not in ds vars: {ds_vars}")

    val_interp = np.empty((nts, n_geo), dtype=native_dtype)
    var_vals = ds[var].values

    # for t in np.arange(nts):
    #     # val_flat_interp = (
    #     #     ds[var].values[t, 1 : grd_shp[1] - 1, 1 : grd_shp[2] - 1].flatten()
    #     # )
    print(f"processing time for var: {var}")
    for i in np.arange(len(geo_index)):
        weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
        tw = weight_id_rows.wght.values
        i_ind = np.array(weight_id_rows.i.values)
        j_ind = np.array(weight_id_rows.j.values)

        vals = var_vals[:, i_ind, j_ind]

        # tgid = weight_id_rows.grid_ids.values
        # tmp = getaverage(val_flat_interp[tgid], tw)
        tmp = get_average_wtime(vals, tw)
        try:
            if np.isnan(tmp).any():
                val_interp[:, i] = get_ma_average_wtime(vals, tw)
            else:
                val_interp[:, i] = tmp
        except KeyError:
            val_interp[:, i] = netCDF4.default_fillvals["f8"]

        if i % print_on == 0:
            print(f"    Processing {var} for feature {geo_index[i]}", flush=True)

    # print(val_interp)
    return gdf, val_interp


def run_weights_static(
    var: str,
    da: xr.DataArray,
    wght_file: Union[str, pd.DataFrame],
    shp: gpd.GeoDataFrame,
    geom_id: str,
) -> Any:
    """Run aggregation mapping on static (no time dependency) data.

    Args:
        var (str): _description_
        da (xr.DataArray): _description_
        wght_file (Union[str, pd.DataFrame]): _description_
        shp (gpd.GeoDataFrame): _description_
        geom_id (str): _description_

    Returns:
        Any: _description_
    """
    wghts = _get_wieght_df(wght_file, geom_id)

    unique_geom_ids = wghts.groupby(geom_id)

    print(f"processing time for var: {var}")
    weight_id_rows = unique_geom_ids.get_group(str(shp.get(geom_id).values[0]))
    tw = weight_id_rows.wght.values
    i_ind = np.array(weight_id_rows.i.values)
    j_ind = np.array(weight_id_rows.j.values)

    vals = da.values[i_ind, j_ind]

    # tgid = weight_id_rows.grid_ids.values
    # tmp = getaverage(val_flat_interp[tgid], tw)
    tmp = get_average(vals, tw)
    try:
        val = get_ma_average(vals, tw) if np.isnan(tmp).any() else tmp
    except KeyError:
        val = netCDF4.default_fillvals["f8"]
    return val


def build_subset(
    bounds: npt.NDArray[np.double],
    xname: str,
    yname: str,
    tname: str,
    toptobottom: bool,
    date_min: str,
    date_max: Optional[str] = None,
) -> Dict[str, object]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        bounds (np.ndarray): _description_
        xname (str): _description_
        yname (str): _description_
        tname (str): _description_
        toptobottom (bool): _description_
        date_min (str): _description_
        date_max (Optional[str], optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    if not toptobottom:
        return (
            {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: date_min,
            }
            if date_max is None
            else {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: slice(date_min, date_max),
            }
        )

    elif date_max is None:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            tname: date_min,
        }

    else:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            tname: slice(date_min, date_max),
        }


def build_subset_tiff(
    bounds: npt.NDArray[np.double],
    xname: str,
    yname: str,
    toptobottom: bool,
    bname: str,
    band: int,
) -> Dict[str, object]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        bounds (npt.NDArray[np.double]): _description_
        xname (str): _description_
        yname (str): _description_
        toptobottom (bool): _description_
        bname (str): _description_
        band (int): _description_

    Returns:
        Dict[str, object]: _description_
    """
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    ss_dict = {}
    ss_dict = (
        {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            bname: band,
        }
        if toptobottom
        else {
            xname: slice(minx, maxx),
            yname: slice(maxy, miny),
            bname: band,
        }
    )

    return ss_dict


def calc_weights_catalog2(
    params_json: CatParams,
    grid_json: CatGrids,
    shp_file: Union[str, gpd.GeoDataFrame],
    shp_poly_idx: str,
    wght_gen_proj: Any,
    wght_gen_file: Optional[str] = None,
    verbose: Optional[bool] = False,
) -> pd.DataFrame:
    """Calculate area-intersected weights of grid to feature.

    Args:
        params_json (CatParams): _description_
        grid_json (CatGrids): _description_
        shp_file (Union[str, gpd.GeoDataFrame]): _description_
        shp_poly_idx (str): _description_
        wght_gen_proj (Any): _description_
        wght_gen_file (Optional[str], optional): _description_. Defaults to None.
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Raises:
        ValueError: _description_

    Returns:
        pd.DataFrame: _description_
    """
    # run check on intersection of shape features and gridded data
    gdf = _read_shp_file(shp_file)
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        params_json=params_json, grid_json=grid_json, gdf=gdf
    )
    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf, gdf_bounds = _get_shp_file(
        shp_file=gdf, grid_json=grid_json, is_degrees=is_degrees
    )

    ds_proj = grid_json.proj
    # only need one time step for generating weights so choose the first time from the param_cat
    date = params_json.duration.split("/")[0]

    # get sub-setted xarray dataset
    rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
    ds_ss = _get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=date,
        rotate_lon=rotate_ds,
    )
    tsrt = time.perf_counter()
    ds_ss.load()
    tend = time.perf_counter()

    print(f"loading {params_json.varname} in {tend-tsrt:0.4f} seconds")
    # get grid polygons to calculate intersection with polygon of interest - shp_file
    xname = grid_json.X_name
    yname = grid_json.Y_name
    var = params_json.variable
    gdf_grid = _get_cells_poly(ds_ss, x=xname, y=yname, var=var, crs_in=ds_proj)

    # calculate the intersection weights and generate weight_file
    # assumption is that the first column in the shp_file is the id to use for
    # calculating weights
    if shp_poly_idx not in gdf.columns[:]:
        raise ValueError(
            f"shp_poly_idx: {shp_poly_idx} not in gdf columns: {gdf.columns}"
        )
    else:
        apoly_idx = shp_poly_idx

    return generate_weights2(
        poly=gdf,
        poly_idx=apoly_idx,
        grid_cells=gdf_grid,
        filename=wght_gen_file,
        wght_gen_crs=wght_gen_proj,
        verbose=verbose,
    )


def calc_weights_catalog(
    params_json: CatParams,
    grid_json: CatGrids,
    shp_file: Union[str, gpd.GeoDataFrame],
    shp_poly_idx: str,
    wght_gen_proj: Any,
    wght_gen_file: Optional[str] = None,
    verbose: Optional[bool] = False,
) -> pd.DataFrame:
    """Calculate area-intersected weights of grid to feature.

    Args:
        params_json (CatParams): _description_
        grid_json (CatGrids): _description_
        shp_file (Union[str, gpd.GeoDataFrame]): _description_
        shp_poly_idx (str): _description_
        wght_gen_proj (Any): _description_
        wght_gen_file (Optional[str], optional): _description_. Defaults to None.
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Raises:
        ValueError: _description_

    Returns:
        pd.DataFrame: _description_
    """
    # run check on intersection of shape features and gridded data
    gdf = _read_shp_file(shp_file)
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        params_json=params_json, grid_json=grid_json, gdf=gdf
    )

    gdf, gdf_bounds = _get_shp_file(
        shp_file=gdf, grid_json=grid_json, is_degrees=is_degrees
    )

    # ds_URL = params_json.URL.values[0]
    ds_proj = grid_json.proj
    # only need one time step for generating weights so choose the first time from the param_cat
    date = params_json.duration.split("/")[0]

    # get sub-setted xarray dataset
    rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
    ds_ss = _get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=date,
        rotate_lon=rotate_ds,
    )
    tsrt = time.perf_counter()
    ds_ss.load()
    tend = time.perf_counter()
    print(f"loading {params_json.varname} in {tend-tsrt:0.4f} seconds")
    # get grid polygons to calculate intersection with polygon of interest - shp_file
    xname = grid_json.X_name
    yname = grid_json.Y_name
    var = params_json.variable
    gdf_grid = _get_cells_poly(ds_ss, x=xname, y=yname, var=var, crs_in=ds_proj)

    # calculate the intersection weights and generate weight_file
    # assumption is that the first column in the shp_file is the id to use for
    # calculating weights
    if shp_poly_idx not in gdf.columns[:]:
        raise ValueError(
            f"shp_poly_idx: {shp_poly_idx} not in gdf columns: {gdf.columns}"
        )
    else:
        apoly_idx = shp_poly_idx

    return generate_weights(
        poly=gdf,
        poly_idx=apoly_idx,
        grid_cells=gdf_grid,
        filename=wght_gen_file,
        wght_gen_crs=wght_gen_proj,
        verbose=verbose,
    )


def calc_weights_catalog_pershp(
    params_json: CatParams,
    grid_json: CatGrids,
    shp_file: Union[str, gpd.GeoDataFrame],
    shp_poly_idx: str,
    wght_gen_proj: Any,
    verbose: Optional[bool] = False,
) -> pd.DataFrame:
    """Calculate area-intersected weights of grid to feature.

    Args:
        params_json (CatParams): _description_
        grid_json (CatGrids): _description_
        shp_file (Union[str, gpd.GeoDataFrame]): _description_
        shp_poly_idx (str): _description_
        wght_gen_proj (Any): _description_
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Raises:
        ValueError: _description_

    Returns:
        pd.DataFrame: _description_
    """
    # run check on intersection of shape features and gridded data
    gdf = _read_shp_file(shp_file)
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        params_json=params_json, grid_json=grid_json, gdf=gdf
    )
    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf, gdf_bounds = _get_shp_file(
        shp_file=gdf, grid_json=grid_json, is_degrees=is_degrees
    )

    ds_proj = grid_json.proj
    # only need one time step for generating weights so choose the first time from the param_cat
    date = params_json.duration.split("/")[0]

    # get sub-setted xarray dataset
    rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
    ds_ss = _get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=date,
        rotate_lon=rotate_ds,
    )
    tsrt = time.perf_counter()
    ds_ss.load()
    tend = time.perf_counter()
    print(f"loading {params_json.varname} in {tend-tsrt:0.4f} seconds")
    # get grid polygons to calculate intersection with polygon of interest - shp_file
    xname = grid_json.X_name
    yname = grid_json.Y_name
    var = params_json.variable
    gdf_grid = _get_cells_poly(ds_ss, x=xname, y=yname, var=var, crs_in=ds_proj)

    # calculate the intersection weights and generate weight_file
    # assumption is that the first column in the shp_file is the id to use for
    # calculating weights
    if shp_poly_idx not in gdf.columns[:]:
        raise ValueError(
            f"shp_poly_idx: {shp_poly_idx} not in gdf columns: {gdf.columns}"
        )
    else:
        apoly_idx = shp_poly_idx

    return generate_weights(
        poly=shp_file,
        poly_idx=apoly_idx,
        grid_cells=gdf_grid,
        wght_gen_crs=wght_gen_proj,
        verbose=verbose,
    )


def run_weights_catalog_pershp(
    params_json: CatParams,
    grid_json: CatGrids,
    wght_file: pd.DataFrame,
    shp: gpd.GeoDataFrame,
    poly_idx: str,
    begin_date: str,
    end_date: str,
) -> Tuple[gpd.GeoDataFrame, npt.NDArray[np.double]]:
    """Run area-weighted aggragation of grid to feature.

    Args:
        params_json (CatParams): _description_
        grid_json (CatGrids): _description_
        wght_file (pd.DataFrame): _description_
        shp (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        begin_date (str): _description_
        end_date (str): _description_

    Returns:
        Union[gpd.GeoDataFrame, np.ndarray]: _description_
    """
    wghts = _get_wieght_df(wght_file, poly_idx)

    # read shapefile, calculate total_bounds, and project to grid's projection
    shp.to_crs(grid_json.proj, inplace=True)
    bbox = box(*shp.total_bounds)
    b_buf = max(grid_json.resX, grid_json.resY)
    gdf_bounds = bbox.buffer(2 * b_buf).bounds
    # gdf_bounds = shp.total_bounds

    # get sub-setted xarray dataset
    ds = _get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=begin_date,
        end_date=end_date,
    )
    tsrt = time.perf_counter()
    ds.load()
    tend = time.perf_counter()
    print(f"loading {params_json.varname} in {tend-tsrt:0.4f} seconds")
    # shp.reset_index(drop=True, inplace=True)
    gdf1 = shp.dissolve(by=poly_idx)

    geo_index = np.asarray(gdf1.index, dtype=type(gdf1.index.values[0]))
    n_geo = len(geo_index)

    print_on = _get_print_on(n_geo)
    unique_geom_ids = wghts.groupby(poly_idx)

    var = params_json.varname
    t_name = params_json.T_name
    ds_vars = list(ds.data_vars)
    # if var not in ds_vars:
    #     raise KeyError(f"var: {var} not in ds vars: {ds_vars}")
    #     return None, None

    nts = len(ds.coords[t_name].values)
    try:
        native_dtype = ds[var].dtype
    except KeyError:
        print(f"var: {var} not in ds vars: {ds_vars}")
    val_interp = np.empty(nts, dtype=native_dtype)

    var_vals = ds[var].values
    i = 0

    weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
    tw = weight_id_rows.wght.values
    i_ind = np.array(weight_id_rows.i.values)
    j_ind = np.array(weight_id_rows.j.values)

    vals = var_vals[:, i_ind, j_ind]
    tmp = get_average_wtime(vals, tw)
    try:
        val_interp[:] = get_ma_average_wtime(vals, tw) if np.isnan(tmp).any() else tmp
    except KeyError:
        val_interp[:] = netCDF4.default_fillvals["f8"]

    if i % print_on == 0:
        print(f"    Processing {var} for feature {geo_index[i]}", flush=True)

    return gdf1, val_interp


def run_weights_catalog(
    params_json: CatParams,
    grid_json: CatGrids,
    wght_file: Union[str, pd.DataFrame],
    shp_file: Union[str, gpd.GeoDataFrame],
    shp_poly_idx: str,
    begin_date: str,
    end_date: str,
) -> Tuple[gpd.GeoDataFrame, npt.NDArray[np.double]]:
    """Run area-weighted aggragation of grid to feature.

    Args:
        params_json (CatParams): _description_
        grid_json (CatGrids): _description_
        wght_file (Union[str, pd.DataFrame]): _description_
        shp_file (Union[str, gpd.GeoDataFrame]): _description_
        shp_poly_idx (str): _description_
        begin_date (str): _description_
        end_date (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        Tuple[gpd.GeoDataFrame, npt.NDArray[np.double]]: _description_
    """
    # run check on intersection of shape features and gridded data
    gdf = _read_shp_file(shp_file)
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        params_json=params_json, grid_json=grid_json, gdf=gdf
    )
    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf, gdf_bounds = _get_shp_file(
        shp_file=gdf, grid_json=grid_json, is_degrees=is_degrees
    )

    poly_idx = shp_poly_idx
    if poly_idx not in gdf.columns[:]:
        raise ValueError(
            (f"shp_poly_idx: {poly_idx}" " not in gdf columns: {gdf.columns}")
        )

    wghts = _get_wieght_df(wght_file, poly_idx)

    # get sub-setted xarray dataset
    rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
    da = _get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=begin_date,
        end_date=end_date,
        rotate_lon=rotate_ds,
    )
    tsrt = time.perf_counter()
    da.load()
    tend = time.perf_counter()
    print(f"loading {params_json.varname} in {tend-tsrt:0.4f} seconds")

    gdf.reset_index(drop=True, inplace=True)
    gdf = gdf.sort_values(poly_idx).dissolve(by=poly_idx)

    geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
    n_geo = len(geo_index)

    print_on = _get_print_on(n_geo)
    unique_geom_ids = wghts.groupby(poly_idx)

    var = params_json.varname
    t_name = params_json.T_name

    nts = len(da.coords[t_name].values)

    native_dtype = da.dtype
    val_interp = np.empty((nts, n_geo), dtype=native_dtype)

    for i in np.arange(len(geo_index)):
        weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
        tw = weight_id_rows.wght.values
        i_ind = np.array(weight_id_rows.i.values)
        j_ind = np.array(weight_id_rows.j.values)

        tmp = get_average_wtime(da.values[:, i_ind, j_ind], tw)

        try:
            if np.isnan(tmp[:]).any():
                val_interp[:, i] = get_ma_average_wtime(da.values[:, i_ind, j_ind], tw)
            else:
                val_interp[:, i] = tmp
        except KeyError:
            val_interp[:, i] = netCDF4.default_fillvals["f8"]

        if i % print_on == 0:
            print(f"    Processing {var} for feature {geo_index[i]}", flush=True)

    return gdf, val_interp


def get_data_subset_catalog(
    params_json: CatParams,
    grid_json: CatGrids,
    shp_file: Union[str, gpd.GeoDataFrame],
    begin_date: str,
    end_date: str,
) -> xr.DataArray:
    """Get xarray subset data.

    Args:
        params_json (CatParams): _description_
        grid_json (CatGrids): _description_
        shp_file (Union[str, gpd.GeoDataFrame]): _description_
        begin_date (str): _description_
        end_date (str): _description_

    Returns:
        xr.Dataset: _description_
    """
    # run check on intersection of shape features and gridded data
    gdf = _read_shp_file(shp_file)
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        params_json=params_json, grid_json=grid_json, gdf=gdf
    )

    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf, gdf_bounds = _get_shp_file(
        shp_file=gdf, grid_json=grid_json, is_degrees=is_degrees
    )

    rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
    return _get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=begin_date,
        end_date=end_date,
        rotate_lon=rotate_ds,
    )


def finalize(
    gdf: List[gpd.GeoDataFrame],
    vals: List[npt.NDArray[np.double]],
    p_opath: str,
    start_date: str,
    time_interval: int,
    time_type: str,
    var_dict: Dict[str, Dict[str, Any]],
    prefix: Optional[str] = None,
    use_opt_dict: Optional[bool] = False,
    work_dict: Optional[Dict[str, Dict[str, Any]]] = MappingProxyType(
        {"str": {"str": "arg"}}
    ),
) -> bool:
    """Write netCDF.

    Args:
        gdf (List[gpd.GeoDataFrame]): _description_
        vals (List[npt.NDArray[np.double]]): _description_
        p_opath (str): _description_
        start_date (str): _description_
        time_interval (int): _description_
        time_type (str): _description_
        var_dict (Dict[str, Dict[str, Any]]): _description_
        prefix (Optional[str], optional): _description_. Defaults to None.
        use_opt_dict (Optional[bool], optional): _description_. Defaults to False.
        work_dict (_type_, optional): _description_.
            Defaults to MappingProxyType({"str": {"str": "arg"}}).

    Returns:
        bool: _description_
    """
    if prefix is None:
        prefix = "t_"
    pd_offset_conv: Dict[str, str] = {
        "years": "Y",
        "months": "M",
        "days": "D",
        "hours": "H",
    }
    uconv = False

    print(
        len(gdf),
        type(gdf[0]),
        gdf[0].index.name,
    )
    poly_idx = gdf[0].index.name
    time_varname = "time"
    lat_varname = "lat"
    lon_varname = "lon"
    num_ts = vals[0].shape[1]
    times = pd.date_range(
        start_date,
        freq=str(time_interval) + str(pd_offset_conv.get(time_type)),
        periods=num_ts,
    )

    if use_opt_dict:
        work_dict = defaultdict(lambda: None, work_dict)  # type: ignore
        wd_dims = defaultdict(lambda: None, work_dict["dims"])
        wd_feature = defaultdict(lambda: None, work_dict["feature"])
        wd_lon = defaultdict(lambda: None, work_dict["lon"])
        wd_lat = defaultdict(lambda: None, work_dict["lat"])

        if wd_dims["time"]:
            time_varname = wd_dims["time"]
        if wd_dims["x"]:
            lon_varname = wd_dims["x"]
        if wd_dims["y"]:
            lat_varname = wd_dims["y"]
        if wd_dims["feature"]:
            poly_idx = wd_dims["feature"]

    opath = Path(p_opath)
    if opath.exists():
        print("output path exists", flush=True)
    else:
        sys.exit(f"Output Path does not exist: {opath} - EXITING")

    fname = opath / (prefix + ".nc")
    ncfile = netCDF4.Dataset(fname, mode="w", format="NETCDF4")

    def getxy(pt: Point) -> Tuple[np.double, np.double]:
        """Return x y components of point."""
        return pt.x, pt.y

    centroidseries = gdf[0].geometry.centroid

    tlon, tlat = [list(t) for t in zip(*map(getxy, centroidseries))]

    # Global Attributes
    ncfile.Conventions = "CF-1.8"
    ncfile.featureType = "timeSeries"
    ncfile.history = ""

    feature_dim = len(gdf[0].index)
    # Create dimensions

    print(poly_idx, gdf[0].index)
    ncfile.createDimension(poly_idx, size=feature_dim)  # hru_id
    ncfile.createDimension(
        time_varname, size=None
    )  # unlimited axis (can be appended to).

    # Create Variables
    crs_cf = pyproj.CRS(gdf[0].crs).to_cf()
    crs = ncfile.createVariable("crs", np.int32, ())
    crs.setncatts(crs_cf)
    # for key, val in crs_cf.items():
    #     crs[key] = val
    time = ncfile.createVariable(time_varname, "f4", (time_varname,))
    time.long_name = time_varname
    time.standard_name = time_varname
    time.units = "days since " + start_date
    time.calendar = "standard"
    time[:] = netCDF4.date2num(times.to_pydatetime(), time.units, calendar="standard")

    long_name = "feature id"
    if use_opt_dict:
        if wd_feature["long_name"]:
            long_name = wd_feature["long_name"]

    feature = ncfile.createVariable(poly_idx, "i8", (poly_idx,))
    feature.cf_role = "timeseries_id"
    feature.long_name = long_name
    feature[:] = gdf[0].index.values.astype("i8")

    long_name = "Latitude of feature centroid"
    units = "degree_north"
    standard_name = "latitude"
    if use_opt_dict:
        if wd_lat["long_name"]:
            long_name = wd_lat["long_name"]
        if wd_lat["units"]:
            units = wd_lat["units"]
        if wd_lat["standard_name"]:
            standard_name = wd_lat["standard_name"]

    lat = ncfile.createVariable("lat", np.dtype(np.float32).char, (poly_idx,))

    lat.long_name = long_name
    lat.units = units
    lat.standard_name = standard_name
    lat.axis = "Y"
    lat[:] = tlat

    long_name = "Longitude of feature centroid"
    units = "degree_east"
    standard_name = "longitude"
    if use_opt_dict:
        if wd_lon["long_name"]:
            long_name = wd_lon["long_name"]
        if wd_lon["units"]:
            units = wd_lon["units"]
        if wd_lon["standard_name"]:
            standard_name = wd_lon["standard_name"]
    lon = ncfile.createVariable("lon", np.dtype(np.float32).char, (poly_idx,))
    lon.long_name = long_name
    lon.units = units
    lon.standard_name = standard_name
    lon.axis = "X"
    lon[:] = tlon

    for index, key in enumerate(var_dict):
        print(f"Processing: {key}")
        uvar: pd.DataFrame = var_dict.get(key)
        long_name = uvar.get("long_name")
        standard_name = uvar.get("standard_name")
        units = uvar.get("units")
        varname = uvar.get("varname")
        convert_unit = ""
        uconv = False
        if use_opt_dict & (key in [*work_dict]):
            try:
                dict_var = defaultdict(lambda: None, work_dict.get(key))  # type: ignore
                if dict_var["long_name"]:
                    long_name = dict_var["long_name"]
                if dict_var["units"]:
                    units = dict_var["units"]
                if dict_var["standard_name"]:
                    standard_name = dict_var["standard_name"]
                if dict_var["convert"]:
                    uconv = True
                if dict_var["native_unit"]:
                    units = dict_var["native_unit"]
                if dict_var["convert_unit"]:
                    convert_unit = dict_var["convert_unit"]
            except KeyError:
                print(
                    f"Error: Key - {key} not found in work_dict"
                    "will resort to default values"
                )

        vartype = vals[index].dtype
        ncvar = ncfile.createVariable(
            varname,
            vartype,
            (time_varname, poly_idx),
            fill_value=netCDF4.default_fillvals["f8"],
        )
        ncvar.grid_mapping = "crs"
        ncvar.coordinates = f"{time_varname} {lat_varname} {lon_varname}"
        ncvar.long_name = long_name
        ncvar.standard_name = standard_name
        ncvar.units = units
        if uconv:
            tmp = vals[index][:, :] * mpunits(units)
            tmp.ito(convert_unit)
            ncvar[:, :] = tmp[:, :]
            ncvar.units = convert_unit
        else:
            ncvar[:, :] = vals[index][:, :]

    ncfile.close()

    return True
