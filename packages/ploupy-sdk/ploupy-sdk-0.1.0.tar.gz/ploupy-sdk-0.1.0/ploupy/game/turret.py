from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from ..models.core import GameConfig

from .entity import Entity

from ..models.game import TurretState
from ..core import InvalidStateException

if TYPE_CHECKING:
    from .game import Game
    from .player import Player


class Turret(Entity):
    def __init__(self, state: TurretState, owner: Player, game: Game) -> None:
        super().__init__()
        self._assert_complete_state(state)
        self._owner = owner
        self._map = game.map
        self._config = game.config
        self._id: str = state.id
        self._coord: np.ndarray = state.coord.coord

        # notify map of creation
        self._map.get_tile(self._coord)._building_id = self._id

    def _assert_complete_state(self, state: TurretState):
        if None in (state.coord):
            raise InvalidStateException()

    def _die(self, death_cause: str):
        super()._die(death_cause)
        # notify map of death
        self._map.get_tile(self._coord)._building_id = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def coord(self) -> np.ndarray:
        return self._coord.copy()

    async def _update_state(self, state: TurretState):
        """
        Update instance with given state
        """
        if state.coord is not None:
            self._coord = state.coord.coord
        if state.death is not None:
            self._die(state.death)
        if state.shot_id is not None:
            pass
