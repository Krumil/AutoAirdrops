# # Example usage
# account_address = "0xYourAccountAddress"
# private_key = "0xYourPrivateKey"
# chain = "ethereum"


# def swap_low_value_tokens_to_eth(chain, account_address, private_key):
#     # Get list of tokens and their balances
#     tokens = get_all_tokens(chain, account_address)
#     for token in tokens:
#         # Get token balance in terms of USDC
#         token_balance = get_token_balance(chain, account_address, token["address"])
#         token_usdc_value = get_usdc_value(chain, token["address"], token_balance)

#         # Check if the token value is less than 50 USDC
#         if token_usdc_value < 50:
#             # Swap token to ETH
#             receipt = execute_swap(
#                 chain,
#                 chain,
#                 token["symbol"],
#                 "ETH",
#                 token_balance,
#                 account_address,
#                 private_key,
#             )
#             print(f"Swapped {token['symbol']} to ETH: {receipt}")


# swap_low_value_tokens_to_eth(chain, account_address, private_key)


from utils import get_all_tokens, get_token_balance, load_uniswap_token_list
from actions.lifi import get_token_usdc_value

token_list = load_uniswap_token_list("uniswap-token-list.json")
chain = "base"
account_address = "0x8e5e01DCa1706F9Df683c53a6Fc9D4bb8D237153"

tokens = get_all_tokens(chain, account_address, token_list)
for token in tokens:
    token_balance = token["amount"]
    token_usdc_value = get_token_usdc_value(
        chain, token["address"], token_balance, account_address
    )

    print(
        f"Token Symbol: {token['symbol']} Balance: {token_balance}, USDC Value: {token_usdc_value}"
    )
