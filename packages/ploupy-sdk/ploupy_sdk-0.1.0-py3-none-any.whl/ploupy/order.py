import time
from typing import Any, Awaitable, Callable


class Order:
    def __init__(
        self,
        on: Callable[[], bool],
        action: Callable[[], Awaitable[None]],
        with_timeout: float | None = None,
    ) -> None:
        self._on = on
        self._action = action
        self._aborted = False
        self._timeout = with_timeout
        self._start_time = time.time()

    async def resolve(self) -> bool:
        """
        Try to resolve the order:
        Either the order is aborted (either manually or by
        timeout) or check if the conditions are met, if so
        execute the order's action.

        Return if the order was resolved
        """
        if self._aborted:
            return True

        if self._timeout is not None:
            if time.time() > self._start_time + self._timeout:
                return True

        if self._on():
            await self._action()
            return True
        return False

    def abort(self) -> None:
        """
        Abort the order, it won't be executed
        """
        self._aborted = True


class OrderMixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._orders: list[Order] = []

    async def place_order(self, order: Order) -> None:
        """
        Place an order

        Try to resolve it directly, if not
        possible, add it to the orders pool
        and tries to resolve it on game state update
        """
        if await order.resolve():
            return

        self._orders.append(order)

    async def _resolve_orders(self) -> None:
        """
        Try to resolve orders
        """
        to_remove = []
        for order in self._orders:
            if await order.resolve():
                to_remove.append(order)

        for order in to_remove:
            self._orders.remove(order)
