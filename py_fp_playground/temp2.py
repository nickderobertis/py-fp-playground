from typing import NoReturn, Union

import ziopy.services.console as console
import ziopy.services.system as system
from ziopy.either import EitherArrow
from ziopy.environments import ConsoleSystemEnvironment
from ziopy.services.console import Console, LiveConsole
from ziopy.zio import ZIO, Environment, ZIOMonad, monadic, unsafe_run


@monadic
def program(
    do: ZIOMonad[object, Union[EOFError, KeyboardInterrupt]]
) -> ZIO[
    Console,
    Union[EOFError, KeyboardInterrupt],
    str
]:
    con = do << Environment[Console]()

    do << con.print("Hello, what is your name?")
    name = do << sub_program().catch(NotImplementedError)
    do << con.print(f"Your name is: {name}")
    x = do << ZIO.succeed(1)

    while x < 20:
        x = do << (
            ZIO.succeed(x)
            .map(lambda p: p + 1)
            .flat_map(lambda q: ZIO.succeed(q - 1))
            .flat_map(lambda r: ZIO.succeed(r + 1))
        )

    do << con.print(f"The value of x is: {x}")
    return ZIO.succeed(f"Hello, {name}!")


@monadic
def sub_program(
    do: ZIOMonad[object, Union[ValueError, NotImplementedError]]
) -> ZIO[
    object,
    Union[ValueError, NotImplementedError],
    str
]:
    x = do << ZIO.succeed(1)
    y = do << ZIO.fail(NotImplementedError("Not implemented"))
    return ZIO.succeed(f"{x} + {y} = {x + y}")


p = program().provide(LiveConsole())
final_result = unsafe_run(p)
print(f"Final result (1) is: {final_result}")

