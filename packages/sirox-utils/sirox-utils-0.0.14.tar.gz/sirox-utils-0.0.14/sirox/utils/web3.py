import json
from typing import List


def read_abi(address: str, path: str = None) -> str:
    if not path:
        path = "abis"
    with open(f"{path}/{address.lower()}.json", "r") as file:
        abi = json.loads(file.read())
    return abi


def encode_fn_data(w3, contract_address: str, fn_name: str, fn_args: List):
    contract_instance = w3.eth.contract(
        address=contract_address, abi=read_abi(contract_address)
    )
    return contract_instance.encodeABI(fn_name=fn_name, args=fn_args)
