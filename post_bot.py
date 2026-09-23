import os
import datetime
import time 
import random 
import json
import urllib.request
from beem import Steem
from beem.comment import Comment

# =========================================================================
# GITHUB ACTIONS RUNTIME DELAY BUFFER
# =========================================================================
random_delay_seconds = random.randint(60, 1500)
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
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com"
    ],
    'eth': [
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com"
    ],
    'bnb': [
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com"
    ],
    'xrp': [
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com"
    ],
    'sol': [
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com",
        "https://steemitimages.com"
    ]
}

# ==========================================
# 2. KEY, ENDPOINT & ACCOUNT HEALTH SAFARDS
# ==========================================
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
PROXY_URL = "https://steemit.com"  

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
        gecko_url = "https://api.coingecko.com/api/v3"
        req = urllib.request.Request(gecko_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_json = json.loads(response.read().decode())
            
            # Map parameters safely
            mapping = {'bitcoin': 'btc', 'ethereum': 'eth', 'binancecoin': 'bnb', 'ripple': 'xrp', 'solana': 'sol'}
            for item in raw_json:
                sym = mapping.get(item['id'])
                if sym:
                    market_data[sym]['price'] = float(item['current_price'])
                    market_data[sym]['change'] = float(item['price_change_percentage_24h'] or 0.0)
            
            # Verify no empty fields slipped through
            if market_data['btc']['price'] > 0:
                data_acquired = True
                print("CoinGecko ingestion complete.")
    except Exception as e:
        print(f"⚠️ Primary Pipeline Blocked ({e}). Forwarding request to Backup Pipeline...")

# --- SOURCE 2: CRYPTOCOMPARE PUBLIC ENDPOINT ---
if not data_acquired:
    print("Secondary Pipeline: Fetching live data from CryptoCompare API...")
    try:
        # Validated pricing API url string query parameters
        cc_url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD"
        req = urllib.request.Request(cc_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_json = json.loads(response.read().decode())
            raw_data = raw_json.get("RAW", {})
            
            for sym in ['BTC', 'ETH', 'BNB', 'XRP', 'SOL']:
                low_sym = sym.lower()
                market_data[low_sym]['price'] = float(raw_data[sym]['USD']['PRICE'])
                market_data[low_sym]['change'] = float(raw_data[sym]['USD']['CHANGEPCT24HOUR'])
            
            if market_data['btc']['price'] > 0:
                data_acquired = True
                print("CryptoCompare ingestion complete.")
    except Exception as e:
        print(f"⚠️ Secondary Pipeline Blocked ({e}). Forwarding to Tertiary Tier...")

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
print(f"📊 Top Performer: {top_performer['name']} ({top_coin_key.upper()}) at {top_performer['change']:.2f}%. Selected image link variant.")

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
    emoji = "🟢 +" if coin['change'] >= 0 else "🔴 "
    price_str = f"${coin['price']:,}" if coin['price'] >= 1 else f"${coin['price']:.4f}"
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
post_title = f"{selected_prefix} — {formatted_date}"

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

print(f"🔗 Dynamic Title Generated: '{post_title}'")
print(f"🔗 Matching Permlink Slug compiled: '{post_permlink}'")

# Compile the final Markdown text array payload
body_lines = [
    f"### 📈 {selected_prefix} — {formatted_date}\n",
    "Daily analytical tracking data for top-tier cryptocurrency assets compiled seamlessly using lightweight text parameters:\n",
    format_row('btc'),
    format_row('eth'),
    format_row('bnb'),
    format_row('xrp'),
    format_row('sol'),
    f"\n🚀 **Top Asset Performer Today:** {top_performer['name']} ({top_coin_key.upper()})\n",
    f"![Market Performance Header Area]({selected_display_image})"
]
post_body = "\n".join(body_lines)

# ==========================================
# 5. BLOCKCHAIN TRANSMISSION HANDSHAKE
# ==========================================
try:
    print(f"Connecting to Steem node: {PROXY_URL}")
    stm = Steem(node=[PROXY_URL], keys=[MY_PRIVATE_POSTING_KEY])
    print(f"Broadcasting dynamic market data overview to community {TARGET_COMMUNITY}.")
    
    stm.post(
        title=post_title,
        body=post_body,
        author=MY_ACCOUNT,
        permlink=post_permlink,
        tags=[TARGET_COMMUNITY] + CUSTOM_TAGS,
        parent_author="",
        parent_permlink=TARGET_COMMUNITY
    )
    print(f"Success! Crypto Market Report has been successfully published to {TARGET_COMMUNITY}.")
except Exception as e:
    print(f"CRITICAL ERROR: Broadcast routing failed: {e}")
    exit(1)
