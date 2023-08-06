"""Ancillary function to support core functions in helper.py."""
from __future__ import annotations

import json
import logging
import re
import sys
import time
import warnings
from collections.abc import Iterator
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import shapely
import xarray as xr
from pyproj import CRS
from shapely.geometry import box
from shapely.geometry import LineString
from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
from shapely.ops import split

from gdptools.gdp_data_class import CatGrids
from gdptools.gdp_data_class import CatParams


logger = logging.getLogger(__name__)


def _get_print_on(numrows: int) -> int:
    """Return an interval to print progress of run_weights() function.

    Args:
        numrows (int): Number of rows: as in number of polygons

    Returns:
        int: Reasonable interval to print progress statements. Prints at about 10%
    """
    if numrows <= 10:
        print_on = 1
    elif numrows <= 100:
        print_on = 10
    elif numrows <= 1000:
        print_on = 100
    elif numrows <= 10000:
        print_on = 1000
    elif numrows <= 100000:
        print_on = 10000
    else:
        print_on = 50000
    return int(print_on)


def _get_crs(crs_in: Any) -> CRS:
    """Return pyproj.CRS given integer or string.

    Args:
        crs_in (Any): integer: epsg code or pyproj string

    Returns:
        CRS: pyproj.CRS
    """
    # if type(crs_in) == int:
    #     in_crs = CRS.from_epsg(crs_in)
    # elif type(crs_in) == str:
    #     in_crs = CRS.from_proj4(crs_in)
    return CRS.from_user_input(crs_in)


def _get_cells_poly(  # noqa
    xr_a: Union[xr.Dataset, xr.DataArray],
    x: str,
    y: str,
    var: str,
    crs_in: Any,
    verbose: Optional[bool] = False,
) -> gpd.GeoDataFrame:  # noqa
    """Get cell polygons associated with "nodes" in xarray gridded data.

    Args:
        xr_a (xr.Dataset, xr.DataArray): _description_
        x (str): _description_
        y (str): _description_
        var (str): _description_
        crs_in (Any): _description_
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Returns:
        gpd.GeoDataFrame: _description_
    """
    tlon = xr_a[x]
    tlat = xr_a[y]
    in_crs = _get_crs(crs_in)
    # if type(crs_in) == int:
    #     in_crs = CRS.from_epsg(crs_in)
    # elif type(crs_in) == str:
    #     in_crs = CRS.from_proj4(crs_in)

    # out_crs = _get_crs(4326)
    lon, lat = np.meshgrid(tlon, tlat)
    poly = []
    if verbose:
        logger.info("calculating surrounding cell vertices")
    start = time.perf_counter()
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
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating surrounding cell vertices in {round(end-start, 2)} second(s)"
        )

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

    if verbose:
        logger.info("calculating cell 1 centroids")
    start = time.perf_counter()
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
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 1 centroids in {round(end-start, 2)} second(s)"
        )
    del tpoly_1_lat, tpoly_1_lon

    if verbose:
        logger.info("calculating cell 2 centroids")
    start = time.perf_counter()
    tpoly_2_lon = [
        [lon_n[i], lon_ip1[i], lon_ip1_jp1[i], lon_jp1[i]] for i in range(numcells)
    ]
    tpoly_2_lat = [
        [lat_n[i], lat_ip1[i], lat_ip1_jp1[i], lat_jp1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_2_lon), tpoly_2_lon[0])
    newp = [Polygon(zip(tpoly_2_lon[i], tpoly_2_lat[i])) for i in range(numcells)]
    p2 = [p.centroid for p in newp]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 2 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_2_lat, tpoly_2_lon, newp

    if verbose:
        logger.info("calculating cell 3 centroids")
    start = time.perf_counter()
    tpoly_3_lon = [
        [lon_n[i], lon_jp1[i], lon_im1_jp1[i], lon_im1[i]] for i in range(numcells)
    ]
    tpoly_3_lat = [
        [lat_n[i], lat_jp1[i], lat_im1_jp1[i], lat_im1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [Polygon(zip(tpoly_3_lon[i], tpoly_3_lat[i])) for i in range(numcells)]
    p3 = [p.centroid for p in newp]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 3 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_3_lat, tpoly_3_lon, newp

    if verbose:
        logger.info("calculating cell 4 centroids")
    start = time.perf_counter()
    tpoly_4_lon = [
        [lon_n[i], lon_im1[i], lon_im1_jm1[i], lon_jm1[i]] for i in range(numcells)
    ]
    tpoly_4_lat = [
        [lat_n[i], lat_im1[i], lat_im1_jm1[i], lat_jm1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [Polygon(zip(tpoly_4_lon[i], tpoly_4_lat[i])) for i in range(numcells)]
    p4 = [p.centroid for p in newp]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 4 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_4_lat, tpoly_4_lon, newp
    del (
        lon_n,
        lon_jm1,
        lon_ip1_jm1,
        lon_ip1,
        lon_ip1_jp1,
        lon_jp1,
        lon_im1_jp1,
        lon_im1,
        lon_im1_jm1,
    )
    del (
        lat_n,
        lat_jm1,
        lat_ip1_jm1,
        lat_ip1,
        lat_ip1_jp1,
        lat_jp1,
        lat_im1_jp1,
        lat_im1,
        lat_im1_jm1,
    )

    if verbose:
        logger.info("creating bounding polygons")
    start = time.perf_counter()
    lon_point_list = [[p1[i].x, p2[i].x, p3[i].x, p4[i].x] for i in range(numcells)]
    lat_point_list = [[p1[i].y, p2[i].y, p3[i].y, p4[i].y] for i in range(numcells)]
    poly = [Polygon(zip(lon_point_list[i], lat_point_list[i])) for i in range(numcells)]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished creating bounding polygons in {round(end-start, 2)} second(s)"
        )

    if verbose:
        logger.info("reprojecting cells")
    start = time.perf_counter()
    # grd_shp = xr_a[var].values.shape
    df = pd.DataFrame({"i_index": i_index, "j_index": j_index})
    gmcells = gpd.GeoDataFrame(df, index=index, geometry=poly, crs=in_crs)
    # gmcells.to_crs(crs=out_crs, inplace=True)
    end = time.perf_counter()
    if verbose:
        logger.info(f"finished reprojecting cells in {round(end-start, 2)} second(s)")

    return gmcells


def _generate_weights_pershp(
    poly: gpd.GeoDataFrame,
    poly_idx: str,
    grid_cells: gpd.GeoDataFrame,
    wght_gen_crs: str,
) -> pd.DataFrame:
    """Generate weights for aggragations of poly-to-poly mapping.

    Args:
        poly (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        wght_gen_crs (str): _description_

    Raises:
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
    tcount = 0

    numrows = len(npoly.index)
    print_on = _get_print_on(numrows)

    # in order, i_index, j_index, poly_index, weight values
    i_index = []
    j_index = []
    p_index = []
    wghts = []

    for index, row in npoly.iterrows():
        # hru_area = poly.loc[poly[poly_idx] == row[poly_idx]].geometry.area.sum()
        hru_area = row.geometry.area
        if possible_matches_index := list(
            spatial_index.intersection(row["geometry"].bounds)
        ):
            possible_matches = grid_cells.iloc[possible_matches_index]
            precise_matches = possible_matches[
                possible_matches.intersects(row["geometry"])
            ]
            if len(precise_matches) != 0:
                res_intersection = gpd.overlay(
                    npoly.loc[[index]], precise_matches, how="intersection"
                )
                for nindex, nrow in res_intersection.iterrows():
                    tmpfloat = float(res_intersection.area.iloc[nindex] / hru_area)
                    i_index.append(int(nrow["i_index"]))
                    j_index.append(int(nrow["j_index"]))
                    p_index.append(str(nrow[poly_idx]))
                    wghts.append(tmpfloat)
                tcount += 1
                if tcount % print_on == 0:
                    logger.info(index)

        else:
            print("no intersection: ", index, flush=True)

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
    end = time.perf_counter()
    print(f"Weight generations finished in {round(end-start, 2)} second(s)")
    return wght_df


def _build_subset_cat(
    param_json: CatParams,
    grid_json: CatGrids,
    bounds: npt.NDArray[np.double],
    date_min: str,
    date_max: Optional[str] = None,
) -> Dict[Any, Any]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        param_json (CatParams): _description_
        grid_json (CatGrids): _description_
        bounds (npt.NDArray[np.double]): _description_
        date_min (str): _description_
        date_max (str, optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """
    xname = grid_json.X_name
    yname = grid_json.Y_name
    # print(type(xname), type(yname))
    tname = param_json.T_name
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    gridorder = bool(grid_json.toptobottom)
    if not gridorder:
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


def _read_shp_file(shp_file: Union[str, gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
    """Read shapefile.

    Args:
        shp_file (Union[str, gpd.GeoDataFrame]): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    return pd.read_file(shp_file) if isinstance(shp_file, str) else shp_file


def _get_shp_file(
    shp_file: gpd.GeoDataFrame, grid_json: CatGrids, is_degrees: bool
) -> Tuple[gpd.GeoDataFrame, npt.NDArray[np.double]]:
    """Return GeoDataFrame and bounds of shapefile.

    Args:
        shp_file (gpd.GeoDataFrame): _description_
        grid_json (CatGrids): _description_
        is_degrees (bool): _description_

    Returns:
        Union[gpd.GeoDataFrame, npt.NDArray[np.double]y]: _description_
    """
    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf = shp_file.to_crs(grid_json.proj)
    # buffer polygons bounding box by twice max resolution of grid
    bbox = box(*gdf.total_bounds)
    gdf_bounds = bbox.buffer(2 * max(grid_json.resX, grid_json.resY)).bounds
    if is_degrees:
        if (gdf_bounds[0] < -180.0) & (gdf_bounds[2] > 180.0):
            newxmax = 180 - (abs(gdf_bounds[0]) - 180.0)
            newxmin = -180.0 + (abs(gdf_bounds[2]) - 180.0)
            gdf_bounds = (newxmin, gdf_bounds[1], newxmax, gdf_bounds[3])
            print("Warning: The feature data crosses the anitmeridian.")

    # TODO: need to rethink buffer - leaving it out for now
    # gdf_bounds = gdf.total_bounds.buffer(2.0*buffer)
    return gdf, gdf_bounds


def _is_degrees(ds: xr.Dataset, grid_json: CatGrids) -> bool:
    """Test if degrees in attributes on longitude.

    Args:
        ds (xr.Dataset): _description_
        grid_json (CatGrids): _description_

    Returns:
        bool: _description_
    """
    xvals = ds[grid_json.X_name]
    attr = xvals.attrs
    units = attr.get("units")
    return bool(re.search("degrees", units, flags=re.IGNORECASE))


def _is_lon_0_360(vals: npt.NDArray[np.double]) -> bool:
    """Test if longitude spans 0-360.

    Args:
        vals (npt.NDArray[np.double]): _description_

    Returns:
        bool: _description_
    """
    result = False
    if (vals[0] > 180.0) & (np.min(vals) > 0.0):
        result = False
    elif (np.max(vals) > 180.0) & (np.min(vals) > 180.0):
        result = False
    elif np.max(vals) > 180.0:
        result = True

    return result


def _get_shp_bounds_w_buffer(
    gdf: gpd.GeoDataFrame, ds: xr.Dataset, crs: Any, lon: str, lat: str
) -> npt.NDArray[np.double]:
    """Return bounding box based on 2 * max(ds.dx, ds.dy).

    Args:
        gdf (gpd.GeoDataFrame): _description_
        ds (xr.Dataset): _description_
        crs (Any): _description_
        lon (str): _description_
        lat (str): _description_

    Returns:
        tuple: _description_
    """
    bbox = box(*gdf.to_crs(crs).total_bounds)
    return np.asarray(
        bbox.buffer(
            2 * max(max(np.diff(ds[lat].values)), max(np.diff(ds[lon].values)))
        ).bounds
    )


def _check_for_intersection(
    params_json: CatParams,
    grid_json: CatGrids,
    gdf: gpd.GeoDataFrame,
) -> Tuple[bool, bool, bool]:
    """Check broadly for intersection between features and grid.

    Args:
        params_json (CatParams): _description_
        grid_json (CatGrids): _description_
        gdf (gpd.GeoDataFrame): _description_

    Returns:
        Tuple[bool, bool, bool]: _description_
    """
    is_degrees = False
    is_intersect = True
    is_0_360 = False
    ds_url = params_json.URL
    ds = xr.open_dataset(
        ds_url + "#fillmismatch", decode_coords=True, chunks={}
    )  # type:ignore
    xvals = ds[grid_json.X_name]
    yvals = ds[grid_json.Y_name]
    minx = xvals.values.min()
    maxx = xvals.values.max()
    miny = yvals.values.min()
    maxy = yvals.values.max()
    ds_bbox = box(minx, miny, maxx, maxy)
    bounds = _get_shp_bounds_w_buffer(
        gdf,
        ds,
        grid_json.proj,
        grid_json.X_name,
        grid_json.Y_name,
    )
    is_degrees = _is_degrees(ds=ds, grid_json=grid_json)
    if is_degrees & (not ds_bbox.intersects(box(*np.asarray(bounds).tolist()))):
        is_intersect = False
        is_0_360 = _is_lon_0_360(xvals.values)
        if is_0_360:
            warning_string = (
                "0-360 longitude crossing the international date line encountered.\n"
                "Longitude coordinates will be 0-360 in output."
            )
            warnings.warn(warning_string)

    return is_intersect, is_degrees, is_0_360


def _get_data_via_catalog(
    params_json: CatParams,
    grid_json: CatGrids,
    bounds: npt.NDArray[np.double],
    begin_date: str,
    end_date: Optional[str] = None,
    rotate_lon: Optional[bool] = False,
) -> xr.DataArray:
    """Get xarray spatial and temporal subset.

    Args:
        params_json (CatParams): _description_
        grid_json (CatGrids): _description_
        bounds (np.ndarray): _description_
        begin_date (str): _description_
        end_date (Optional[str], optional): _description_. Defaults to None.
        rotate_lon (Optional[bool], optional): _description_. Defaults to False.

    Returns:
        xr.DataArray: _description_
    """
    ds_url = params_json.URL
    ds = xr.open_dataset(
        ds_url + "#fillmismatch", decode_coords=True, chunks={}
    )  # type:ignore
    if rotate_lon:
        lon = grid_json.X_name
        ds.coords[lon] = (ds.coords["lon"] + 180) % 360 - 180
        ds = ds.sortby(ds[lon])

    # get grid data subset to polygons buffered bounding box
    ss_dict = _build_subset_cat(params_json, grid_json, bounds, begin_date, end_date)
    # gridMET requires the '#fillmismatch' see:
    # https://discourse.oceanobservatories.org/
    # t/
    # accessing-data-on-thredds-opendap-via-python-netcdf4-or-xarray
    # -dealing-with-fillvalue-type-mismatch-error/61

    varname = params_json.varname
    return ds[varname].sel(**ss_dict)  # type: ignore


def _get_wieght_df(wght_file: Union[str, pd.DataFrame], poly_idx: str) -> pd.DataFrame:
    if isinstance(wght_file, pd.DataFrame):
        wghts = wght_file.copy()
    elif isinstance(wght_file, str):
        wghts = pd.read_csv(
            wght_file, dtype={"i": int, "j": int, "wght": float, poly_idx: str}
        )
    else:
        sys.exit("wght_file must be one of string or pandas.DataFrame")
    return wghts


def _date_range(p_start: str, p_end: str, intv: int) -> Iterator[str]:
    """Return a date range.

    Args:
        p_start (str): _description_
        p_end (str): _description_
        intv (int): _description_

    Yields:
        Iterator[str]: _description_
    """
    start = datetime.strptime(p_start, "%Y-%m-%d")
    end = datetime.strptime(p_end, "%Y-%m-%d")
    diff = (end - start) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y-%m-%d")
    yield end.strftime("%Y-%m-%d")


def _get_catalog_time_increment(param: pd.DataFrame) -> Tuple[int, str]:
    interval = param["interval"].values[0].split(" ")
    return int(interval[0]), str(interval[1])


def _get_dataframe(object: Union[str, pd.DataFrame]) -> pd.DataFrame:
    if isinstance(object, str):
        return pd.DataFrame.from_dict(json.loads(object))
    else:
        return object


# this function is copied from here:
# https://github.com/gboeing/osmnx/blob/main/osmnx/utils_geo.py
# if it turns out to be helpful in speedin up intersections then I'll import it via
# the package - for now copied in here for development testing.
def _quadrat_cut_geometry(
    geometry: Union[shapely.geometry.Polygon, shapely.geometry.MultiPolygon],
    quadrat_width: float,
    min_num: Optional[int] = 3,
) -> shapely.geometry.MultiPolygon:
    """Split a Polygon or MultiPolygon up into sub-polygons of a specified size.

    Args:
        geometry (Union[shapely.geometry.Polygon, shapely.geometry.MultiPolygon]): _description_
        quadrat_width (float): _description_
        min_num (Optional[int], optional): _description_. Defaults to 3.

    Returns:
        shapely.geometry.MultiPolygon: _description_
    """
    # create n evenly spaced points between the min and max x and y bounds
    west, south, east, north = geometry.bounds
    x_num = int(np.ceil((east - west) / quadrat_width) + 1)
    y_num = int(np.ceil((north - south) / quadrat_width) + 1)
    x_points = np.linspace(west, east, num=max(x_num, min_num))
    y_points = np.linspace(south, north, num=max(y_num, min_num))

    # create a quadrat grid of lines at each of the evenly spaced points
    vertical_lines = [
        LineString([(x, y_points[0]), (x, y_points[-1])]) for x in x_points
    ]
    horizont_lines = [
        LineString([(x_points[0], y), (x_points[-1], y)]) for y in y_points
    ]
    lines = vertical_lines + horizont_lines

    # recursively split the geometry by each quadrat line
    geometries = [geometry]

    for line in lines:
        # split polygon by line if they intersect, otherwise just keep it
        split_geoms = [
            split(g, line).geoms if g.intersects(line) else [g] for g in geometries
        ]
        # now flatten the list and process these split geoms on the next line in
        # the list of lines
        geometries = [g for g_list in split_geoms for g in g_list]

    return MultiPolygon(geometries)
