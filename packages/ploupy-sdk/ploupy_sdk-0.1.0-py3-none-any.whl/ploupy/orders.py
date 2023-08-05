import asyncio
from typing import Awaitable, Callable

from .core.exceptions import ActionFailedException
from .models.game import Techs

from .order import Order
from .game import Tile, Player
from .actions import Actions


class BuildFactoryOrder(Order):

    MAX_RETRIES: int = 3
    """
    Maximum number of times the action will be sent to the server
    in case of `ActionFailedException`
    """
    RETRY_DELAY: float = 0.5
    """
    Delay to wait before retrying to send the action to the server
    """

    def __init__(
        self,
        player: Player,
        tile: Tile,
        on: Callable[[], bool] | None = None,
        action: Callable[[], Awaitable[None]] | None = None,
        with_timeout: float | None = None,
        with_retry: bool = True,
    ) -> None:
        super().__init__(self._on, self._action, with_timeout=with_timeout)
        self._player = player
        self._tile = tile
        self._custom_on = on
        self._custom_action = action
        self._with_retry = with_retry

    def _on(self) -> bool:
        return (
            self._player.can_build_factory()
            and self._tile.can_build(self._player)
            and self._custom_on()
        )

    async def _action(self, nth_try: int = 0) -> None:
        """
        Try the build the factory.

        This can fails in the case the player spends money
        in between income events (for example on probe creation).
        """
        if nth_try >= self.MAX_RETRIES:
            return  # abort
        try:
            await Actions.build_factory(self._player._game._gid, self._tile.coord)
        except ActionFailedException:
            if not self._with_retry:
                return

            await asyncio.sleep(self.RETRY_DELAY)
            # retry
            await self._action(nth_try=nth_try + 1)
            return

        # executed once after main action
        if self._custom_action is not None:
            await self._custom_action()


class BuildTurretOrder(Order):

    MAX_RETRIES: int = 3
    """
    Maximum number of times the action will be sent to the server
    in case of `ActionFailedException`
    """
    RETRY_DELAY: float = 0.5
    """
    Delay to wait before retrying to send the action to the server
    """

    def __init__(
        self,
        player: Player,
        tile: Tile,
        on: Callable[[], bool] | None = None,
        action: Callable[[], Awaitable[None]] | None = None,
        with_timeout: float | None = None,
        with_retry: bool = True,
    ) -> None:
        super().__init__(self._on, self._action, with_timeout=with_timeout)
        self._player = player
        self._tile = tile
        self._custom_on = on if on is not None else lambda: True
        self._custom_action = action
        self._with_retry = with_retry

    def _on(self) -> bool:
        return (
            self._player.can_build_turret()
            and self._tile.can_build(self._player)
            and self._custom_on()
        )

    async def _action(self, nth_try: int = 0) -> None:
        """
        Try the build the turret.

        This can fails in the case the player spends money
        in between income events (for example on probe creation).
        """
        if nth_try >= self.MAX_RETRIES:
            return  # abort
        try:
            await Actions.build_turret(self._player._game._gid, self._tile.coord)
        except ActionFailedException:
            if not self._with_retry:
                return

            await asyncio.sleep(self.RETRY_DELAY)
            # retry
            await self._action(nth_try=nth_try + 1)

        # executed once after main action
        if self._custom_action is not None:
            await self._custom_action()


class AcquireTechOrder(Order):

    MAX_RETRIES: int = 3
    """
    Maximum number of times the action will be sent to the server
    in case of `ActionFailedException`
    """
    RETRY_DELAY: float = 0.5
    """
    Delay to wait before retrying to send the action to the server
    """

    def __init__(
        self,
        player: Player,
        tech: Techs,
        on: Callable[[], bool] | None = None,
        action: Callable[[], Awaitable[None]] | None = None,
        with_timeout: float | None = None,
        with_retry: bool = True,
    ) -> None:
        super().__init__(self._on, self._action, with_timeout=with_timeout)
        self._player = player
        self._tech = tech
        self._custom_on = on if on is not None else lambda: True
        self._custom_action = action
        self._with_retry = with_retry

    def _on(self) -> bool:
        if not self._player.is_tech_acquirable(self._tech):
            self.abort()
            return False
        return self._player.can_acquire_tech(self._tech) and self._custom_on()

    async def _action(self, nth_try: int = 0) -> None:
        """
        Try the acquire the tech.

        This can fails in the case the player spends money
        in between income events (for example on probe creation).
        """
        if nth_try >= self.MAX_RETRIES:
            return  # abort
        try:
            await Actions.acquire_tech(self._player._game._gid, self._tech)
        except ActionFailedException:
            if not self._with_retry:
                return

            await asyncio.sleep(self.RETRY_DELAY)
            # retry
            await self._action(nth_try=nth_try + 1)

        # executed once after main action
        if self._custom_action is not None:
            await self._custom_action()
