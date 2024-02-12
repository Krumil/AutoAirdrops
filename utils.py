import json
import os 
import dotenv

dotenv.load_dotenv()

def get_possible_chains():
	return ['arbitrum','base', 'optimism', 'polygon_zk']  
	# return ['arbitrum','base', 'optimism', 'polygon_zk', 'scroll']  

# Function to count the number of account entries in the .env
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
    
    networks = get_possible_chains()
    alchemy_url_list = {chain: os.getenv(f'{chain.upper()}_ALCHEMY_URL') for chain in networks}
    
    return hNFT_addresses, hFT_addresses, domains, alchemy_url_list, hNFT_abi, hFT_abi



# Function to read ABI from a local file
def load_abi(file_path):
	with open(file_path, 'r') as file:
		return json.load(file)
