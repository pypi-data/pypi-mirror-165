from pydantic import BaseModel

from ..core import core as _c


class TileState(BaseModel):
    id: str
    coord: _c.Point | None = None
    owner: str | None = None
    """Only store the username of the owner"""
    occupation: int | None = None


class FactoryState(BaseModel):
    id: str
    coord: _c.Point | None = None
    death: str | None = None


class ProbeState(BaseModel):
    id: str
    pos: _c.Point | None = None
    death: str | None = None
    target: _c.Point | None = None
    policy: str | None = None
    """May be: Farm or Attack"""


class TurretState(BaseModel):
    id: str
    coord: _c.Point | None = None
    death: str | None = None
    shot_id: str | None = None
