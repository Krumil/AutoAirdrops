from web3 import Web3
from utils import load_files, get_mint_id, randomize_transaction_parameters, init_web3

hNFT_addresses, hFT_addresses, domains, alchemy_url_list, hNFT_abi, hFT_abi, _, _ = load_files()

def mint_nft(web3, contract, starting_domain, account_address, private_key, amount=1):
	# Minting NFT
	fee = contract.functions.fee().call()
	nonce = web3.eth.get_transaction_count(account_address)
	tx_dict = {
		'from': account_address,
		'chainId': starting_domain,  # Use the appropriate chain ID
		'nonce': nonce,
		'value': fee * amount  # Adjust based on the fee and amount
	}
	tx = contract.functions.mint(amount).build_transaction(tx_dict)
	
	# Sign and send the transaction
	signed_tx = web3.eth.account.sign_transaction(tx, private_key)
	tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
	receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
	return {'tx_hash': tx_hash, 'receipt': receipt}

def bridge_nft(web3, contract, destination_domain, mintID, account_address, private_key):
	quote = contract.functions.quoteBridge(destination_domain).call()
	bridge_tx = contract.functions.bridgeNFT(destination_domain, mintID).build_transaction({
		'from': account_address,
		'nonce': web3.eth.get_transaction_count(account_address),
		'value': quote
	})
	
	signed_bridge_tx = web3.eth.account.sign_transaction(bridge_tx, private_key)
	bridge_tx_hash = web3.eth.send_raw_transaction(signed_bridge_tx.rawTransaction)
	return bridge_tx_hash

def execute_merkly_transaction(nft=True, amount=1, starting_chain=None, destination_chain=None, account_address=None, private_key=None):
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