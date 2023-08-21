import inspect
import types
from functools import wraps, cached_property
from typing import TypeVar, ParamSpec, Callable, Union, Generic, Awaitable, get_args, overload
from typing_extensions import TypeVarTuple, Unpack

from py_fp_playground.either import Either

E = TypeVar("E", bound=BaseException)
E2 = TypeVar("E2", bound=BaseException)
T = TypeVar("T")
R = TypeVar("R", covariant=True)
P = ParamSpec("P")
Es = TypeVarTuple("Es")

Failure = Either.left
Success = Either.right
Try = Either[E, R]


class catch(Generic[T]):

    @cached_property
    def _exception_type(self) -> T:
        return get_args(self.__orig_class__)[0]

    @cached_property
    def _exceptions(self) -> tuple[type[BaseException], ...]:
        if isinstance(self._exception_type, types.UnionType):
            exceptions = get_args(self._exception_type)
        elif issubclass(self._exception_type, BaseException):
            exceptions = (self._exception_type,)
        else:
            raise TypeError(
                f"Expected an exception type, got {self._exception_type}."
            )
        return exceptions

    @overload
    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[Either[T, R]]]:
        ...

    @overload
    def __call__(self, func: Callable[P, R]) -> Callable[P, Either[T, R]]:
        ...

    def __call__(
        self,
        func: Callable[P, R] | Callable[P, Awaitable[R]]
    ) -> Callable[P, Either[T, R]] | Callable[P, Awaitable[Either[T, R]]]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Either[T, R]:
            try:
                return Success(func(*args, **kwargs))
            except self._exceptions as e:
                return Failure(e)

        if not inspect.iscoroutinefunction(func):
            return wrapper

        @wraps(func)
        async def wrapper_async(*args: P.args, **kwargs: P.kwargs) -> Either[T, R]:
            try:
                return Success(await func(*args, **kwargs))
            except self._exceptions as e:
                return Failure(e)

        return wrapper_async
