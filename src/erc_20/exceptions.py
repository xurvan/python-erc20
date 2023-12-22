from typing import Self


class InvalidProviderError(Exception):
    def __init__(self: Self) -> None:
        super().__init__("invalid provider")


class ConnectionFailedError(Exception):
    def __init__(self: Self) -> None:
        super().__init__("can not connect to the provider")
