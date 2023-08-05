import json
import logging
import numpy as np
from pydantic import BaseModel

from .game.probe import Probe

from .core.exceptions import ActionFailedException

from .models import core as _c, sio as _s, game as _g
from .sio import sio

logger = logging.getLogger("ploupy")


class Actions:
    @staticmethod
    async def _send_action(action: str, model: BaseModel):
        response = await sio.call(action, model.dict())
        response = _c.Response(**json.loads(response))

        if not response.success:
            logger.warning(f"{action} failed: {response.msg}")
            raise ActionFailedException(response.msg)

    @classmethod
    async def build_factory(cls, gid: str, coord: _c.Pos):
        model = _s.actions.BuildFactory(gid=gid, coord=_c.Point.from_list(coord))
        await cls._send_action("action_build_factory", model)

    @classmethod
    async def build_turret(cls, gid: str, coord: _c.Pos):
        model = _s.actions.BuildTurret(gid=gid, coord=_c.Point.from_list(coord))
        await cls._send_action("action_build_turret", model)

    @classmethod
    async def move_probes(cls, gid: str, probes: list[Probe], target: _c.Pos):
        model = _s.actions.MoveProbes(
            gid=gid, ids=[p.id for p in probes], target=_c.Point.from_list(target)
        )
        await cls._send_action("action_move_probes", model)

    @classmethod
    async def explode_probes(cls, gid: str, probes: list[Probe]):
        model = _s.actions.ExplodeProbes(gid=gid, ids=[p.id for p in probes])
        await cls._send_action("action_explode_probes", model)

    @classmethod
    async def probes_attack(cls, gid: str, probes: list[Probe]):
        model = _s.actions.ProbesAttack(gid=gid, ids=[p.id for p in probes])
        await cls._send_action("action_probes_attack", model)

    @classmethod
    async def acquire_tech(cls, gid: str, tech: _g.Techs):
        model = _s.actions.AcquireTech(gid=gid, tech=tech.name)
        await cls._send_action("action_acquire_tech", model)
