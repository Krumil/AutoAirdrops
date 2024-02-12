from actions.merkly import mint_nft, bridge_nft, init_web3, execute_merkly_transaction
from actions.lifi import execute_swap
from utils import randomize_transaction_parameters
import time
import os

starting_chain, destination_chain, account_address, private_key = randomize_transaction_parameters()
starting_chain = "arbitrum"
destination_chain = "optimism"
print(f"Starting chain: {starting_chain}")
print(f"Destination chain: {destination_chain}")
print(f"Account address: {account_address}")


# execute_merkly_transaction(nft=True, amount=1, starting_chain=starting_chain, destination_chain=destination_chain, account_address=account_address, private_key=private_key)
execute_swap(starting_chain, destination_chain, "ETH", "ETH", 1000000000000000, account_address, private_key)