from typing import NoReturn, Union

import ziopy.services.console as console
import ziopy.services.system as system
from ziopy.either import EitherArrow
from ziopy.environments import ConsoleSystemEnvironment
from ziopy.services.console import Console, LiveConsole
from ziopy.either import Either, EitherMonad, monadic
from ziopy.zio import unsafe_run


@monadic
def program(
    do: EitherMonad[Union[EOFError, KeyboardInterrupt]]
) -> Either[
    Union[EOFError, KeyboardInterrupt],
    str
]:
    # name = do << sub_program().fold(
    #     lambda e: Either.right(1),
    #     lambda s: Either.right("good"),
    # )
    name = do << sub_program()
    print(f"Your name is: {name}")
    x = do << Either.right(1)

    while x < 20:
        x = do << (
            Either.right(x)
            .map(lambda p: p + 1)
            .flat_map(lambda q: Either.right(q - 1))
            .flat_map(lambda r: Either.right(r + 1))
        )

    print(f"The value of x is: {x}")
    return Either.right(f"Hello, {name}!")


@monadic
def sub_program(
    do: EitherMonad[Union[ValueError, NotImplementedError]]
) -> Either[
    Union[ValueError, NotImplementedError],
    str
]:
    x = do << Either.right(1)
    y = do << Either.left(NotImplementedError("Not implemented"))
    return Either.right(f"{x} + {y} = {x + y}")


final_result = program().to_union()
print(f"Final result (1) is: {final_result}")

