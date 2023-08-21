import types
import typing
from functools import wraps, cached_property
from typing import TypeVar, ParamSpec, Callable, Union, Generic
from typing_extensions import TypeVarTuple, Unpack

from py_fp_playground.either import Either

E = TypeVar("E", bound=BaseException)
E2 = TypeVar("E2", bound=BaseException)
# ET = TypeVar("ET", bound=type[BaseException] | Union[type[BaseException], ...])
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
        return typing.get_args(self.__orig_class__)[0]

    @cached_property
    def _exceptions(self) -> tuple[type[BaseException], ...]:
        if isinstance(self._exception_type, types.UnionType):
            exceptions = typing.get_args(self._exception_type)
        elif issubclass(self._exception_type, BaseException):
            exceptions = (self._exception_type,)
        else:
            raise TypeError(
                f"Expected an exception type, got {self._exception_type}."
            )
        return exceptions

    def __call__(self, func: Callable[P, R]) -> Callable[P, Either[T, R]]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Either[T, R]:
            try:
                return Success(func(*args, **kwargs))
            except self._exceptions as e:
                return Failure(e)

        return wrapper
