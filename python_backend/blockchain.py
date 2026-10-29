import os
from typing import Optional
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware




from python_backend.merkle import build_merkle_root_for_properties

POLYGON_AMOY_RPC = os.getenv("POLYGON_AMOY_RPC", "https://rpc-amoy.polygon.technology")
ANCHOR_CONTRACT_ADDRESS = os.getenv("ANCHOR_CONTRACT_ADDRESS", "0xYourAnchorContract")
ANCHOR_CONTRACT_ABI = []

PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS", "")


def get_web3() -> Web3:
    w3 = Web3(Web3.HTTPProvider(POLYGON_AMOY_RPC))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)



    return w3


def anchor_merkle_root_on_polygon(property_ids: list[int]) -> Optional[str]:
    try:
        w3 = get_web3()
        if not w3.is_connected():
            raise RuntimeError("Web3 connection failed")

        merkle_root = build_merkle_root_for_properties(property_ids)

        contract = w3.eth.contract(
            address=Web3.to_checksum_address(ANCHOR_CONTRACT_ADDRESS),
            abi=ANCHOR_CONTRACT_ABI,
        )

        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

        tx = contract.functions.anchorMerkleRoot(merkle_root).build_transaction(
            {
                "from": ACCOUNT_ADDRESS,
                "nonce": nonce,
                "gas": 300000,
                "gasPrice": w3.to_wei("1", "gwei"),
            }
        )

        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

        return tx_hash.hex()

    except Exception as e:
        print(f"Anchor failed: {e}")
        return None
