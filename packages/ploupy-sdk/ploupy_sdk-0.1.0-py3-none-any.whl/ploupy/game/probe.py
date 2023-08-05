from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from .entity import Entity

from ..models.game import ProbeState
from ..core import InvalidStateException

if TYPE_CHECKING:
    from .game import Game
    from .player import Player


class Probe(Entity):
    def __init__(self, state: ProbeState, owner: Player, game: Game) -> None:
        super().__init__()
        self._assert_complete_state(state)
        self._owner = owner
        self._config = game.config
        self._map = game.map
        self._id: str = state.id
        self._pos: np.ndarray = state.pos.pos
        self._target: np.ndarray | None = (
            None if state.target is None else state.target.coord
        )
        self._attacking: bool = False

    def _assert_complete_state(self, state: ProbeState):
        if None in (state.pos):
            raise InvalidStateException()

    @property
    def id(self) -> str:
        return self._id

    @property
    def pos(self) -> np.ndarray:
        """Current position (dtype: float)"""
        return self._pos.copy()

    @property
    def target(self) -> np.ndarray:
        """Where the probe is going (dtype: int)"""
        if self._target is None:
            return None
        return self._target.copy()

    @property
    def attacking(self) -> bool:
        """If the probe is currently attacking"""
        return self._attacking

    async def _update_state(self, state: ProbeState):
        """
        Update instance with given state
        """
        if state.pos is not None:
            self._pos = state.pos.pos

        if state.target is not None:
            self._target = state.target.coord

        if state.policy is not None:
            self._attacking = state.policy == "Attack"

        if state.death is not None:
            self._die(state.death)
