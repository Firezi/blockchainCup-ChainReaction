from solc import compile_source
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

web3 = Web3(HTTPProvider('http://localhost:9545'))

contract_address = "0x345ca3e014aaf5dca488057592ee47305d9b3e10"
trader_address = "0xf17f52151ebef6c7334fad080c5704d77216b732"

contract_address = web3.toChecksumAddress(contract_address)
trader_address = web3.toChecksumAddress(trader_address)

contract_fs = open('smart-contract/contracts/Trades.sol', 'r')
contract_source_code = ''.join(contract_fs.readlines())

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Trades']

instance = web3.eth.contract(abi=contract_interface['abi'], address=contract_address,
                             ContractFactoryClass=ConciseContract)


def push(_type, _shareName, _cost, _count, _comission, _time, _signature):
    instance.addTrade(_type, _shareName, int(_cost * 100), _count, int(_comission * 100), _time, _signature, transact={'from': trader_address})


# push('sell', 'SBR', 100.23, 1, 1.01, 123, 'sign')
