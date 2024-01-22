import math

from web3 import Web3
import random
import json


#rpc_url = "http://localhost:8545" #Set this to a node that you can connect to (e.g. an Alchemy node)
rpc_url = "https://mainnet.infura.io/v3/7d971d5755d142b49329f02a8bfd5d72"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
	pass
else:
	print( "Failed to connect to Ethereum node!" )


"""
	Takes a block number
	Returns a boolean that tells whether all the transactions in the block are ordered by priority fee

	Before EIP-1559, a block is ordered if and only if all transactions are sorted in decreasing order of the gasPrice field

	After EIP-1559, there are two types of transactions
		*Type 0* The priority fee is tx.gasPrice - block.baseFeePerGas
		*Type 2* The priority fee is min( tx.maxPriorityFeePerGas, tx.maxFeePerGas - block.baseFeePerGas )

	Conveniently, most type 2 transactions set the gasPrice field to be min( tx.maxPriorityFeePerGas + block.baseFeePerGas, tx.maxFeePerGas )
"""
def is_ordered_block(block_num):
    block = w3.eth.get_block(block_num)
    ordered = True
    prev = math.inf
    
    #YOUR CODE HERE
    transactions = block.transactions
    for tx in transactions:
        curr_tx = w3.eth.get_transaction(tx)
        if(curr_tx.type != 2):
            if curr_tx.gasPrice > prev:
                return False
            else:
                prev = curr_tx.gasPrice
        else:
            total_fee = min(curr_tx.maxPriorityFeePerGas + curr_tx.baseFeePerGas, curr_tx.maxFeePerGas)
            if total_fee > prev:
                return False
            else:
                prev = total_fee
        #print(w3.eth.get_transaction(tx).type)

    return ordered

print(is_ordered_block(12965000))

"""
	This might be useful for testing

if __name__ == "__main__":
	latest_block = w3.eth.get_block_number()

	london_hard_fork_block_num = 12965000
	assert latest_block > london_hard_fork_block_num, f"Error: the chain never got past the London Hard Fork"

	n = 5

	for _ in range(n):
        #Pre-London
		block_num = random.randint(1,london_hard_fork_block_num-1)
		ordered = is_ordered_block(block_num)
		if ordered:
			print( f"Block {block_num} is ordered" )
		else:
			print( f"Block {block_num} is ordered" )

        #Post-London
		block_num = random.randint(london_hard_fork_block_num,latest_block)
		ordered = is_ordered_block(block_num)
		if ordered:
			print( f"Block {block_num} is ordered" )
		else:
			print( f"Block {block_num} is ordered" )
"""
