from typing import Union

from py_fp_playground.either import EitherMonad, Either, monadic


@monadic
def program(
    do: EitherMonad[Union[EOFError, KeyboardInterrupt]]
) -> str:
    # res = sub_program()
    # res2 = res.fold(
    #     lambda e: Either.right(1),
    #     lambda s: Either.right("good"),
    # )
    name = do << sub_program().either_fold(
        lambda e: Either.right(1),
        lambda s: Either.right("good"),
    )
    good_name = do << sub_program().map_left(lambda e: EOFError())
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
    do: EitherMonad[Union[ValueError, NotImplementedError]]
) -> str:
    x = do << Either.right(1)
    # y = do << Either.left(NotImplementedError("Not implemented"))
    # raise NotImplementedError("Not implemented")
    y = do << Either.right(2)
    return f"{x} + {y} = {x + y}"


final_result = program().get_or_else(1)
print(f"Final result (1) is: {final_result}")

