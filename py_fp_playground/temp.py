from expression import effect, Some, Nothing


@effect.option()
def fn() -> int:
    # x = yield from Nothing  # or a function returning Nothing
    x = yield from Some(42)

    # -- The rest of the function will never be executed --
    y = yield from Some(43)

    return x + y


xs = fn()
assert xs is Nothing
