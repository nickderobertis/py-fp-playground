from typing import TypeVar

from py_fp_playground.either import Either

T = TypeVar('T', covariant=True)

Nothing = Either.left(None)
Some = Either.right
Option = Either[None, T]
