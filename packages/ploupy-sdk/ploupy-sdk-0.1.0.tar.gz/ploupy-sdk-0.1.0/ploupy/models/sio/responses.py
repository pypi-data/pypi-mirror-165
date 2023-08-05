from .. import core as _c, game as _g


class StartGame(_c.Response):
    """
    Represents the start game event
    """

    gid: str


class QueueInvitation(_c.Response):
    """
    Represents an invitation to a queue
    """

    qid: str


class GameResults(_c.Response):
    """
    Represents the results of a game
    Including the statistics of the game
    and the mmrs updates.
    """

    gid: str
    ranking: list[_c.User]
    """players: from best (idx: 0) to worst (idx: -1)"""
    stats: list[_g.GamePlayerStats]
    """
    in-game statistics of each player (same order as ranking)
    """
    mmrs: list[int]
    """
    new mmr of players in game 
    """
    mmr_diffs: list[int]
    """
    mmr difference of players in game (same order as ranking)
    """
