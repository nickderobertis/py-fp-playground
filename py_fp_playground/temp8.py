from typing import Union

from py_fp_playground.either import EitherMonad, Either, monadic, Left, Right
from py_fp_playground.option import Some, Nothing, Option


@monadic
def program(
    do: EitherMonad[Union[EOFError, KeyboardInterrupt]]
) -> str:
    # res = sub_program()
    # res2 = res.fold(
    #     lambda e: Either.right(1),
    #     lambda s: Either.right("good"),
    # )
    # name = do << sub_program().either_fold(
    #     lambda e: Either.right(1),
    #     lambda s: Either.right("good"),
    # )
    good_name = do << sub_program(Some(15)).map_left(lambda e: EOFError())
    match sub_program(Some(10)):
        case Left(x):
            print(f"Error: {x}")
        case Right(x):
            print(f"Success: {x}")
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


@monadic
def sub_program(
    do: EitherMonad[Union[ValueError, NotImplementedError, None]],
        something: Option[int] = Nothing
) -> str:
    x = do << Some(2)
    print(f"{x=}")
    z = do << something
    print(f"{z=}")
    # y = do << Either.left(NotImplementedError("Not implemented"))
    # raise NotImplementedError("Not implemented")
    y = do << Some(4)
    print(f"{y=}")
    return f"{x} + {y} = {x + y}"


final_result = program().get_or_else(1)
print(f"Final result (1) is: {final_result}")

