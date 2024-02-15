import random

from actions.merkly import execute_merkly_transaction
from actions.lifi import execute_swap, split_send_eth, execute_swap_ETH_to_USDC, execute_swap_all_USDC_to_ETH
from utils import randomize_transaction_parameters, convert_eth_to_wei, get_token_balance, convert_wei_to_eth

starting_chain, destination_chain, account_address, private_key = randomize_transaction_parameters()
# starting_chain = "zksync_era"
# starting_chain = "arbitrum"
# destination_chains = ["arbitrum","optimism"]
# print(f"Starting chain: {starting_chain}")
# print(f"Destination chain: {destination_chain}")
# print(f"Account address: {account_address}")


# min_eth = 0.02
# execute_merkly_transaction(nft=True, amount=1, starting_chain=starting_chain, destination_chain=destination_chain, account_address=account_address, private_key=private_key)
# execute_swap(starting_chain, destination_chain, "ETH", "ETH", convert_eth_to_wei(min_eth), account_address, private_key)
# split_send_eth(starting_chain, destination_chains, "ETH", "ETH", min_eth, account_address, private_key)
# execute_swap_ETH_to_USDC(starting_chain,account_address, private_key, convert_eth_to_wei(min_eth))
# execute_swap_all_USDC_to_ETH(starting_chain, account_address, private_key)


def random_swap_amount(chain, account_address):
	eth_balance = get_token_balance(chain, account_address, "ETH")
	max_eth_to_swap = eth_balance * 0.8
	min_eth_to_swap = eth_balance * 0.2
	max_eth_to_swap = int(max_eth_to_swap)
	min_eth_to_swap = int(min_eth_to_swap)
	amount_in_wei = random.randint(min_eth_to_swap, max_eth_to_swap)
	return amount_in_wei

def execute_random_swaps_on_path(chains, account_address, private_key):
	for chain in chains:
		amount_in_wei = random_swap_amount(chain, account_address)  
		amount_eth_to_usdc = convert_wei_to_eth(amount_in_wei)
		print(f"Swapping {amount_eth_to_usdc} ETH to USDC on {chain}")
		execute_swap_ETH_to_USDC(chain,account_address, private_key, amount_in_wei)
		print(f"Swapped {amount_eth_to_usdc} ETH to USDC on {chain}")
		execute_swap_all_USDC_to_ETH(chain, account_address, private_key)
		print(f"Swapped back to ETH on {chain}")
		if chain != chains[-1]:
			eth_balance_in_wei = get_token_balance(chain, account_address, "ETH")
			eth_balance = convert_wei_to_eth(eth_balance_in_wei)
			if eth_balance < 0.02:
				print(f"Not enough ETH to bridge to {chains[chains.index(chain) + 1]}")
				continue


			next_chain = chains[chains.index(chain) + 1]
			print(f"Bridging {amount_eth_to_usdc} ETH to {next_chain}")
			execute_swap(chain, next_chain, "ETH", "ETH", amount_in_wei, account_address, private_key)
			print(f"Bridged ETH to {next_chain}")
		
chains = ['arbitrum', 'optimism', 'base', 'scroll']
execute_random_swaps_on_path(chains, account_address, private_key)
