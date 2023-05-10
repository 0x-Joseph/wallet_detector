#!/usr/bin/env python3

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import BitcoinMainnet
from hdwallet.derivations import BIP44Derivation
# from hdwallet.utils import generate_mnemonic
import requests
import time
# from typing import Optional


# api keys
etherscan_apikey = "ZVJRWF74YSUTFHFC5JPGJPNREZ3I77IXJY"



# Check Coin Balances
def eth_balance(address):
    response=requests.get("https://api.etherscan.io/api?module=account&action=balance&address=" + address + "&tag=latest&apikey=" + etherscan_apikey)
    return response.json()["result"]


def eth_table(mnemonic):
    # English mnemonic words
    MNEMONIC: str = mnemonic	# generate_mnemonic(language="english", strength=128)

    # Initialize Bitcoin mainnet BIP44HDWallet
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=BitcoinMainnet)
    # Get Bitcoin BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(mnemonic=MNEMONIC, language="english")
    # Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    print("Mnemonic:", bip44_hdwallet.mnemonic())
    print("Base HD Path:  m/44'/0'/0'/0/{address_index}", "\n")


    print("index\tpath \t\taddress \t\t\t\tprivate_key \t\t\t\t\tBalance")

    # Get Bitcoin BIP44HDWallet information's from address index
    for address_index in range(10):
        # Derivation from Bitcoin BIP44 derivation path
        bip44_derivation: BIP44Derivation = BIP44Derivation(cryptocurrency=BitcoinMainnet, account=0, change=False, address=address_index)
        # Derive Bitcoin BIP44HDWallet
        bip44_hdwallet.from_path(path=bip44_derivation)
        # Print address_index, path, address and private_key
        address = f"{bip44_hdwallet.address()}"
        print(f"({address_index}) {bip44_hdwallet.path()} {bip44_hdwallet.address()} 0x{bip44_hdwallet.private_key()} ", eth_balance(address))
        # Clean derivation indexes/paths
        bip44_hdwallet.clean_derivation()
        
        # avoid rate limit of 5 req/sec
        if (address_index + 1) % 5 == 0:
            time.sleep(1)
        else:
            continue
    print("\n\n")

eth_table("audit sustain suggest monster device lizard offer must voyage aim sail game")
eth_table("copper item observe chimney find recall penalty leisure panic school exclude vapor fringe avocado visit")