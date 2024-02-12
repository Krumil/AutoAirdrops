import requests
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from utils import load_files, init_web3, estimate_gas_limit, estimate_gas_price

# Load necessary data
_, _, domains, alchemy_url_list, _, _, erc20_abi, lifi_chains = load_files()

def get_chain_key(chain_name):
	chain_name = chain_name.lower()
	# search for the chain name in the lifi_chains array
	for chain in lifi_chains:
		if chain['name'].lower() == chain_name:
			return chain['key']

def get_quote(starting_chain, destination_chain, from_token, to_token, from_amount, from_address):
	starting_domain = get_chain_key(starting_chain)
	destination_domain = get_chain_key(destination_chain)
	url = 'https://li.quest/v1/quote'
	params = {
		'fromChain': starting_domain,
		'toChain': destination_domain,
		'fromToken': from_token,
		'toToken': to_token,
		'fromAmount': from_amount,
		'fromAddress': from_address,
	}
	response = requests.get(url, params=params)
	return response.json()

def get_status(bridge, starting_chain, destination_chain, tx_hash):
	starting_domain = get_chain_key(starting_chain)
	destination_domain = get_chain_key(destination_chain)
	url = 'https://li.quest/v1/status'
	params = {
		'bridge': bridge,
		'fromChain': starting_domain,
		'toChain': destination_domain,
		'txHash': tx_hash,
	}
	response = requests.get(url, params=params)
	return response.json()

def check_and_set_allowance(web3, account_address, private_key, token_address, approval_address, amount, abi):
	zero_address ='0x0000000000000000000000000000000000000000'
	if token_address == zero_address:
		return

	contract = web3.eth.contract(address=token_address, abi=abi)
	current_allowance = contract.functions.allowance(account_address, approval_address).call()

	if current_allowance < amount:
		nonce = web3.eth.get_transaction_count(account_address)
		approve_tx = contract.functions.approve(approval_address, amount).buildTransaction({
			'from': account_address,
			'chainId': web3.eth.chainId,
			'nonce': nonce,
		})
		signed_tx = web3.eth.account.sign_transaction(approve_tx, private_key)
		tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
		web3.eth.wait_for_transaction_receipt(tx_hash)

def execute_swap(starting_chain, destination_chain, from_token, to_token, from_amount, account_address, private_key):
	alchemy_url = alchemy_url_list[starting_chain]
	web3 = init_web3(alchemy_url)	
	quote = get_quote(starting_chain, destination_chain, from_token, to_token, from_amount, account_address)
	check_and_set_allowance(web3, account_address, private_key, quote['action']['fromToken']['address'], quote['estimate']['approvalAddress'], from_amount, erc20_abi)
	
	nonce = web3.eth.get_transaction_count(account_address)

	gasPrice = estimate_gas_price(web3)
	gasLimit = estimate_gas_limit(web3, account_address, quote['transactionRequest']['to'], quote['transactionRequest']['data'], quote['transactionRequest']['value'])
	tx = {
		'from': account_address,
		'to': quote['transactionRequest']['to'],
		'value': quote['transactionRequest']['value'], # Convert hex to int
		'data': quote['transactionRequest']['data'],
		# 'gas': quote['transactionRequest']['gasLimit'],
		# 'gas': 21000000,
		'gas': gasLimit,
		'gasPrice': quote['transactionRequest']['gasPrice'],
		'nonce': nonce,
	}
	signed_tx = web3.eth.account.sign_transaction(tx, private_key)
	tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
	receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
	print(f"Transaction hash: {tx_hash.hex()}")
	print(f"Transaction receipt: {receipt}")


