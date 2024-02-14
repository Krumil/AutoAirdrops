from actions.merkly import execute_merkly_transaction
from actions.lifi import execute_swap, split_send_eth, execute_swap_ETH_to_USDC, execute_swap_all_USDC_to_ETH
from utils import randomize_transaction_parameters, convert_eth_to_wei, get_token_balance
import random

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


def random_swap_amount():
    return random.uniform(0.02, 0.04)  # Randomly select an amount between 0.01 and 0.1 ETH for swapping

def execute_random_swaps_on_path(chains, account_address, private_key):
    for chain in chains:
        amount_eth_to_usdc = random_swap_amount()  # Random amount for ETH to USDC swap
        amount_in_wei = convert_eth_to_wei(amount_eth_to_usdc)
        eth_to_usdc_receipt = execute_swap(chain, chain, 'ETH', 'USDC', amount_in_wei, account_address, private_key)
        print(f"Swapped {amount_eth_to_usdc} ETH to USDC on {chain}")

        # Wait for the swap to be completed and the balance to update
        # This step is simplified; in a real scenario, you should check the updated balance

        usdc_to_eth_receipt = execute_swap(chain, chain, 'USDC', 'ETH', amount_in_wei, account_address, private_key)
        print(f"Swapped back to ETH on {chain}")
        
chains = ['arbitrum', 'optimism', 'zksync_era', 'scroll']
execute_random_swaps_on_path(chains, account_address, private_key)
