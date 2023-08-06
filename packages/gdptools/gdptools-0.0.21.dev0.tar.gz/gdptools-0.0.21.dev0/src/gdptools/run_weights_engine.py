"""Engine to run area-weighted aggragations."""
import datetime
import logging
import sys
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
from metpy.units import units as mpunits
from shapely.geometry import Point

from .ancillary import _date_range
from .ancillary import _get_catalog_time_increment
from .gdp_data_class import CatGrids
from .gdp_data_class import CatParams
from .helpers import run_weights_catalog


logger = logging.getLogger(__name__)

pd_offset_conv: Dict[str, str] = {
    "years": "Y",
    "months": "M",
    "days": "D",
    "hours": "H",
}


def valid_date(s: str) -> datetime.datetime:
    """Validate and format date str as datetime.

    Args:
        s (str): _description_

    Returns:
        datetime.datetime: _description_
    """
    try:
        val = datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        print(msg)
    return val


class RunWghtEngine:
    """Class to aggragate variables and write output to netcdf file."""

    def __init__(self) -> None:
        """Initialize."""
        pass

    def initialize(
        self: "RunWghtEngine",
        param_dict: dict[str, pd.DataFrame],
        grid_dict: dict[str, pd.DataFrame],
        wghts: Union[str, pd.DataFrame],
        gdf: Union[str, gpd.GeoDataFrame],
        gdf_poly_idx: str,
        start_date: str,
        end_date: str,
    ) -> None:
        """Initialize.

        Args:
            param_dict (Dict): _description_
            grid_dict (Dict): _description_
            wghts (Union[str, pd.DataFrame]): _description_
            gdf (Union[str, gpd.GeoDataFrame]): _description_
            gdf_poly_idx (str): _description_
            start_date (str): _description_
            end_date (str): _description_
        """
        self.param_dict = param_dict
        self.grid_dict = grid_dict
        self.wghts = wghts
        self.gdf = gdf
        self.gdf_poly_idx = gdf_poly_idx
        self.start_date = start_date
        self.end_date = end_date
        self.time_interval, self.time_type = _get_catalog_time_increment(
            list(param_dict.values())[0]
        )
        self.start = valid_date(self.start_date)
        self.end = valid_date(self.end_date)
        self.numdays = (self.end - self.start).days + 1

    def run(
        self: "RunWghtEngine", numdiv: Optional[int] = 1
    ) -> Tuple[List[gpd.GeoDataFrame], List[npt.NDArray[np.double]]]:
        """Run weighted-area-aggragation.

        Args:
            numdiv (Optional[int], optional): _description_. Defaults to 1.

        Returns:
            Tuple[List[gpd.GeoDataFrame], List[npt.NDArray[np.double]]]: _description_
        """
        ndiv: int = numdiv  # type:ignore
        date_bracket = list(_date_range(self.start_date, self.end_date, ndiv))

        gdf = []
        vals = []

        for key in self.param_dict:
            print(f"Processing: {key}")
            cp = CatParams(**self.param_dict.get(key).to_dict("records")[0])
            cg = CatGrids(**self.grid_dict.get(key).to_dict("records")[0])
            tvals = []
            for i in range(ndiv):
                if i == 0:
                    tstart = date_bracket[i]
                else:
                    date1 = valid_date(date_bracket[i])
                    date = date1 + datetime.timedelta(days=1)
                    tstart = date.strftime("%Y-%m-%d")
                tend = date_bracket[i + 1]
                newgdf, nvals = run_weights_catalog(
                    params_json=cp,
                    grid_json=cg,
                    wght_file=self.wghts,
                    shp_file=self.gdf,
                    shp_poly_idx=self.gdf_poly_idx,
                    begin_date=tstart,
                    end_date=tend,
                )
                if i == 0:
                    gdf.append(newgdf)
                tvals.append(nvals)
                print(nvals.shape)

            if ndiv > 1:
                ntvals = tvals[0]
                print(ntvals.shape)
                for i in range(1, ndiv):
                    print(tvals[i].shape)
                    ntvals = np.append(ntvals, tvals[i], axis=0)
                vals.append(ntvals)
                # vals.append(np.vstack())
            else:
                vals.append(nvals)
        print(vals[0].shape)
        return gdf, vals

    def finalize(  # noqa: C901
        self: "RunWghtEngine",
        gdf: List[gpd.GeoDataFrame],
        vals: List[npt.NDArray[np.double]],
        p_opath: str,
        prefix: Optional[str] = "t_",
        use_opt_dict: Optional[bool] = False,
        work_dict: Optional[dict[str, dict[str, Any]]] = MappingProxyType(
            {"kwarg": "default"}
        ),
    ) -> bool:
        """Write netcdf file of aggragated weighted area values.

        Args:
            gdf (List[gpd.GeoDataFrame]): _description_
            vals (List[npt.NDArray[np.double]]): _description_
            p_opath (str): _description_
            prefix (Optional[str], optional): _description_.
            use_opt_dict (Optional[bool], optional): _description_. Defaults to False.
            work_dict (_type_, optional): _description_.
                Defaults to MappingProxyType( {"kwarg": "default"} ).

        Returns:
            bool: _description_
        """
        print(len(gdf), type(gdf[0]), gdf[0].index.name)
        poly_idx = gdf[0].index.name
        time_varname = "time"
        lat_varname = "lat"
        lon_varname = "lon"
        num_ts = vals[0].shape[0]
        times = pd.date_range(
            self.start_date,
            freq=str(self.time_interval) + str(pd_offset_conv.get(self.time_type)),
            periods=num_ts,
        )

        if use_opt_dict:
            work_dict = defaultdict(lambda: None, work_dict)
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
        ncfile.Conventions = "CF-1.8"
        ncfile.featureType = "timeSeries"
        ncfile.history = ""
        feature_dim = len(gdf[0].index)
        print(poly_idx, gdf[0].index)
        ncfile.createDimension(poly_idx, size=feature_dim)
        ncfile.createDimension(time_varname, size=None)
        crs_cf = pyproj.CRS(gdf[0].crs).to_cf()
        crs = ncfile.createVariable("crs", np.int32, ())
        crs.setncatts(crs_cf)
        time = ncfile.createVariable(time_varname, "f4", (time_varname,))
        time.long_name = time_varname
        time.standard_name = time_varname
        time.units = "days since " + self.start_date
        time.calendar = "standard"
        time[:] = netCDF4.date2num(
            times.to_pydatetime(), time.units, calendar="standard"
        )

        long_name = "feature id"
        if use_opt_dict and wd_feature["long_name"]:
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
        for index, key in enumerate(self.param_dict):
            print(f"Processing: {key}")
            param_json: pd.DataFrame = self.param_dict.get(key)
            long_name = param_json.long_name.values[0]
            standard_name = param_json.varname.values[0]
            units = param_json.units.values[0]
            uconv = False
            convert_unit = ""
            if use_opt_dict:
                try:
                    dict_var = defaultdict(lambda: None, work_dict.get(key))
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
                        f"Error: Key - {key} not found in work_dict \
                            will resort to default values"
                    )

            vartype = vals[index].dtype
            ncvar = ncfile.createVariable(
                key,
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


# class RunWghtEnginePerFeature:
#     """Class to aggragate variables by polygon and write ouput to netcdf file."""

#     def __init__(self, log_level: Optional[str] = "Critical") -> None:
#         """Init class.

#         Args:
#             log_level (str): _description_
#         """
#         tmp = log_level  # noqa: F841
#         self.wpf_log = logging.getLogger(__name__)
#         pass

#     def initialize(
#         self: "RunWghtEnginePerFeature",
#         param_dict: Dict,
#         grid_dict: Dict,
#         gdf: str,
#         start_date: str,
#         end_date: str,
#         wght_gen_proj: str,
#     ) -> None:
#         """Initialize.

#         Args:
#             param_dict (Dict): _description_
#             grid_dict (Dict): _description_
#             gdf (str): _description_
#             start_date (str): _description_
#             end_date (str): _description_
#             wght_gen_proj (str): _description_
#         """
#         self.param_dict = param_dict
#         self.grid_dict = grid_dict

#         self.gdf = gpd.read_file(gdf)
#         self.start_date = start_date
#         self.end_date = end_date

#         self.wght_gen_proj = wght_gen_proj

#         self.start = valid_date(self.start_date)
#         self.end = valid_date(self.end_date)
#         self.numdays = (self.end - self.start).days + 1
#         self.wpf_log.info("finished RunWghtEnginePerFeature.initialize()")

#     def run_per_feature(self) -> Union[List[gpd.GeoDataFrame], List[np.ndarray]]:
#         """Run weighted area aggragation per feature.

#         Returns:
#             Union[List[gpd.GeoDataFrame], List[np.ndarray]]: _description_
#         """
#         ngdf = []
#         nvals = []

#         num_features = len(self.gdf.index)
#         print(f"Number of features to process: {num_features}")
#         for _key in self.param_dict:

#             key_gdf = []
#             key_vals = []
#             for index in range(num_features):
#                 tgdf = self.gdf.loc[[index]]
#                 newgdf, vals = intersect_by_weighted_area(
#                     params_json=self.param_dict.get("tmax"),
#                     grid_json=self.grid_dict.get("tmax"),
#                     gdf=tgdf,
#                     begin_date=self.start_date,
#                     end_date=self.end_date,
#                     wght_gen_proj=self.wght_gen_proj,
#                 )
#                 key_gdf.append(tgdf)
#                 key_vals.append(vals)
#             tmpgdf = pd.concat(key_gdf)
#             tmpvals = np.stack(vals, axis=0)
#             ngdf.append(tmpgdf)
#             nvals.append(tmpvals)

#         return ngdf, nvals
