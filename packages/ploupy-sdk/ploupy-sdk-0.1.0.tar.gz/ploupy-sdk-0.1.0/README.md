# [Ploupy Python SDK](https://github.com/Plouc314/ploupy-python-sdk)

## Installation

```
pip install ploupy-sdk
```

> **Note**  
> This library requires python 3.10 or higher

## Getting started

Here is a minimal example:

```python
import ploupy as pp

class MyBehaviour(pp.Behaviour):
    pass  # the bot code goes here

BOT_KEY = "..." # the key given when creating the bot

bot = pp.Bot(bot_key=BOT_KEY, behaviour_class=MyBehaviour)

if __name__ == "__main__":
    bot.run()
```

## Behaviour

The SDK is events driven. Define the bot by inheriting from the `Behaviour` class
and overriding callback methods (all callbacks are **async**).

Here is an example of a bot that build a factory as soon as he can:

```python
import ploupy as pp

class MyBehaviour(pp.Behaviour):

    async def on_income(self, money: int) -> None:
        # select the tile to build the factory on
        # using Map instance exposed by Behaviour class
        # and the bot's Player instance
        tiles = self.map.get_buildable_tiles(self.player)
        if len(tiles) == 0:
            return
        tile = tiles[0]

        # check if the bot has enough money
        # using GameConfig instance exposed by Behaviour class
        if money >= self.config.factory_price:
            # send an action to the server
            # this can failed if all the necessary conditions aren't
            # met to perform the action
            try:
                await self.build_factory(tile.coord)
            except pp.ActionFailedException:
                return
```

Here is an example of a bot that will try to build a turret when attacked:

```python
import ploupy as pp

class MyBehaviour(pp.Behaviour):

    async def on_probes_attack(
        self,
        probes: list[pp.Probe],
        attacked_player: pp.Player,
        attacking_player: pp.Player,
    ) -> None:
        # check that it is the bot that is attacked
        if attacked_player is not self.player:
            return

        # get the center of where the probes are attacking
        target = pp.geometry.get_center([probe.target for probe in probes])

        # get tiles where a turret could be built
        tiles = self.map.get_buildable_tiles(self.player)

        # if none are buildable then too bad...
        if len(tiles) == 0:
            return

        # get the tile that is as close as possible to the center of the attack
        tile = pp.geometry.get_closest_tile(tiles, target)

        # place an order on "build turret" action, the action will be performed
        # when the necessary conditions are met
        await self.place_order(
            pp.BuildTurretOrder(
                self.player,
                tile,
                with_timeout=2.0, # maximum time (sec) before aborting the order
                with_retry=False, # if the action should be retried in case of failure
            )
        )

```
