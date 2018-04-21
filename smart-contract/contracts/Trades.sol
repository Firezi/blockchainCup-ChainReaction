pragma solidity ^0.4.21;

contract Trades {
	address public owner;

	struct Trade {
		address trader;
		string tradeType; // buy or sell
		string shareName;
		uint cost; // * 100
		uint count;
		uint comission;
		uint time;
		string signature;
	}

	mapping (address => bool) public isTrader;
	Trade[] public tradesList;

	modifier onlyOwner() {
		require(msg.sender == owner);
		_;
	}

	modifier onlyTrader() { 
		require (isTrader[msg.sender]); 
		_; 
	}
	
	event NewTrade(address trader, string tradeType, string shareName, uint cost, uint count, uint comission, uint time, string signature);

	function Trades() public {
		owner = msg.sender;
	}

	function verifyTrader(address _trader) onlyOwner public {
		isTrader[_trader] = true;
	}


	function addTrade(string _type, string _shareName, uint _cost, uint _count, uint _comission, uint _time, string _signature) onlyTrader public {
		tradesList.push(Trade({
				trader: msg.sender,
				tradeType: _type,
				shareName: _shareName,
				cost: _cost,
				count: _count,
				comission: _comission,
				time: _time,
				signature: _signature
			}));

		emit NewTrade(msg.sender, _type, _shareName, _cost, _count, _comission, _time, _signature);
	}


	function getSize() public constant returns (uint) {
		return tradesList.length;
	}

	function getTrade(uint index) public constant returns (address, string, string, uint, uint, uint, uint) {
		return (tradesList[index].trader, tradesList[index].tradeType, tradesList[index].shareName, tradesList[index].cost,
				tradesList[index].count, tradesList[index].comission, tradesList[index].time);
	}
}