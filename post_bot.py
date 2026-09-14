import os
import datetime
from beem import Steem
from beem.comment import Comment

# 1. Configuration variables
MY_ACCOUNT = "bnwt"  
TARGET_COMMUNITY = "hive-129948"  
CUSTOM_TAGS = ["amarbanglablog", "art", "meme", "trc-20", "sunpump", "puss", "krsuccess"]

# The specific account receiving 100% of the rewards
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"  # Your worker endpoint

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

def get_ordinal_suffix(day):
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

def generate_custom_date():
    """Generates date format: 23rd Tuesday March 2026"""
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=3) # UTC to EAT
    day = now.day
    suffix = get_ordinal_suffix(day)
    weekday = now.strftime("%A")
    month = now.strftime("%B")
    year = now.strftime("%Y")
    return f"{day}{suffix} {weekday} {month} {year}"

# Build Date Formats
formatted_date = generate_custom_date()

# Content structure in Bangla
post_title = f"🐈‍⬛Puss গ্যাং🐾"
post_body = f"আরো Puss😼, আরো জুস🧃! {formatted_date}\n\nhttps://cdn.steemitimages.com/DQmVNXDdA1bCBGRZ2azkVdi7q19aupXoryQPnvzDXKWES3q/1000022551.jpg"
post_permlink = f"daily-blessing-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M')}"

# 3. Connect and broadcast using standard Beem structures
try:
    print(f"Connecting to node via Cloudflare proxy: {PROXY_URL}")
    
    # Initialize the robust Steem client
    stm = Steem(
        node=[PROXY_URL],
        keys=[MY_PRIVATE_POSTING_KEY]
    )
    
    print(f"Broadcasting to community {TARGET_COMMUNITY}...")
    
    # Post directly using the standard, tested blockchain structure wrapper
    stm.post(
        title=post_title,
        body=post_body,
        author=MY_ACCOUNT,
        permlink=post_permlink,
        tags=[TARGET_COMMUNITY] + CUSTOM_TAGS,
        parent_author="",
        parent_permlink=TARGET_COMMUNITY
    )
    
    print("Post has been published.")

except Exception as e:
    print(f"CRITICAL ERROR: Broadcast routing failed: {e}")
    exit(1)
