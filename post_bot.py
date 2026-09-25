import os
import datetime
import time 
import random 
import json
import urllib.request
from beem import Steem
from beem.comment import Comment
import websocket

# =========================================================================
# GITHUB ACTIONS RUNTIME DELAY BUFFER
# =========================================================================
random_delay_seconds = random.randint(60, 900)
print(f"Cloudflare handshake cleared. Shifting execution delay to GitHub Actions context...")
print(f"Jitter activated: Sleeping for {random_delay_seconds / 60:.1f} minutes before posting...")
time.sleep(random_delay_seconds)
# =========================================================================

# ==========================================
# 1. CONFIGURATION VARIABLES
# ==========================================
MY_ACCOUNT = "blog.god"  
TARGET_COMMUNITY = "hive-129948"  
CUSTOM_TAGS = ["crypto", "xrp", "eth", "bnb", "sol", "btc", "krsuccess"]

# 20 Hardcoded ultra-low RC asset images mapped explicitly (4 per coin asset category)
IMAGE_MATRIX = {
    'btc': [
        "https://cdn.steemitimages.com/DQmc1LphNvohBCUsroZ9zjRuL3VzaVJfMVN9oN8hDmX5M9A/1000024867.jpg",
        "https://cdn.steemitimages.com/DQmQjKH5D34ym38roHSoCKh7W79GaV3f6Hh3FNAf7zH6x4K/1000024869.jpg",
        "https://cdn.steemitimages.com/DQmPNweKd69d1esmMV7DDFFkqs1oPYjEP4TMRqx7TKySk4F/1000024870.jpg",
        "https://cdn.steemitimages.com/DQmVphp18Aq5jdTu2VsvaQ8SK22FQrsoHHMvCnivwFn2ECz/1000024872.jpg"

    ],
    'eth': [
        "https://cdn.steemitimages.com/DQmNbTtqvFoiDwHvxVsSo3AfDgK6YnAnvnndpB52ei5o4cg/1000024873.jpg", 
        "https://cdn.steemitimages.com/DQmXZayvTu9PqYiWRX9s6ok2GYHj4ZVJ2ZzaJbeSQG1UZtd/1000024874.jpg", 
        "https://cdn.steemitimages.com/DQmeBPMY49p98JYbZqrUHahqyvWiZwTmzKLDH3DqRjK2mej/1000024876.jpg", 
        "https://cdn.steemitimages.com/DQmRagxTVdy3HweodDjUN1Q3qgXUZgvTpdLBpJR7tJ3VfJS/1000024875.jpg" 
    ],
    'bnb': [
        "https://cdn.steemitimages.com/DQmSVx5EisX8kQfv516tTnsuw8da9PWLYSgvMQxpNLZkCFc/1000024880.jpg", 
        "https://cdn.steemitimages.com/DQmRrPFPJ1gP3SLEv5deYRVtJzHr31iBVXiCFvsBPVnqtHZ/1000024879.jpg", 
        "https://cdn.steemitimages.com/DQmPSX1xN4vEQerdyD147mmhCvxX4KpcU4brJXeuhN978qa/1000024878.jpg", 
        "https://cdn.steemitimages.com/DQmX4F4oZtAYv8TXvoripjNxzw1YWn5BnGwb3DJCJHpFmRC/1000024877.jpg" 
    ],
    'xrp': [
        "https://cdn.steemitimages.com/DQmeLCBSXQtxgudkdAarnH9u2U9qAQsJYsVZ3RaeLuyyTZ1/1000024886.jpg", 
        "https://cdn.steemitimages.com/DQmdc4oUuB4gHpeL2DoD5xZZc7EiEFeGtsUYhRH4EoSiQEh/1000024885.jpg", 
        "https://cdn.steemitimages.com/DQmXpKpPXpHWWM5UyVo4adFboRwFLXCNGQhSKyLciUxzTny/1000024884.jpg", 
        "https://cdn.steemitimages.com/DQmTxJR9qrXqhGWVQZz8XHab5gn6RaTHm7VFkHvkDmtpM8H/1000024883.jpg"
    ],
    'sol': [
        "https://cdn.steemitimages.com/DQmXE8Ke5EsaayVFJwHTrqYYTGbHNe9gkJMPDWn4qxBJQyD/1000024887.jpg",
        "https://cdn.steemitimages.com/DQmZHGWT8Y3u4GsKtvQtN65cSNGTXtVxJiJGNXLduaokxkn/1000024888.jpg",
        "https://cdn.steemitimages.com/DQmWGdsU9wF3arTmn4Fz9A4pkU3xSDsGFoVpHgjDURW8xuf/1000024889.jpg",
        "https://cdn.steemitimages.com/DQmbsLSbAETZcwdoKG2t6hNPK9fZShorsMkfcGe5xrhtpfC/1000024890.jpg"
    ]
}

# ==========================================
# 2. KEY, ENDPOINT & ACCOUNT HEALTH SAFARDS
# ==========================================
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"  

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

# Initialize standard client connection node early for verification
stm_check = Steem(node=[PROXY_URL], keys=[MY_PRIVATE_POSTING_KEY])
from beem.account import Account
account_info = Account(MY_ACCOUNT, blockchain_instance=stm_check)

# Live Resource Credits Bandwidth Guard
rc_manabar = account_info.get_rc_manabar()
current_rc = (rc_manabar['current_mana'] / rc_manabar['max_mana']) * 100
print(f"Account @{MY_ACCOUNT} Live Resource Credits check: {current_rc:.2f}%")

if current_rc < 75.0:
    print(f"⚠️ Safety Halt: Resource Credits dropped below threshold ({current_rc:.2f}%). Execution skipped.")
    exit(0)

# Unified standard structured ledger map dictionary
market_data = {
    'btc': {'name': 'Bitcoin', 'price': 0.0, 'change': 0.0},
    'eth': {'name': 'Ethereum', 'price': 0.0, 'change': 0.0},
    'bnb': {'name': 'BNB', 'price': 0.0, 'change': 0.0},
    'xrp': {'name': 'XRP', 'price': 0.0, 'change': 0.0},
    'sol': {'name': 'Solana', 'price': 0.0, 'change': 0.0}
}


# ==========================================
# 3. CASCADING API DATA EXTRACTION LAYER
# ==========================================
data_acquired = False

# --- SOURCE 1: COINGECKO PUBLIC KEYLESS ENDPOINT ---
if not data_acquired:
    print("Primary Pipeline: Fetching live data from CoinGecko Public API...")
    try:
        # Fully qualified API endpoint mapping your target 5 assets
        gecko_url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum,binancecoin,ripple,solana"
            "&vs_currencies=usd"
            "&include_24hr_change=true"
        )

        req = urllib.request.Request(
            gecko_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            raw_json = json.loads(response.read().decode())

        mapping = {
            "bitcoin": "btc",
            "ethereum": "eth",
            "binancecoin": "bnb",
            "ripple": "xrp",
            "solana": "sol",
        }

        for coin_id, sym in mapping.items():
            coin = raw_json.get(coin_id, {})
            market_data[sym]["price"] = float(coin.get("usd", 0))
            market_data[sym]["change"] = float(
                coin.get("usd_24h_change") or 0
            )

        if market_data["btc"]["price"] > 0:
            data_acquired = True
            print("CoinGecko ingestion complete.")

    except Exception as e:
        print(
            f"⚠️ Primary Pipeline Blocked ({e}). "
            "Forwarding request to Backup Pipeline..."
        )

# --- SOURCE 2: BINANCE PUBLIC WEBSOCKET ---
if not data_acquired:
    print("Secondary Pipeline: Fetching live data from Binance WebSocket...")

    try:
        binance_symbols = {
            "BTCUSDT": "btc",
            "ETHUSDT": "eth",
            "BNBUSDT": "bnb",
            "XRPUSDT": "xrp",
            "SOLUSDT": "sol",
        }

        streams = "/".join(
            f"{symbol.lower()}@ticker"
            for symbol in binance_symbols
        )

        binance_url = (
            "wss://stream.binance.com:9443/stream"
            f"?streams={streams}"
        )

        prices_received = set()
        ws = websocket.create_connection(binance_url, timeout=10)

        try:
            while prices_received != set(binance_symbols):
                message = json.loads(ws.recv())
                ticker = message.get("data", {})

                symbol = ticker.get("s")
                if symbol not in binance_symbols:
                    continue

                market_key = binance_symbols[symbol]
                market_data[market_key]["price"] = float(ticker["c"])
                market_data[market_key]["change"] = float(ticker["P"])
                prices_received.add(symbol)

        finally:
            ws.close()

        if len(prices_received) == len(binance_symbols):
            data_acquired = True
            print("Binance WebSocket ingestion complete.")

    except Exception as e:
        print(
            f"⚠️ Secondary Pipeline Blocked ({e}). "
            "Forwarding to Tertiary Tier..."
        )

# --- SOURCE 3: COINPAPRIKA PUBLIC KEYLESS ENDPOINT ---
if not data_acquired:
    print("Tertiary Pipeline: Fetching live data from CoinPaprika API...")
    try:
        paprika_url = "https://api.coinpaprika.com/v1/tickers"
        req = urllib.request.Request(paprika_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as response:
            raw_json = json.loads(response.read().decode())
            
            mapping = {
                'btc-bitcoin': 'btc', 'eth-ethereum': 'eth', 
                'bnb-binance-coin': 'bnb', 'xrp-xrp': 'xrp', 'sol-solana': 'sol'
            }
            for item in raw_json:
                sym = mapping.get(item['id'])
                if sym:
                    market_data[sym]['price'] = float(item['quotes']['USD']['price'])
                    market_data[sym]['change'] = float(item['quotes']['USD']['percent_change_24h'])
            
            if market_data['btc']['price'] > 0:
                data_acquired = True
                print("CoinPaprika ingestion complete.")
    except Exception as e:
        print(f"🚨 Tertiary Failure: All public data networks unresponsive ({e}).")

# --- ABSOLUTE SAFETY BREAK ---
if not data_acquired:
    print("Safeguard Halt: Live market data unreachable. Terminating deployment loop to prevent posting old data.")
    exit(0) # Halts context cleanly without displaying system error codes on GitHub

# Find the highest performer out of your active database loop
top_performer = max(market_data.values(), key=lambda x: x['change'])

# ==========================================
# 4. STRUCTURE, SELECTION & LOW-RC TEXT COMPILATION
# ==========================================
# Find the highest performer out of your active database loop dictionary keys
top_coin_key = max(market_data.keys(), key=lambda k: market_data[k]['change'])
top_performer = market_data[top_coin_key]

# Pick a completely random target image out of the top performer's 4 dedicated URLs
selected_display_image = random.choice(IMAGE_MATRIX[top_coin_key])
print(f"🥇 Top Performer: {top_performer['name']} ({top_coin_key.upper()}) at {top_performer['change']:.2f}%. Selected image link variant.")

now_eat = datetime.datetime.utcnow() + datetime.timedelta(hours=3) # UTC to EAT

def get_ordinal_suffix(day):
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

day = now_eat.day
suffix = get_ordinal_suffix(day)
formatted_date = f"{day}{suffix} {now_eat.strftime('%A %B %Y')}"

def format_row(key):
    coin = market_data[key]
    emoji = "🔺 +" if coin['change'] >= 0 else "🔻"
    # Added :.2f to format numbers >= 1 with exactly 2 decimal places
    price_str = f"${coin['price']:,.2f}" if coin['price'] >= 1 else f"${coin['price']:.4f}"
    return f"* 🪙 **{coin['name']} ({key.upper()}):** {price_str} | {emoji}{coin['change']:.2f}%"

# A pool of unique human-written title prefixes to break structural repetitions
title_variations = [
    "The Crypto Market is Crazy Today!",
    "What's Happening On The Crypto World?",
    "BTC, XRP, ETH, BNB And SOLANA Are Moving!",
    "Crypto Market Prices Update",
    "Is a Crypto Breakout Happening Right Now?",
    "The Complete Daily Crypto Asset Report",
    "Where is the Crypto Market Heading Today?",
    "A Quick Look at Today's Crypto Movements",
    "Crypto Prices Are Shifting Fast Today!",
    "Your Essential Daily Crypto Market Ingest",
    "Major Volatility Hitting Top Crypto Coins!",
    "Checking In On The Crypto World Today",
    "Are the Top Cryptos Gaining Momentum?",
    "Unpacking Today's Crypto Market Action",
    "The Big 5 Cryptos Are Shaking Up the Market!",
    "A Quick Breakdown of Today's Crypto Prices",
    "An Interesting Day in the Crypto Space!",
    "Tracking Today's Top Cryptocurrencies",
    "The Latest Shifts in the Crypto Market",
    "Where the Top 5 Crypto Coins Stand Today"
]
selected_prefix = random.choice(title_variations)
post_title = f"{selected_prefix}"

# ==========================================
# 5. DYNAMIC TITLE-BASED PERMLINK SLUG LOGIC
# ==========================================
# 1. Transform the randomly chosen prefix to lowercase
raw_slug = selected_prefix.lower()
# 2. Safely strip special characters using basic loop text filtering
clean_chars = [char if char.isalnum() or char.isspace() else "" for char in raw_slug]
# 3. Clean up spaces and join strings using standard hyphens
slug_str = "-".join("".join(clean_chars).split())
# 4. Combine the dynamic prefix slug with the current date to guarantee uniqueness
post_permlink = f"{slug_str}-{now_eat.strftime('%Y%m%d')}"

print(f"✅ Dynamic Title Generated: '{post_title}'")
print(f"✅ Matching Permlink Slug compiled: '{post_permlink}'")

# Compile the final Markdown text array payload
body_lines = [
    f"### {formatted_date}\n",
    "Latest Prices:\n",
    format_row('btc'),
    format_row('eth'),
    format_row('bnb'),
    format_row('xrp'),
    format_row('sol'),
    f"\n🔺**Top Coin Today:** {top_coin_key.upper()}\n",
    f"![{selected_prefix}]({selected_display_image})"
]
post_body = "\n".join(body_lines)

# ==========================================
# 5. BLOCKCHAIN TRANSMISSION HANDSHAKE
# ==========================================
try:
    print(f"Connecting to Steem node: {PROXY_URL}")
    stm = Steem(node=[PROXY_URL], keys=[MY_PRIVATE_POSTING_KEY])
    print(f"Posting on {TARGET_COMMUNITY}.")
    
    stm.post(
        title=post_title,
        body=post_body,
        author=MY_ACCOUNT,
        permlink=post_permlink,
        tags=[TARGET_COMMUNITY] + CUSTOM_TAGS,
        parent_author="",
        parent_permlink=TARGET_COMMUNITY
    )
    print(f"✅ The Report has been Published on {TARGET_COMMUNITY} posts feed.")
except Exception as e:
    print(f"CRITICAL ERROR: Broadcast routing failed: {e}")
    exit(1)
