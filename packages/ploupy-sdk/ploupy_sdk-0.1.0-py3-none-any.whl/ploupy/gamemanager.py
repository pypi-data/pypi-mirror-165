import asyncio
from typing import Type

from .behaviour import Behaviour
from .game import Game
from .models.game import GameState


class GameManager:
    def __init__(self, uid: str, behaviour_class: Type[Behaviour]) -> None:
        self._uid = uid
        self._behaviour_class = behaviour_class
        self._games: dict[str, Game] = {}
        self._behaviours: dict[str, Behaviour] = {}

    def get_game(self, gid: str) -> Game | None:
        """
        Return the game with the given gid
        """
        return self._games.get(gid)

    async def create_game(self, state: GameState):
        """
        Create a new game instance and behaviour instance
        """
        game = Game(state)
        behaviour = self._behaviour_class(self._uid, game)

        self._games[state.gid] = game
        self._behaviours[state.gid] = behaviour

        # wait a little -> avoid performing actions at same time of inital game state
        await asyncio.sleep(0.1)
        await behaviour.on_start()
