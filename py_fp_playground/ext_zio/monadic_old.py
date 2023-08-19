import functools
from typing import Concatenate, Callable, TypeVar, ParamSpec, cast

from ziopy.either import Either, EitherMonad

A = TypeVar('A', covariant=True)
E = TypeVar('E', covariant=True)
P = ParamSpec("P")

def monadic(
    func: Callable[Concatenate[EitherMonad[E], P], A]
) -> Callable[P, Either[E, A]]:
    @functools.wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> Either[E, A]:
        try:
            return Either.right(func(EitherMonad(), *args, **kwargs))
        except Exception as e:
            return Either.left(cast(E, e))
    return _wrapper