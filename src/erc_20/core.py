from pathlib import Path
from typing import Self, TYPE_CHECKING

from web3 import Web3
from web3.contract import Contract

from erc_20.exceptions import InvalidProviderError, ConnectionFailedError

if TYPE_CHECKING:
    from web3.providers import BaseProvider


class ERC20:
    abi: str | None
    bytecodes: str | None
    sol: str | None
    _w3: Web3
    _contract: type[Contract] | Contract

    def __init__(
        self: Self,
        *,
        provider: str,
        address: str | None = None,
        abi: str | Path | None = None,
        bytecodes: str | Path | None = None,
        sol: str | Path | None = None,
    ) -> None:
        _provider: BaseProvider
        if "http://" in provider or "https://" in provider:
            _provider = Web3.HTTPProvider(provider)
        elif "wss://" in provider:
            _provider = Web3.WebsocketProvider(provider)
        elif ".ipc" in provider:
            _provider = Web3.IPCProvider(provider)
        else:
            raise InvalidProviderError

        self._w3 = Web3(_provider)
        if not self._w3.is_connected():
            raise ConnectionFailedError

        if isinstance(abi, Path):
            with Path.open(abi) as f:
                self.abi = f.read()
        else:
            self.abi = abi

        if isinstance(bytecodes, Path):
            with Path.open(bytecodes) as f:
                self.bytecodes = f.read()
        else:
            self.bytecodes = bytecodes

        if isinstance(sol, Path):
            with Path.open(sol) as f:
                self.sol = f.read()
        else:
            self.sol = sol

        self._contract = self._w3.eth.contract(address=address, abi=self.abi)

    def balance(self: Self, address: str) -> int:
        return self._contract.functions.balanceOf(address).call()
