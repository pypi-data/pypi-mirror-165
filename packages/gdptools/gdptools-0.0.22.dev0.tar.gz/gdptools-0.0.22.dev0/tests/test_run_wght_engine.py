"""Testing run_wght_engine functions."""
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest

from gdptools.gdp_data_class import CatGrids
from gdptools.gdp_data_class import CatParams
from gdptools.helpers import calc_weights_catalog
from gdptools.helpers import calc_weights_catalog2
from gdptools.run_weights_engine import RunWghtEngine

# from .support import skip_if_typeguard

gm_vars = ["aet", "pet", "PDSI"]


@pytest.fixture
def param_dict(vars=gm_vars) -> Dict:
    """Return parameter json."""
    param_json = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
    params = pd.read_json(param_json)
    _id = "terraclim"  # noqa
    var_params = [
        params.query(
            "id == @_id & variable == @_var", local_dict={"_id": _id, "_var": _var}
        )
        for _var in vars
    ]
    return dict(zip(vars, var_params))


@pytest.fixture
def grid_dict(vars=gm_vars) -> Dict:
    """Return grid json."""
    grid_json = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
    grids = pd.read_json(grid_json)
    _gridid = 116  # noqa
    var_grid = [
        grids.query(
            "grid_id == @_gridid", local_dict={"_gridid": _gridid, "_var": _var}
        )
        for _var in vars
    ]
    return dict(zip(vars, var_grid))


@pytest.fixture
def gdf() -> gpd.GeoDataFrame:
    """Create xarray dataset."""
    return gpd.read_file("./tests/data/hru_1210_epsg5070.shp")


@pytest.fixture
def poly_idx() -> str:
    """Return poly_idx."""
    return "hru_id_nat"


@pytest.fixture
def wght_gen_proj() -> int:
    """Return wght gen projection."""
    return 6931


# @skip_if_typeguard
def test__rwe(
    param_dict, grid_dict, gdf, poly_idx, wght_gen_proj, tvars=gm_vars
) -> None:
    """Test rwe."""
    cp = CatParams(**param_dict.get(tvars[0]).to_dict("records")[0])
    cg = CatGrids(**grid_dict.get(tvars[0]).to_dict("records")[0])
    wghtf = calc_weights_catalog(
        params_json=cp,
        grid_json=cg,
        shp_file=gdf,
        shp_poly_idx=poly_idx,
        wght_gen_proj=wght_gen_proj,
    )
    assert isinstance(wghtf, pd.DataFrame)

    eng = RunWghtEngine()

    eng.initialize(
        param_dict=param_dict,
        grid_dict=grid_dict,
        wghts=wghtf,
        gdf=gdf,
        gdf_poly_idx=poly_idx,
        start_date="1980-01-01",
        end_date="1980-12-31",
    )

    ngdf, nvals = eng.run(numdiv=1)

    test_arr = np.asarray(
        [
            [3.1605408],
            [0.0121277],
            [41.983784],
            [68.91504],
            [81.72351],
            [92.60617],
            [48.96107],
            [37.30392],
            [27.883911],
            [64.65818],
            [52.897045],
            [1.6390916],
        ]
    )

    np.testing.assert_allclose(test_arr, nvals[0], rtol=1e-4, verbose=True)

    with TemporaryDirectory() as tmpdirname:
        success = eng.finalize(
            gdf=ngdf,
            vals=nvals,
            p_opath=tmpdirname,
            prefix="terraclimetest",
        )
        file = Path(tmpdirname) / "terraclimetest.nc"
        assert success
        assert file.exists()


def test__rwe2(
    param_dict, grid_dict, gdf, poly_idx, wght_gen_proj, tvars=gm_vars
) -> None:
    """Test rwe."""
    cp = CatParams(**param_dict.get(tvars[0]).to_dict("records")[0])
    cg = CatGrids(**grid_dict.get(tvars[0]).to_dict("records")[0])
    wghtf = calc_weights_catalog2(
        params_json=cp,
        grid_json=cg,
        shp_file=gdf,
        shp_poly_idx=poly_idx,
        wght_gen_proj=wght_gen_proj,
    )
    assert isinstance(wghtf, pd.DataFrame)

    eng = RunWghtEngine()

    eng.initialize(
        param_dict=param_dict,
        grid_dict=grid_dict,
        wghts=wghtf,
        gdf=gdf,
        gdf_poly_idx=poly_idx,
        start_date="1980-01-01",
        end_date="1980-12-31",
    )

    ngdf, nvals = eng.run(numdiv=1)

    test_arr = np.asarray(
        [
            [3.1605408],
            [0.0121277],
            [41.983784],
            [68.91504],
            [81.72351],
            [92.60617],
            [48.96107],
            [37.30392],
            [27.883911],
            [64.65818],
            [52.897045],
            [1.6390916],
        ]
    )

    np.testing.assert_allclose(test_arr, nvals[0], rtol=1e-4, verbose=True)

    with TemporaryDirectory() as tmpdirname:
        success = eng.finalize(
            gdf=ngdf,
            vals=nvals,
            p_opath=tmpdirname,
            prefix="terraclimetest",
        )
        file = Path(tmpdirname) / "terraclimetest.nc"
        assert success
        assert file.exists()
