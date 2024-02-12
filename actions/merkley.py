from web3 import Web3

# Initialize web3 with Alchemy provider
def init_web3(provider_url):
	return Web3(Web3.HTTPProvider(provider_url))

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