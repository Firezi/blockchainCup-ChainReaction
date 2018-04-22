from solc import compile_source
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
import time
from tradeFormation import operations
import pandas

from keys import publicKey
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

import requests
import json
import time

from addresses import contract_address

web3 = Web3(HTTPProvider('http://localhost:9545'))

contract_address = web3.toChecksumAddress(contract_address)

contract_fs = open('smart-contract/contracts/Trades.sol', 'r')
contract_source_code = ''.join(contract_fs.readlines())

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Trades']

instance = web3.eth.contract(abi=contract_interface['abi'], address=contract_address,
                             ContractFactoryClass=ConciseContract)

contract = web3.eth.contract(address=contract_address, abi=contract_interface['abi'])


def sendToBack(trade):
    trade = list(trade)
    if trade[1] == 'sell':
        trade[4] = -1 * trade[4]

    data = {"ticker": [trade[2]], "price": [trade[3] / 100], "quantity": [trade[4]],
            "comission": [trade[5] / 100], "time": [trade[6]], "address": [trade[0]]}
    print(data)

    url = 'http://192.168.43.46:3000/rawData'
    answer = requests.post(url, data=json.dumps(data), headers={'Content-type': 'application/json'})
    print(answer)


def removeAll():
    url = 'http://192.168.43.46:3000/removeOldData'
    answer = requests.post(url, data={})
    print(answer)
    time.sleep(2)


def checkSign(trade):
    # s = trade[1] + trade[2] + str(trade[3]) + str(trade[4]) + str(trade[5]) + str(trade[6])
    # print(s)
    # s = s.encode()
    # h = SHA256.new()
    # h.update(s)
    # try:
    #     pkcs1_15.new(publicKey).verify(h, trade[7])
    #     return True
    # except ValueError:
    #     print('Signature failed: ', trade)
    #     return False
    if trade[7] == "signature":
        return True
    print('Signature failed: ', trade)
    return False


last_count = 0


def getTrades():
    global last_count
    removeAll()
    while True:
        count = instance.getSize()
        for i in range(last_count, count):
            tr = instance.getTrade(i)
            if checkSign(tr):
                sendToBack(tr)
        last_count = count
        time.sleep(2)


getTrades()
