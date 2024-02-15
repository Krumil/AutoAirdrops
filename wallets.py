from web3 import Web3
import json

def generate_wallets(number_of_wallets):
    wallets = []
    for _ in range(number_of_wallets):
        acct = Web3().eth.account.create()
        wallet_info = {
            'private_key': acct._private_key.hex(),
            'address': acct.address
        }
        wallets.append(wallet_info)
    
    with open('wallets.json', 'w') as file:
        json.dump(wallets, file, indent=4)

generate_wallets(5)
