import asyncio
from typing import Callable, Union, Awaitable

# from fn import _

from py_fp_playground.scalambda import _

from py_fp_playground.either import EitherMonad, Either, monadic, Left, Right
from py_fp_playground.option import Some, Nothing, Option


@monadic
async def program(do: EitherMonad[Union[EOFError, KeyboardInterrupt]]) -> str:
    # res = sub_program()
    # res2 = res.fold(
    #     lambda e: Either.right(1),
    #     lambda s: Either.right("good"),
    # )
    # name = do << sub_program().either_fold(
    #     lambda e: Either.right(1),
    #     lambda s: Either.right("good"),
    # )
    good_name = do << (await sub_program(Some(15))).map_left(lambda e: EOFError())
    x = 1

    add_one: Callable[[int], int] = _ + 1

    while x < 20:
        x = do << (
            Either.right(x)
            .map(add_one)
            .map(_ + 2)
            .flat_map(lambda q: Either.right(q - 1))
            .flat_map(lambda r: Either.right(r + 1))
        )
        print(f"The value of x is: {x}")

    return f"Hello, {good_name}!"


@monadic
async def sub_program(
    do: EitherMonad[Union[ValueError, NotImplementedError, None]],
    something: Option[int] = Nothing,
) -> str:
    x = do << Some(2)
    await asyncio.sleep(0.2)
    print(f"{x=}")
    z = do << something
    print(f"{z=}")
    # y = do << Either.left(NotImplementedError("Not implemented"))
    # raise NotImplementedError("Not implemented")
    y = do << Some(4)
    print(f"{y=}")
    return f"{x} + {y} = {x + y}"


async def temp():
    await asyncio.sleep(0.1)
    return "hello"


temp_coro: Awaitable[str] = temp()

print(asyncio.run(temp_coro))
final_result = asyncio.run(program()).get_or_else(1)
print(f"Final result (1) is: {final_result}")