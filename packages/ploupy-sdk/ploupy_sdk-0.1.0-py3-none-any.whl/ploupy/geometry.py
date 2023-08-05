import numpy as np
from scipy.cluster.vq import kmeans2

from .game import Tile
from .models.core import Pos


def get_closest_tile(tiles: list[Tile], pos: Pos) -> Tile | None:
    """
    Return the tile closest to the given position

    Note: return None if `tiles` is empty
    """
    if len(tiles) == 0:
        return None

    coords = np.array([tile.coord - pos for tile in tiles])
    dists = np.linalg.norm(coords, axis=1)
    idx = np.argmin(dists)

    return tiles[idx]


def get_center(positions: list[Pos]) -> np.ndarray | None:
    """
    Return the center of the positions (as defined by the k-means algorithm)

    Note: return None if `positions` is empty
    """
    return get_centers(positions, 1)[0]


def get_centers(positions: list[Pos], n_center) -> list[np.ndarray]:
    """
    Return the n centers that fit the best for the given positions
    (as defined by the k-means algorithm)
    """
    positions = np.array(positions, dtype=float)

    centers, _ = kmeans2(positions, k=n_center, minit="points")

    return list(centers)
