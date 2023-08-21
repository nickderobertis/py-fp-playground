import asyncio
from typing import Union, Awaitable

from py_fp_playground.either import EitherMonad, Either, monadic, Left, Right
from py_fp_playground.option import Some, Nothing, Option
from py_fp_playground.catch import catch


@monadic
async def program(do: EitherMonad[ValueError | NotImplementedError | EOFError]) -> str:
    # res = sub_program()
    # res2 = res.fold(
    #     lambda e: Either.right(1),
    #     lambda s: Either.right("good"),
    # )
    # name = do << sub_program().either_fold(
    #     lambda e: Either.right(1),
    #     lambda s: Either.right("good"),
    # )
    good_name = do << (await sub_program2(Some(15))).map_left(lambda e: EOFError())
    match sub_program(Some(10)):
        case Left(x):
            print(f"Error: {x}")
        case Right(x):
            print(f"Success: {x}")
    something = sub_program()
    something2 = await sub_program2()

    bad_name = do << sub_program()
    print(f"Your name is: {good_name}")
    wut = Either.left(NotImplementedError("Not implemented"))
    x = do << wut

    while x < 20:
        x = do << (
            Either.right(x)
            .map(lambda p: p + 1)
            .flat_map(lambda q: Either.right(q - 1))
            .flat_map(lambda r: Either.right(r + 1))
        )

    print(f"The value of x is: {x}")
    return f"Hello, {good_name}!"


catcher = catch[ValueError | NotImplementedError]()


@catch[ValueError | NotImplementedError]()
def sub_program(something: Option[int] = Nothing) -> str:
    x = 2
    print(f"{x=}")
    raise ValueError("Wut?")
    return "yeah baby"


@catcher
async def sub_program2(something: Option[int] = Nothing) -> str:
    x = 2
    print(f"{x=}")
    # raise ValueError("Wut?")
    return "yeah baby"


async def temp():
    await asyncio.sleep(0.1)
    return "hello"


temp_coro: Awaitable[str] = temp()

print(asyncio.run(temp_coro))
final_result = asyncio.run(program())
print(f"Final result (1) is: {final_result}")
