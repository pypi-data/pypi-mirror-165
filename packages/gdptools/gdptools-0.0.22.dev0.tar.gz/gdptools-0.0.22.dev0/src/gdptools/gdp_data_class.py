"""Data classes."""
from __future__ import annotations

from typing import Any
from typing import Optional

import numpy as np
import xarray as xr
from attrs import define
from attrs import field
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from pyproj.crs import CRS


def check_xname(instance, attribute, value):
    """Validate xname."""
    if value not in instance.ds.coords:
        raise ValueError(f"xname:{value} not in {instance.ds.coords}")


def check_yname(instance, attribute, value):
    """Validate yname."""
    if value not in instance.ds.coords:
        raise ValueError(f"yname:{value} not in {instance.ds.coords}")


def check_band(instance, attribute, value):
    """Validate band name."""
    if value not in instance.ds.coords:
        raise ValueError(f"band:{value} not in {instance.ds.coords}")


def check_crs(instance, attribute, value):
    """Validate crs."""
    crs = CRS.from_user_input(value)
    if not isinstance(crs, CRS):
        raise ValueError(f"crs:{crs} not in valid")


@define(kw_only=True)
class TiffAttributes(object):
    """Tiff qttributes data class."""

    varname: str
    xname: str = field(validator=check_xname)
    yname: str = field(validator=check_yname)
    bname: str = field(validator=check_band)
    band: int = field()
    toptobottom: bool = field(init=False)
    crs: Any = field(validator=check_crs)
    categorical: bool = field()
    ds: xr.DataArray

    def __attrs_post_init__(self):
        """Generate toptobottom."""
        yy = self.ds.coords[self.yname].values
        self.toptobottom = yy[0] <= yy[-1]


class CatParams(BaseModel):
    """Class representing elements of Mike Johnsons OpenDAP catalog params.

    https://mikejohnson51.github.io/opendap.catalog/cat_params.json
    """

    id: str
    URL: str
    grid_id: int
    variable: str
    varname: str
    long_name: str
    T_name: str
    duration: str
    units: str
    interval: str = None
    nT: Optional[int] = None  # noqa
    tiled: Optional[str] = None
    model: Optional[str] = None
    ensemble: Optional[str] = None
    scenario: Optional[str] = None

    @validator("grid_id", pre=True, always=True)
    def set_grid_id(cls, v):  # noqa:
        """Convert to int."""
        return int(v)

    @validator("nT", pre=True, always=False)
    def set_nt(cls, v):  # noqa:
        """Convert to int."""
        return 0 if np.isnan(v) else int(v)


class CatGrids(BaseModel):
    """Class representing elements of Mike Johnsons OpenDAP catalog grids.

    https://mikejohnson51.github.io/opendap.catalog/cat_grids.json
    """

    grid_id: int
    X_name: str
    Y_name: str
    X1: float
    Xn: float
    Y1: float
    Yn: float
    resX: float  # noqa
    resY: float  # noqa
    ncols: int
    nrows: int
    proj: str
    toptobottom: int
    tile: Optional[str] = None
    grid_id_1: Optional[str] = Field(None, alias="grid.id")

    @validator("toptobottom", pre=True, always=True)
    def get_toptobottom(cls, v):  # noqa:
        """Convert str to int."""
        return int(v)
