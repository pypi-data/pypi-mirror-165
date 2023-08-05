from ..order import OrderMixin
from .entity import Entity
from ..models.core import GameConfig, GameMetadata
from ..models.game import GameState
from ..core import InvalidStateException

from .map import Map
from .player import Player


class Game(OrderMixin):
    def __init__(self, state: GameState) -> None:
        super().__init__()
        self._assert_complete_state(state)
        self._gid = state.gid
        self._config: GameConfig = state.config
        self._metadata: GameMetadata = state.metadata
        self._map: Map = Map(state.map, self)
        self._players: dict[str, Player] = {
            s.uid: Player(s, self) for s in state.players
        }

    def _assert_complete_state(self, state: GameState):
        if None in (state.config, state.metadata, state.map):
            raise InvalidStateException()

    @property
    def config(self) -> GameConfig:
        return self._config

    @property
    def metadata(self) -> GameMetadata:
        return self._metadata

    @property
    def map(self) -> Map:
        return self._map

    @property
    def players(self) -> list[Player]:
        return list(self._players.values())

    def get_player(self, uid: str) -> Player | None:
        """
        Return the player with the given uid, if it exists
        """
        return self._players.get(uid)

    def get_opponents(self, player: Player) -> list[Player]:
        """
        Return the opponents of the given player
        """
        return [p for p in self.players if p._uid != player._uid]

    async def _update_state(self, state: GameState):
        """
        Update instance with given state
        """

        if state.map is not None:
            await self._map._update_state(state.map)

        for ps in state.players:
            player = self._players.get(ps.uid)
            if player is not None:
                await player._update_state(ps)

        Entity._remove_deads(self._players)

        await self._resolve_orders()
