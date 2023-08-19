from dataclasses import dataclass
from typing import TypeVar, Generic, ParamSpec, NoReturn, Union, Type, Optional, Callable

from ziopy.either import Either as _Either, EitherMonad as _EitherMonad
from ziopy.util import raise_exception

A = TypeVar('A', covariant=True)
A1 = TypeVar('A1')
A2 = TypeVar('A2')
AA = TypeVar('AA')
A_con = TypeVar("A_con", contravariant=True)

B = TypeVar('B', covariant=True)
B1 = TypeVar('B1')
B2 = TypeVar('B2')
BB = TypeVar('BB')

C = TypeVar('C')
C1 = TypeVar('C1')
C2 = TypeVar('C2')

E = TypeVar('E', covariant=True)
E1 = TypeVar('E1')
E2 = TypeVar('E2')
E_con = TypeVar('E_con', contravariant=True)

X = TypeVar('X', bound=BaseException)
P = ParamSpec("P")
PP = ParamSpec("PP")


class Either(Generic[A, B], _Either[A, B]):

    # New methods

    def get(self) -> B:
        return self.fold(
            lambda e: raise_exception(e),
            lambda a: a
        )

    def get_or_else(self, default: C) -> B | C:
        return self.fold(
            lambda e: default,
            lambda a: a
        )

    # Below are existing methods with updated type signatures

    @staticmethod
    def left(a: AA) -> "Either[AA, NoReturn]":
        return Left(a)

    @staticmethod
    def right(b: BB) -> "Either[NoReturn, BB]":
        return Right(b)

    @staticmethod
    def from_union(
            value: Union[A, B],
            left_type: Type[A],
            right_type: Type[B]
    ) -> "Either[A, B]":
        if isinstance(value, left_type):
            return Either.left(value)
        elif isinstance(value, right_type):
            return Either.right(value)
        else:
            raise TypeError()

    @staticmethod
    def from_optional(value: Optional[B]) -> "Either[None, B]":
        if value is None:
            return Either.left(value)
        return Either.right(value)

    def to_left(self: "Either[AA, NoReturn]") -> "Left[AA]":
        if not isinstance(self, Left):
            raise TypeError("to_left can only be called on an instance of Left.")
        return self

    def to_right(self: "Either[NoReturn, BB]") -> "Right[BB]":
        if not isinstance(self, Right):
            raise TypeError("to_right can only be called on an instance of Right.")
        return self

    def match(
            self,
            case_left: "Callable[[Left[A]], C1]",
            case_right: "Callable[[Right[B]], C2]"
    ) -> Union[C1, C2]:
        if isinstance(self, Left):
            return case_left(self)
        elif isinstance(self, Right):
            return case_right(self)
        else:
            raise TypeError()

    def fold(
            self,
            case_left: "Callable[[A], C1]",
            case_right: "Callable[[B], C2]"
    ) -> Union[C1, C2]:
        return self.match(
            lambda x: case_left(x.value),
            lambda y: case_right(y.value)
        )

    def swap(self) -> "Either[B, A]":
        return self.match(
            lambda left: Either.right(left.value),
            lambda right: Either.left(right.value)
        )

    def map(self, f: Callable[[B], C]) -> "Either[A, C]":
        return self.match(
            lambda left: left,
            lambda right: Either.right(f(right.value))
        )

    def map_left(self, f: Callable[[A], C]) -> "Either[C, B]":
        return self.match(
            lambda left: Either.left(f(left.value)),
            lambda right: right
        )

    def flat_map(self, f: "Callable[[B], Either[AA, C]]") -> "Either[Union[A, AA], C]":
        return self.match(
            lambda left: left,
            lambda right: f(right.value)
        )

    def __lshift__(self, f: "Callable[[B], Either[AA, C]]") -> "Either[Union[A, AA], C]":
        return self.flat_map(f)

    def flatten(self: "Either[A1, Either[AA, BB]]") -> "Either[Union[A1, AA], BB]":
        return self.flat_map(lambda x: x)

    def require(
            self,
            predicate: Callable[[B], bool],
            to_error: Callable[[B], AA]
    ) -> "Either[Union[A, AA], B]":
        def _case_right(right: Right[B]) -> "Either[Union[A, AA], B]":
            if predicate(right.value):
                return right
            return Either.left(to_error(right.value))

        return self.match(
            lambda left: left,
            _case_right
        )

    def asserting(
            self,
            predicate: Callable[[B], bool],
            to_error: Callable[[B], X]
    ) -> "Either[A, B]":
        def _case_right(right: Right[B]) -> "Either[A, B]":
            if not predicate(right.value):
                raise to_error(right.value)
            return right

        return self.match(
            lambda left: left,
            _case_right
        )

    def raise_errors(self: "Either[AA, BB]") -> "Either[NoReturn, BB]":
        def _case_left(error: AA) -> NoReturn:
            if isinstance(error, Exception):
                raise error from error
            else:
                raise EitherException(value=error)

        return self.fold(_case_left, lambda x: Either.right(x))

    def tap(self, op: "Callable[[Either[A, B]], Any]") -> "Either[A, B]":
        op(self)
        return self

    def display(self, description: Optional[str] = None) -> "Either[A, B]":
        if description is not None:
            print(f"{description}:")
        return self.tap(print)

    def to_union(self) -> Union[A, B]:
        return self.match(lambda x: x.value, lambda y: y.value)

    def cast(self: "Either[AA, BB]", t: Type[C]) -> "Either[Union[AA, TypeError], C]":
        return self.flat_map(
            lambda b: Either.right(b) if isinstance(b, t)
            else Either.left(
                TypeError(f"Unable to cast value {b} (of type {type(b).__name__}) as type {t.__name__}.")
            )
        )


@dataclass(frozen=True)
class Left(Generic[A], Either[A, NoReturn]):
    value: A


@dataclass(frozen=True)
class Right(Generic[B], Either[NoReturn, B]):
    value: B

class EitherMonad(Generic[E_con], _EitherMonad[E_con]):
    def __lshift__(self, arg: Either[E_con, BB]) -> BB:
        return arg.get()
