from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class _Scalambda(Generic[T]):
    def __add__(self, other: Any) -> Callable[[T], R]:
        def add(x: T) -> R:
            return x + other

        return add


_ = _Scalambda()
