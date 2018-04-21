from solc import compile_source
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
import time
from tradeFormation import operations
import pandas

web3 = Web3(HTTPProvider('http://localhost:9545'))

contract_address = "0x345ca3e014aaf5dca488057592ee47305d9b3e10"

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
	newdeal = pandas.DataFrame({"ticker": [trade[2]], "price": [trade[3]], "quantity": [trade[4] / 100],
		                        "comission": [trade[5]], "time": [trade[6]], "address": [trade[0]]})
	operations(newdeal)


last_count = 0;

def getTrades():
    global last_count
    while True:
        count = instance.getSize()
        for i in range(last_count, count):
            sendToBack(instance.getTrade(i))
        last_count = count
        time.sleep(2)


getTrades()
