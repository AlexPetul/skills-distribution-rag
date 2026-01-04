from typing import Any, Protocol, overload


class CacheProtocol(Protocol):
    @overload
    async def set(self, key: str, value: Any) -> None: ...

    @overload
    async def set(self, key: str, value: Any, ex: int) -> None: ...

    async def get(self, key: str): ...
