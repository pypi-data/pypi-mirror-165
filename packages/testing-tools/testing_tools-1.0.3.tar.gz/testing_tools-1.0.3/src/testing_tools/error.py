from contextlib import nullcontext as does_not_raise


class TestingToolsError(Exception):
    pass


__all__ = [
    does_not_raise,
    TestingToolsError,
]
