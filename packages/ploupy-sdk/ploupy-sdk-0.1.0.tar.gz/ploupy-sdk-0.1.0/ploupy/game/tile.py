from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from ..models.core import GameConfig

from .player import Player

from ..order import OrderMixin

from ..models.game import TileState
from ..core import InvalidStateException

if TYPE_CHECKING:
    from .game import Game


class Tile:
    def __init__(self, state: TileState, game: Game) -> None:
        self._assert_complete_state(state)
        self._config: GameConfig = game.config
        self._id: str = state.id
        self._coord: np.ndarray = state.coord.coord
        self._owner: str | None = state.owner
        self._occupation: int = state.occupation
        self._building_id: str | None = None

    def _assert_complete_state(self, state: TileState):
        if None in (state.coord, state.occupation):
            raise InvalidStateException()

    @property
    def id(self) -> str:
        return self._id

    @property
    def coord(self) -> np.ndarray:
        return self._coord.copy()

    @property
    def owner(self) -> str | None:
        """Username of owner"""
        return self._owner

    @property
    def occupation(self) -> int:
        return self._occupation

    def can_build(self, player: Player) -> bool:
        """
        Return if the given player can build on this tile
        """
        return (
            self._building_id is None
            and self.owner == player.username
            and self._occupation >= self._config.building_occupation_min
        )

    async def _update_state(self, state: TileState):
        """
        Update instance with given state
        """
        if state.coord is not None:
            self._coord = state.coord.coord
        self._owner = state.owner
        if state.occupation is not None:
            self._occupation = state.occupation
