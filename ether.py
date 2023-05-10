#!/usr/bin/env python3

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
# from hdwallet.utils import generate_mnemonic
import requests
import time
# from typing import Optional


# api keys
etherscan_apikey = "ZVJRWF74YSUTFHFC5JPGJPNREZ3I77IXJY"     # etherscan.io
covalent_apikey = "cqt_rQXqtYkJgWpj8qtqK4bYkHtqKQhx"        # covalenthq.com



# Check Coin Balances
def eth_balance(address):
    response = requests.get("https://api.etherscan.io/api?module=account&action=balance&address=" + address + "&tag=latest&apikey=" + etherscan_apikey)
    # response = requests.get("https://api.covalenthq.com/v1/eth-mainnet/address/" + address + "/balances_v2/" + covalent_apikey + ":")
    #     headers = {
    #     'Content-Type': 'application/json',
    # }

    # response = requests.get(
    #     'https://api.covalenthq.com/v1/1/block_v2/5000000/',
    #     headers=headers,
    #     auth=('cqt_rQXqtYkJgWpj8qtqK4bYkHtqKQhx', ''),
    # )
    return response.json()["result"]
    # print(response.json())
    # return response.json()


def eth_table(mnemonic):
    # English mnemonic words
    MNEMONIC: str = mnemonic	# generate_mnemonic(language="english", strength=128)

    # Initialize Ethereum mainnet BIP44HDWallet
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    # Get Ethereum BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(mnemonic=MNEMONIC, language="english")
    # Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    print("Mnemonic:", bip44_hdwallet.mnemonic())
    print("Base HD Path:  m/44'/60'/0'/0/{address_index}", "\n")


    print("index\tpath \t\taddress \t\t\t\tprivate_key \t\t\t\t\tBalance")

    # Get Ethereum BIP44HDWallet information's from address index
    for address_index in range(10):
        # Derivation from Ethereum BIP44 derivation path
        bip44_derivation: BIP44Derivation = BIP44Derivation(cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index)
        # Derive Ethereum BIP44HDWallet
        bip44_hdwallet.from_path(path=bip44_derivation)
        # Print address_index, path, address and private_key
        address = f"{bip44_hdwallet.address()}"
        print(f"({address_index}) {bip44_hdwallet.path()} {bip44_hdwallet.address()} 0x{bip44_hdwallet.private_key()} ", eth_balance(address))
        # Clean derivation indexes/paths
        bip44_hdwallet.clean_derivation()
        
        # avoid rate limit of 5 req/sec
        if (address_index + 1) % 5 == 0:
            time.sleep(0.2)
        else:
            continue



#   Use the command via the following:
eth_table("audit sustain suggest monster device lizard offer must voyage aim sail game")

