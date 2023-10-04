import streamlit as st
import requests
import random
from datetime import datetime, timedelta
from web3 import Web3
from .utils import date_to_timestamp, upload_to_ipfs, mint_nft
from .visuals import create_card, create_card_v1, create_card_v2

# w3 = Web3(Web3.HTTPProvider('https://rpc-mainnet.maticvigil.com/')) # Polygon mainnet RPC
w3 = Web3(Web3.HTTPProvider('https://polygon-mumbai.gateway.tenderly.co')) # Polygon Mumbai RPC

def run_app():
    st.title("NFT Resume")

    address = st.text_input("Enter your wallet address: ")
    user_name = st.text_input("Enter your name to show on card (optional)")
    user_image = st.file_uploader("Upload an image to show on your card (optional)", type=['jpg', 'jpeg', 'png'])

    if address:
        response = requests.get(
            f"https://deep-index.moralis.io/api/v2/{address}/nft/transfers?chain=eth&format=decimal&direction=both",
            headers={"accept": "application/json", "X-API-Key": "MORALIS_API_KEY"}
        )
        data = response.json()

        # ... [rest of the logic remains as in your code]
        wei = 1000000000000000000

        purchased_items = []
        sold_items = []

        for item in data["result"]:
            if item["to_address"].lower() == address.lower():
                purchased_items.append(item)
            else:
                sold_items.append(item)

        # Displaying purchased and sold items
        st.write(f"Purchased Items: {len(purchased_items)}")
        st.write(f"Sold Items: {len(sold_items)}")

        # Initial values for trait calculations
        total_hold_days = 0
        positive_profits = 0
        negative_profits = 0
        total_invested_eth = 0
        oldest_txn_date = datetime.now()
        recent_txn_date = datetime(1970, 1, 1)  # Very old date

        for p_item in purchased_items:
            for sold_item in sold_items:
                if p_item["token_address"] == sold_item["token_address"] and p_item["token_id"] == sold_item["token_id"]:
                    p_value = int(p_item["value"]) / wei
                    s_value = int(sold_item["value"]) / wei
                    profit = s_value - p_value
                    hold_time = date_to_timestamp(sold_item["block_timestamp"]) - date_to_timestamp(p_item["block_timestamp"])
                    total_hold_days += hold_time.days
                    
                    # Profit counting
                    if profit > 0:
                        positive_profits += 1
                    else:
                        negative_profits += 1
                        
                    # Total invested ETH counting
                    total_invested_eth += p_value
                    
                    # Oldest transaction date
                    current_txn_date = date_to_timestamp(p_item["block_timestamp"])
                    if current_txn_date < oldest_txn_date:
                        oldest_txn_date = current_txn_date
                        
                    # Recent transaction date
                    if current_txn_date > recent_txn_date:
                        recent_txn_date = current_txn_date

        # 1. Holder Trait
        if not total_hold_days == 0:
            avg_hold_time = timedelta(days=total_hold_days / len(sold_items))
        else:
            avg_hold_time = timedelta(days=1)
        print("Total Hold Days: " + str(total_hold_days))
        print("Avg Hold Time: " + str(avg_hold_time))
        if not len(sold_items) == 0:
            sold_percentage = len(sold_items) / (len(purchased_items) + len(sold_items)) * 100
        else:
            sold_percentage = 0
        print("Sold Percentage: " + str(sold_percentage))
        holder_score = ((100 - sold_percentage) * (avg_hold_time.days / 365))
        if holder_score > 100:
            holder_score = 100
        elif holder_score < 0:
            holder_score = 0
        print()

        # 2. Taker Trait
        if positive_profits == 0:
            positive_profits = 1
        taker_score = 100 * (positive_profits / (positive_profits + negative_profits))
        if taker_score > 100:
            taker_score = 100
        elif taker_score < 0:
            taker_score = 0
        print("Positive Profits: " + str(positive_profits))
        print("Negative Profits: " + str(negative_profits))
        print()

        # 3. OG Trait
        days_since_oldest_txn = (datetime.now() - oldest_txn_date).days
        print("Days Since Oldest Txn: " + str(days_since_oldest_txn))
        three_years = 1095
        og_score = (days_since_oldest_txn / three_years) * 100
        if og_score > 100:
            og_score = 100
        elif og_score < 0:
            og_score = 0
        print()

        # 4. Whale Trait
        whale_score = (total_invested_eth / 10) * 100
        if whale_score > 100:
            whale_score = 100
        elif whale_score < 0:
            whale_score = 0
        print("Total Invested ETH: " + str(total_invested_eth))
        print()

        # 5. Active Trait
        days_since_last_txn = (datetime.now() - recent_txn_date).days + 1
        print("Days Since Last Txn: " + str(days_since_last_txn))
        active_score = (7 / days_since_last_txn) * 100
        if active_score > 100:
            active_score = 100
        elif active_score < 0:
            active_score = 0

        traits = {
            'Holder': round(holder_score, 2),
            'Taker': round(taker_score, 2),
            'OG': round(og_score, 2),
            'Whale': round(whale_score, 2),
            'Active': round(active_score, 2)
        }

        # Validation
        wallet_address = f'{address[0:7]}...{address[-6:]}'
        if user_name == "":
            user_name = f"Anonymous_{random.randint(1000, 9999)}"
        if user_image == None:
            user_image = f"assets/images/ph{random.randint(1, 5)}.png"

        NFT = create_card_v2(user_name, wallet_address, user_image, traits)

        private_key = st.text_input("Your Private Key", "") # Change to Wallet Authentication in production
        receiver_address = w3.to_checksum_address(st.text_input("Receiver Address", address)) # Change to {address} in production
        # token_uri = st.text_input("Token URI", "https://ipfs.io/ipfs/QmQsDj1duabeEDq67PDb6hbGWrJcsM9kzcqUPbUR7rVfUc/73")  # Link to the metadata or image
        if 'token_uri' not in st.session_state:
            st.session_state.token_uri = None
        if st.button('Upload as NFT'):
            st.session_state.token_uri = upload_to_ipfs(NFT)  # Save token_uri in session state
            st.write("Your NFT is ready for Mint, Token URI: " + st.session_state.token_uri)

        if st.session_state.token_uri:
            if st.button('Mint NFT'):
                txn_hash = mint_nft(private_key, receiver_address, st.session_state.token_uri)
                st.write(f'Your NFT is minted successfully, Verify here: https://mumbai.polygonscan.com/tx/{txn_hash}')
