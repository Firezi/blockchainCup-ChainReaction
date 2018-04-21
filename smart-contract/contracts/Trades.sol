pragma solidity ^0.4.21;

contract Trades {
	address public owner;

	struct Trade {
		address trader;
		bool tradeType; // 0 - buy, 1 - sell
		string shareName;
		uint cost; // * 100
		uint count;
		uint time;
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
	
	event NewTrade(address trader, bool _type, string shareName, uint cost, uint count, uint time);

	function Trades() public {
		owner = msg.sender;
	}

	function verifyTrader(address _trader) onlyOwner public {
		isTrader[_trader] = true;
	}


	function addTrade(bool _type, string _shareName, uint _cost, uint _count, uint _time) onlyTrader public {
		tradesList.push(Trade({
				trader: msg.sender,
				tradeType: _type,
				shareName: _shareName,
				cost: _cost,
				count: _count,
				time: _time
			}));

		emit NewTrade(msg.sender, _type, _shareName, _cost, _count, _time);
	}


	function getSize() public constant returns (uint) {
		return tradesList.length;
	}

	function getTrade(uint index) public constant returns (address, bool, string, uint, uint, uint) {
		return (tradesList[index].trader, tradesList[index].tradeType, tradesList[index].shareName, tradesList[index].cost,
				tradesList[index].count, tradesList[index].time);
	}
}