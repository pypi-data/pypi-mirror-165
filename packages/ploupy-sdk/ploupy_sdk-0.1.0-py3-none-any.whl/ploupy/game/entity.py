class Entity:
    def __init__(self) -> None:
        self._alive = True
        self._death_cause: str | None = None

    @property
    def alive(self) -> bool:
        return self._alive

    @property
    def death_cause(self) -> str | None:
        return self._death_cause

    def _die(self, death_cause: str):
        """
        Set alive, death_cause attributes
        """
        self._alive = False
        self._death_cause = death_cause

    @staticmethod
    def _remove_deads(entities: dict[str, "Entity"]):
        """
        Filter the given entities dict, only
        keep alive ones
        """
        ids = list(entities.keys())
        for id in ids:
            if not entities[id].alive:
                entities.pop(id)
