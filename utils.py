from web3 import Web3
import dotenv
import json
import os 
import random
import requests

dotenv.load_dotenv()

def get_possible_chains():
	return ['arbitrum','base', 'optimism', 'polygon_zk', 'scroll', 'zksync_era']  

def get_chain_key(chain_name):
	chain_name = chain_name.lower()
	lifi_chains = json.load(open('lifi-chains.json'))
	for chain in lifi_chains:
		if chain['name'].lower() == chain_name:
			return chain['key']
		
def get_chain_id(chain_name):
	chain_name = chain_name.lower()
	lifi_chains = json.load(open('lifi-chains.json'))
	for chain in lifi_chains:
		if chain['name'].lower() == chain_name:
			return chain['id']
		
def convert_eth_to_wei(amount_eth):
	return Web3.to_wei(amount_eth, 'ether')


def count_accounts():
	count = 0
	while True:
		address_key = f'ADDRESS_{count + 1}'
		private_key = f'PRIVATE_KEY_{count + 1}'
		if os.getenv(address_key) and os.getenv(private_key):
			count += 1
		else:
			break
	return count

def get_accounts():
	num_accounts = count_accounts()
	accounts = [{
		'address': os.getenv(f'ADDRESS_{i+1}'),
		'private_key': os.getenv(f'PRIVATE_KEY_{i+1}')
	} for i in range(num_accounts)]
	return accounts

def get_mint_id(receipt, network):
	mintIDHex = b''
	if network == "Polygon":
		mintIDHex = receipt.logs[1].topics[3] if len(receipt.logs) > 1 else b''
	elif len(receipt.logs) == 1:
		mintIDHex = receipt.logs[0].topics[3]
	else:
		mintIDHex = receipt.logs[2].topics[3] if len(receipt.logs) > 2 else b''
	
	# Convert the byte array to an integer
	if mintIDHex:
		# Ensure mintIDHex is a bytes object, not a hex string
		if isinstance(mintIDHex, str):
			mintIDHex = bytes.fromhex(mintIDHex[2:])  # Remove '0x' prefix and convert
		mintID = int.from_bytes(mintIDHex, byteorder='big')
	else:
		mintID = None
	return mintID

def load_files():
	hNFT_addresses = json.load(open('hNFT-addresses.json'))
	hFT_addresses = json.load(open('hFT-addresses.json'))
	domains = json.load(open('domains.json'))
	hNFT_abi = json.load(open('abi/hNFT-abi.json'))
	hFT_abi = json.load(open('abi/hFT-abi.json'))
	erc20_abi = json.load(open('abi/lifi-erc20-abi.json'))
	lifi_chains = json.load(open('lifi-chains.json'))
	
	networks = get_possible_chains()
	alchemy_url_list = {chain: os.getenv(f'{chain.upper()}_URL') for chain in networks}
	
	return hNFT_addresses, hFT_addresses, domains, alchemy_url_list, hNFT_abi, hFT_abi, erc20_abi, lifi_chains

# Initialize web3 with Alchemy provider
def init_web3(provider_url):
	return Web3(Web3.HTTPProvider(provider_url))

# Function to read ABI from a local file
def load_abi(file_path):
	with open(file_path, 'r') as file:
		return json.load(file)


# Function to randomize selection of chains and account details
def randomize_transaction_parameters():
	accounts = get_accounts()
	chains = get_possible_chains()
	starting_chain = random.choice(chains)
	destination_chain = random.choice([chain for chain in chains if chain != starting_chain])
	
	# Randomly select an account
	account = random.choice(accounts)
	account_address = account['address']
	private_key = account['private_key']
	
	return starting_chain, destination_chain, account_address, private_key

def estimate_gas_limit(web3, from_address, to_address, data=None, value=0):
	# check if value is hex and convert to int
	if isinstance(value, str):
		if value.startswith('0x'):
			value = int(value, 16)
		else:
			value = int(value)

	transaction = {
		'from': from_address,
		'to': to_address,
		'value': value,
		'data': data
	}
	gas_limit = web3.eth.estimate_gas(transaction)
	return gas_limit

def estimate_gas_price(web3):
	gas_price = web3.eth.gas_price
	return gas_price

def get_token_info(chain, symbol):
	url = "https://li.quest/v1/token"
	headers = {"accept": "application/json"}
	response = requests.get(url, headers=headers, params={"chain": chain, "token": symbol})
	return response.json()

def get_token_balance(chain_name, account_address, token_symbol):
	_, _, _, alchemy_url_list, _, _, erc20_abi, _ = load_files()

	alchemy_url = alchemy_url_list.get(chain_name)
	if not alchemy_url:
		raise ValueError(f"Alchemy URL for chain {chain_name} not found.")
	
	token_info = get_token_info(get_chain_id(chain_name), token_symbol)
	token_address = token_info['address']

	web3 = init_web3(alchemy_url)
	token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=erc20_abi)
	balance = token_contract.functions.balanceOf(Web3.to_checksum_address(account_address)).call()
	return balance

