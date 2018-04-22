from solc import compile_source
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# from keys import privateKey
# from Crypto.Hash import SHA256
# from Crypto.Signature import pkcs1_15

from addresses import contract_address, trader_address

web3 = Web3(HTTPProvider('http://localhost:9545'))

contract_address = web3.toChecksumAddress(contract_address)
trader_address = web3.toChecksumAddress(trader_address)

contract_fs = open('smart-contract/contracts/Trades.sol', 'r')
contract_source_code = ''.join(contract_fs.readlines())

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Trades']

instance = web3.eth.contract(abi=contract_interface['abi'], address=contract_address,
                             ContractFactoryClass=ConciseContract)


def push(_type, _shareName, _cost, _count, _comission, _time):
    # s = _type + _shareName + str(_cost) + str(_count) + str(_comission) + str(_time)
    # s = s.encode()
    # h = SHA256.new()
    # h.update(s)
    # signature = pkcs1_15.new(privateKey).sign(h)

    instance.addTrade(_type, _shareName, int(_cost * 100), _count, int(_comission * 100), _time, "signature", transact={'from': trader_address})

import random

for i in range (0, 5):
    print('verify')
    instance.verifyTrader(trader_address, transact={'from': web3.eth.accounts[0]})
    print('buy')
    push('buy', 'SBR', 1000 + random.randint(1, 1000), i , 1.5, 1524377610 + i)
    print('sell')
    push('buy', 'SBR', 1000 + random.randint(1, 1000), i, 1.5, 1524378610 + i)

