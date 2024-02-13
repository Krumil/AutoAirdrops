from actions.merkly import execute_merkly_transaction
from actions.lifi import execute_swap, split_send_eth
from utils import randomize_transaction_parameters, convert_eth_to_wei

starting_chain, destination_chain, account_address, private_key = randomize_transaction_parameters()
starting_chain = "zksync_era"
destination_chains = ["arbitrum","optimism"]
print(f"Starting chain: {starting_chain}")
print(f"Destination chain: {destination_chain}")
print(f"Account address: {account_address}")


# execute_merkly_transaction(nft=True, amount=1, starting_chain=starting_chain, destination_chain=destination_chain, account_address=account_address, private_key=private_key)

min_eth = 0.04

# execute_swap(starting_chain, destination_chain, "ETH", "ETH", convert_eth_to_wei(min_eth), account_address, private_key)
split_send_eth(starting_chain, destination_chains, "ETH", "ETH", min_eth, account_address, private_key)