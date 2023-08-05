from enum import Enum, auto
from pydantic import BaseModel

from ..core import core as _c
from ..game import entities


class Techs(Enum):
    PROBE_EXPLOSION_INTENSITY = "PROBE_EXPLOSION_INTENSITY"
    PROBE_CLAIM_INTENSITY = "PROBE_CLAIM_INTENSITY"
    PROBE_HP = "PROBE_HP"
    FACTORY_BUILD_DELAY = "FACTORY_BUILD_DELAY"
    FACTORY_PROBE_PRICE = "FACTORY_PROBE_PRICE"
    FACTORY_MAX_PROBE = "FACTORY_MAX_PROBE"
    TURRET_SCOPE = "TURRET_SCOPE"
    TURRET_FIRE_DELAY = "TURRET_FIRE_DELAY"
    TURRET_MAINTENANCE_COSTS = "TURRET_MAINTENANCE_COSTS"

    @property
    def type(self) -> str:
        """
        The tech type: "probe" | "turret" | "factory"
        """
        return self.name.split("_")[0].lower()


class MapState(BaseModel):
    tiles: list[entities.TileState] = []


class PlayerState(BaseModel):
    uid: str
    username: str
    money: int | None = None
    death: str | None = None
    income: int | None = None
    techs: list[str] = []
    factories: list[entities.FactoryState] = []
    turrets: list[entities.TurretState] = []
    probes: list[entities.ProbeState] = []


class GameState(BaseModel):
    gid: str
    config: _c.GameConfig | None = None
    metadata: _c.GameMetadata | None = None
    map: MapState | None = None
    players: list[PlayerState] = []


class GamePlayerStats(BaseModel):
    username: str
    money: list[int]
    occupation: list[int]
    factories: list[int]
    turrets: list[int]
    probes: list[int]


class GameResult(BaseModel):
    ranking: list[_c.User]
    """players: from best (idx: 0) to worst (idx: -1)"""
    stats: list[GamePlayerStats]
