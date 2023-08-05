import asyncio
import logging
import sys
import jwt
import toml
import requests
from typing import Type
from socketio import exceptions

from .core import InvalidBotKeyException, URL_SIO, setup_logger, VERSION
from .behaviour import Behaviour
from .gamemanager import GameManager
from .events import EventsHandler
from .sio import sio

logger = logging.getLogger("ploupy")


class Bot:
    """
    Main bot class

    Handle runtime of the bot.
    Call `run` method to start.

    Args:
        bot_key: Authentification key, given on bot creation.
        behaviour_class: Client defined class that defines the bot
            behaviour, must inherit from `Behaviour` class
        log_level (optional): Level of ploupy logger, defaults to INFO
    """

    def __init__(
        self,
        bot_key: str,
        behaviour_class: Type[Behaviour],
        log_level: int = logging.INFO,
    ) -> None:
        self._bot_key = bot_key
        self._uid = self._extract_uid(bot_key)
        self._game_man = GameManager(self._uid, behaviour_class)
        self._events_handler = EventsHandler(self._game_man)

        setup_logger(log_level)

        if not self._check_sdk_version():
            sys.exit(1)

    def _extract_uid(self, bot_key: str) -> str:
        """
        Extract uid from bot_key.

        Note: do not verify token signature
        """
        try:
            headers = jwt.get_unverified_header(bot_key)
        except jwt.exceptions.DecodeError as e:
            raise InvalidBotKeyException(e) from None

        uid = headers.get("uid")
        if uid is None:
            raise InvalidBotKeyException("Missing 'uid' header.")

        return uid

    def _get_sdk_version(self) -> tuple[str, str, str] | None:
        """
        Fetch the latest PyPI version
        """
        url = "https://raw.githubusercontent.com/Plouc314/ploupy-python-sdk/master/pyproject.toml"
        response = requests.get(url)
        if response.status_code != 200:
            return None

        data = toml.loads(response.text)
        version = data.get("project", {}).get("version")
        if version is None:
            return None

        try:
            major, minor, patch = version.split(".")
        except ValueError:
            return None

        return major, minor, patch

    def _check_sdk_version(self) -> bool:
        """
        Check that the current SDK version is compatible with the latest one.
        """
        lv = self._get_sdk_version()
        if lv is None:
            logger.warning(
                (
                    "Couldn't fetch latest SDK version. "
                    "The current version is probably outdated. "
                    "To update the SDK package, run: pip install ploupy-sdk --upgrade"
                )
            )
            return True

        lmajor, lminor, lpatch = lv
        latest_version = ".".join(lv)

        major, minor, patch = VERSION.split(".")

        if lmajor != major:
            logger.critical(
                (
                    "A new major version of the SDK as been released "
                    f"({VERSION} -> {latest_version}). "
                    "Update the SDK package, run: pip install ploupy-sdk --upgrade"
                )
            )
            return False

        if lminor != minor or lpatch != patch:
            logger.info(
                (
                    "A new version of the SDK as been released "
                    f"({VERSION} -> {latest_version}). "
                    "To update the SDK package, run: pip install ploupy-sdk --upgrade"
                )
            )

        return True

    async def _run(self):
        try:
            await sio.connect(URL_SIO, headers={"bot-jwt": self._bot_key})
        except exceptions.ConnectionError:
            return  # the error is logged in connect_error

        # check if existing game
        # -> connect back to them
        await sio.emit("is_active_game", {})

        await sio.wait()

    async def _disconnect(self):
        await sio.disconnect()

    def run(self):
        """
        Run the bot

        Note: this method is blocking
        """
        try:
            asyncio.get_event_loop().run_until_complete(self._run())
        except RuntimeError:  # ctr-C causes a RuntimeError
            pass
        asyncio.get_event_loop().run_until_complete(self._disconnect())
