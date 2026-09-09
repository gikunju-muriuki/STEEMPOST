import os
import datetime
from lightsteem.client import Client
# FIX 1: Import the Operation data structure needed for broadcasting
from lightsteem.datastructures import Operation

# 1. Configuration variables
MY_ACCOUNT = "bnwt"  
TARGET_COMMUNITY = "hive-129948"  
CUSTOM_TAGS = ["steemexclusive", "amarbanglablog", "general-writing", "krsuccess"]

# 2. Extract configuration from GitHub Secrets
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
post_title = f"আজকের দিন, আজকের আশীর্বাদ! - {formatted_date}"
post_body = f"নতুন দিন, নতুন আশীর্বাদ! {formatted_date}\n\nGitHub এবং Cloudflare Workers দ্বারা চালিত।"
post_permlink = f"daily-blessing-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M')}"

# 3. Connect using direct structural processing entries
try:
    client = Client(
        nodes=[PROXY_URL],
        keys=[MY_PRIVATE_POSTING_KEY]
    )
    
    print(f"Broadcasting to community {TARGET_COMMUNITY} via Cloudflare proxy...")
    
    post_data = {
        "author": MY_ACCOUNT,
        "permlink": post_permlink,
        "title": post_title,
        "body": post_body,
        "parent_author": "",                  
        "parent_permlink": TARGET_COMMUNITY,  
        "json_metadata": {"tags": CUSTOM_TAGS}
    }
    
    # FIX 2: Package the comment dictionary inside an Operation object before passing to client.broadcast
    op = Operation("comment", post_data)
    client.broadcast(op)
    
    print("SUCCESS: Post has bypassed the firewall and published to Steem!")

except Exception as e:
    print(f"CRITICAL ERROR: Broadcast routing failed: {e}")
    exit(1)
