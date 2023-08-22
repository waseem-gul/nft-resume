import requests
import json
import streamlit as st
from io import BytesIO
from datetime import datetime
from web3 import Web3

# w3 = Web3(Web3.HTTPProvider('https://rpc-mainnet.maticvigil.com/')) # Polygon mainnet RPC
w3 = Web3(Web3.HTTPProvider('https://polygon-mumbai.gateway.tenderly.co')) # Polygon Mumbai RPC
ABI = [...]  # Your contract ABI
# Load ABI
with open('contract_abi.json', 'r') as file:
    contract_data = json.load(file)
    ABI = contract_data['abi']
CONTRACT_ADDRESS = '0xd9145CCE52D386f254917e481eB44e9943F39138'

contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)


def date_to_timestamp(str_time):
    date_and_time = str_time.split("T")
    r_list = []
    r_list.extend(date_and_time[0].split("-"))
    r_list.extend(date_and_time[1].split(":"))
    result = datetime(int(r_list[0]), int(r_list[1]), int(r_list[2]), int(r_list[3]), int(r_list[4]))
    return result


def upload_to_ipfs(file_path):
    project_id = "2UB2n2k28dL6BIz1FIftDinhgRW"
    project_secret = "7bfa22cee98b5b5938c9765259eb8a57"
    endpoint = "https://ipfs.infura.io:5001"
    buffer = BytesIO()
    file_path.save(buffer, format="PNG")  # You can change PNG to another format if needed
    image_bytes = buffer.getvalue()

    files = {'file': ('image.png', image_bytes, 'image/png')}
    response1 = requests.post(endpoint + '/api/v0/add', files=files, auth=(project_id, project_secret))
    print(response1)
    hash = response1.text.split(",")[1].split(":")[1].replace('"','')
    print(hash)
    return f"ipfs://{hash}"


def mint_nft(private_key, to_address, token_uri):
    current_gas_price = w3.eth.gas_price
    st.write("Gas Price: " + str(current_gas_price))
    adjusted_gas_price = int(current_gas_price * 20)
    nonce = w3.eth.get_transaction_count(w3.eth.account.from_key(private_key).address)
    txn_dict = contract.functions.mint(to_address).build_transaction({
        'chainId': 80001,  # Polygon Mumbainet Chain ID
        'gas': 2000000,
        'gasPrice': adjusted_gas_price,
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key)
    result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return result.hex()
