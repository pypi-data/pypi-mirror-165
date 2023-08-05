from __future__ import annotations
from typing import TYPE_CHECKING

from ..models.game.entities import FactoryState, ProbeState, TurretState

from ..models.core import GameConfig
from .entity import Entity
from ..models.game import PlayerState, Techs
from ..core import InvalidStateException

from .factory import Factory
from .turret import Turret
from .probe import Probe

if TYPE_CHECKING:
    from .game import Game


class Player(Entity):
    """
    Represents a player in the game

    Exposes properties that are automatically updated
    on server update.

    ---

    Define callbacks by overriding the following methods:
    * `on_income`
    * `on_factory_build`
    * `on_turret_build`
    * `on_probe_build`
    * `on_probes_attack`

    Note: these callbacks are the same as the ones defined in `Behaviour`.
    So any callback defined before the `Behaviour.__init__` call will be overriden.
    """

    def __init__(self, state: PlayerState, game: Game) -> None:
        super().__init__()
        self._assert_complete_state(state)
        self._game = game
        self._config: GameConfig = game.config
        self._uid: str = state.uid
        self._username: str = state.username
        self._money: int = state.money
        self._income: int = state.income
        self._techs: set[Techs] = {Techs(t) for t in state.techs}
        self._factories: dict[str, Factory] = {
            s.id: Factory(s, self, game) for s in state.factories
        }
        self._turrets: dict[str, Turret] = {
            s.id: Turret(s, self, game) for s in state.turrets
        }
        self._probes: dict[str, Probe] = {
            s.id: Probe(s, self, game) for s in state.probes
        }

        # store currently attacking probes
        # -> to notify of their attack only once
        self._attacking_probes: list[Probe] = []

    def _assert_complete_state(self, state: PlayerState):
        if None in (state.money, state.income):
            raise InvalidStateException()

    @property
    def username(self) -> str:
        """The player's username"""
        return self._username

    @property
    def money(self) -> str:
        """
        The player's current money
        (as of last server income update)

        Note: this might not be exactly the value as on the server,
        which can cause some actions to fail unexpectedly. Thus, it is
        recommended to use orders to perform actions.
        """
        return self._money

    @property
    def income(self) -> str:
        """
        An approximation of the player's money evolution on the
        next server update.
        """
        return self._income

    @property
    def techs(self) -> set[Techs]:
        """
        The player's acquired technologies (shallow copy)
        """
        return self._techs.copy()

    @property
    def factories(self) -> list[Factory]:
        """
        The player's factories (shallow copy)
        """
        return list(self._factories.values())

    @property
    def turrets(self) -> list[Turret]:
        """
        The player's turrets (shallow copy)
        """
        return list(self._turrets.values())

    @property
    def probes(self) -> list[Probe]:
        """
        The player's probes (shallow copy)
        """
        return list(self._probes.values())

    def can_build_factory(self) -> bool:
        """
        Return if the player can build a factory

        Note: this does not take the tile into account,
        `tile.can_build` should also be called.
        """
        return self._money >= self._config.factory_price

    def can_build_turret(self) -> bool:
        """
        Return if the player can build a turret

        Note: this does not take the tile into account,
        `tile.can_build` should also be called.
        """
        return self._money >= self._config.turret_price

    def is_tech_acquirable(self, tech: Techs) -> bool:
        """
        Return if the player may acquire the `tech` as
        some point in the future (potentially now)
        """
        # check not already acquired
        if tech in self._techs:
            return False

        # check multiple tech of same category
        types = [t.type for t in self._techs]
        if tech.type in types:
            return False

        return True

    def can_acquire_tech(self, tech: Techs) -> bool:
        """
        Return if the player can acquire the `tech`
        """
        if not self.is_tech_acquirable(tech):
            return False

        price = getattr(self._config, f"tech_{tech.name.lower()}_price")
        return self._money >= price

    async def on_income(self, money: int) -> None:
        """
        Called when the money is updated
        """

    async def on_factory_build(self, factory: Factory) -> None:
        """
        Called when a factory is built
        """

    async def on_turret_build(self, turret: Turret) -> None:
        """
        Called when a turret is built
        """

    async def on_probe_build(self, probe: Probe) -> None:
        """
        Called when a probe is built
        """

    async def on_probes_attack(
        self, probes: list[Probe], attacked_player: Player
    ) -> None:
        """
        Called when some probes attack an other player
        """

    async def on_acquire_tech(self, tech: Techs) -> None:
        """
        Called when a new tech is acquired
        """

    async def _update_state(self, state: PlayerState):
        """
        Update instance with given state
        """
        if state.money is not None:
            self._money = state.money
            await self.on_income(self._money)

        if state.income is not None:
            self._income = state.income

        if state.death is not None:
            self._die(state.death)

        await self._update_techs(state.techs)
        await self._update_factories(state.factories)
        await self._update_turrets(state.turrets)
        await self._update_probes(state.probes)

    async def _update_techs(self, techs: list[str]):
        """
        Update techs
        """
        for raw in techs:
            tech = Techs(raw)
            if not tech in self._techs:
                self._techs.add(tech)
                await self.on_acquire_tech(tech)

    async def _update_factories(self, factories_states: list[FactoryState]):
        """
        Update factories
        """

        for fs in factories_states:
            factory = self._factories.get(fs.id)
            if factory is None:
                factory = Factory(fs, self, self._game)
                self._factories[fs.id] = factory
                await self.on_factory_build(factory)
            else:
                await factory._update_state(fs)

        Entity._remove_deads(self._factories)

    async def _update_turrets(self, turrets_states: list[TurretState]):
        """
        Update turrets
        """
        for ts in turrets_states:
            turret = self._turrets.get(ts.id)
            if turret is None:
                turret = Turret(ts, self, self._game)
                self._turrets[ts.id] = turret
                await self.on_turret_build(turret)
            else:
                await turret._update_state(ts)

        Entity._remove_deads(self._turrets)

    async def _update_probes(self, probes_states: list[ProbeState]):
        """
        Update probes
        """
        probes: list[Probe] = []
        for ps in probes_states:
            probe = self._probes.get(ps.id)
            if probe is None:
                probe = Probe(ps, self, self._game)
                self._probes[ps.id] = probe
                await self.on_probe_build(probe)
            else:
                await probe._update_state(ps)
            probes.append(probe)

        # handle probes_attack callback
        # group probes by targeted player
        new_attacking_probes: dict[str, list[Probe]] = {}
        for probe in probes:
            if not probe.attacking or not probe.alive:
                continue
            if not probe in self._attacking_probes:
                self._attacking_probes.append(probe)

                # get attacked tile
                tile = self._game.map.get_tile(probe.target)
                if tile is None or tile.owner is None:
                    continue

                if not tile.owner in new_attacking_probes.keys():
                    new_attacking_probes[tile.owner] = []
                new_attacking_probes[tile.owner].append(probe)

        # trigger a callback for each attacked player
        for username, probes in new_attacking_probes.items():
            player = [p for p in self._game.players if p.username == username][0]
            await self.on_probes_attack(probes, player)

        Entity._remove_deads(self._probes)
