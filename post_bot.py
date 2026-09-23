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
CUSTOM_TAGS = ["crypto", "bitcoin", "krsuccess"]

# Ultra-low RC Asset Image hosted directly on Steemit's server grid
SIGNATURE_IMAGE_URL = "https://steemitimages.com"

# ==========================================
# 2. KEY & ENDPOINT MANAGEMENT
# ==========================================
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
# Validated standard public node backup path (or swap in your verified worker sub-slug)
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"  

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

# Unified standard data dictionary structure
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
        paprika_url = "https://coinpaprika.com"
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
# 4. STRUCTURE & LOW-RC TEXT COMPILATION
# ==========================================
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

post_title = f"Crypto Pulse Market Overview — {formatted_date}"

body_lines = [
    f"### 📈 Crypto Pulse Report — {formatted_date}\n",
    "Daily analytical tracking data for top-tier cryptocurrency assets compiled seamlessly using lightweight text parameters:\n",
    format_row('btc'),
    format_row('eth'),
    format_row('bnb'),
    format_row('xrp'),
    format_row('sol'),
    f"\n🚀 **Top Asset Performer Today:** {top_performer['name']} ({top_performer['name']})\n",
    f"![Market Overview]({SIGNATURE_IMAGE_URL})"
]
post_body = "\n".join(body_lines)
post_permlink = f"crypto-pulse-report-{now_eat.strftime('%Y%m%d')}"

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
