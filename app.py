import random
import os
from utils import load_files, get_mint_id, count_accounts, get_possible_chains
from blockchain import mint_nft, bridge_nft, init_web3

# Load necessary data
hNFT_addresses, hFT_addresses, domains, alchemy_url_list, hNFT_abi, hFT_abi = load_files()

num_accounts = count_accounts()

accounts = [{
    'address': os.getenv(f'ADDRESS_{i+1}'),
    'private_key': os.getenv(f'PRIVATE_KEY_{i+1}')
} for i in range(num_accounts)]

# Function to randomize selection of chains and account details
def randomize_transaction_parameters():
    chains = get_possible_chains()
    starting_chain = random.choice(chains)
    destination_chain = random.choice([chain for chain in chains if chain != starting_chain])
    
    # Randomly select an account
    account = random.choice(accounts)
    account_address = account['address']
    private_key = account['private_key']
    
    return starting_chain, destination_chain, account_address, private_key

# Parametric function for transactions across chains, now with randomization
def execute_transaction(nft=True, amount=1):
    starting_chain, destination_chain, account_address, private_key = randomize_transaction_parameters()
    print(f"Starting chain: {starting_chain}")
    print(f"Destination chain: {destination_chain}")
    print(f"Account address: {account_address}")
    
    alchemy_url = alchemy_url_list[starting_chain]

    # Initialize web3
    web3 = init_web3(alchemy_url)  

    # Load contract addresses and ABIs based on whether it's NFT or FT
    if nft:
        contract_address = hNFT_addresses[starting_chain]
        contract_abi = hNFT_abi
    else:
        contract_address = hFT_addresses[starting_chain]
        contract_abi = hFT_abi
    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    starting_domain = domains[starting_chain]
    destination_domain = domains[destination_chain]

    if nft:
        tx_data = mint_nft(web3, contract, starting_domain, account_address, private_key, amount)
        tx_hash = tx_data['tx_hash']
        receipt = tx_data['receipt']
        print(f"Mint Transaction hash: {web3.to_hex(tx_hash)}")
        
        mintID = get_mint_id(receipt, starting_chain)
        bridge_tx_hash = bridge_nft(web3, contract, destination_domain, mintID, account_address, private_key)
        print(f"Bridge Transaction hash: {web3.to_hex(bridge_tx_hash)}")
    else:
        print("FT functionality not yet implemented")

# Example usage
execute_transaction(nft=True, amount=1)
