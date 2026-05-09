import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import json
import random
from http.server import BaseHTTPRequestHandler

# --- 2026 PROFESSIONAL CONFIGURATION ---
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

# --- THE HARD FILTERS (The "Airen Scott" Protection) ---
# If these words appear, the lead is immediately discarded.
BLOCK_LIST = ["texas", "houston", "dallas", "nepa", "phcn", "light bill", "solar", "freezer", "rent"]
TARGET_CITIES = ["lagos", "accra", "nairobi", "lekki", "epe", "abuja"]

# --- THE SEARCH ENGINE QUERIES ---
# Focused 100% on X.com with Pan-African intent.
QUERIES = [
    'site:x.com "wanna buy" (Lagos OR Accra OR Nairobi) -Texas -Houston',
    'site:x.com "invest in property" (Nigeria OR Ghana OR Kenya) -rent',
    'site:x.com "verified title" (Lagos OR Accra OR Nairobi) "diaspora"',
    'site:x.com "is it safe to buy" (Lekki OR Epe OR "East Legon" OR "Kilimani")',
    'site:x.com "recommend" "realtor" (Lagos OR Accra OR Nairobi) -USA'
]

def get_intent_tag(text):
    """Categorizes the lead based on their message."""
    text = text.lower()
    if "buy" in text or "buying" in text: return "🏠 BUYER"
    if "invest" in text or "yield" in text: return "📈 INVESTOR"
    if "title" in text or "verify" in text: return "🛡️ VERIFICATION"
    return "💡 OPPORTUNITY"

def is_clean_lead(title, snippet):
    """The 'No-Noise' Filter. Checks if the lead is actually about your target market."""
    combined = (title + " " + snippet).lower()
    
    # Rule 1: Check for Blocked terms
    for word in BLOCK_LIST:
        if word in combined:
            return False
            
    # Rule 2: Must mention at least one target African location or "Nigeria/Ghana/Kenya"
    continents = ["nigeria", "ghana", "kenya", "africa"]
    if any(loc in combined for loc in TARGET_CITIES + continents):
        return True
        
    return False

def send_telegram_card(name, location, text, link):
    """Sends a high-end, clean lead card to your Telegram Bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    intent = get_intent_tag(text)
    
    # Modern, agency-style layout
    message = (
        f"💎 **{intent} FOUND**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **User:** {name}\n"
        f"📍 **Focus:** {location.upper()}\n"
        f"🌐 **Source:** 🐦 X (Twitter)\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Signal:** \"{text[:160]}...\"\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [OPEN X PROFILE]({link})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🛡️ *Verified by Superite Partner Engine*"
    )
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

class handler(BaseHTTPRequestHandler):
    """Vercel Entry Point"""
    def do_GET(self):
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        ]
        
        headers = {'User-Agent': random.choice(agents)}
        total_leads = 0

        for query in QUERIES:
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            try:
                response = requests.get(search_url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.select('.tF2Cxc'):
                    title_elem = result.select_one('.DKV0Md')
                    link_elem = result.select_one('.yuRUbf a')
                    snippet_elem = result.select_one('.VwiC3b')

                    if title_elem and link_elem:
                        title = title_elem.text
                        snippet = snippet_elem.text if snippet_elem else ""
                        link = link_elem['href']

                        # APPLY THE PREMIUM FILTERS
                        if is_clean_lead(title, snippet):
                            name = title.split('(@')[0].split('|')[0].strip()
                            
                            # Identify Location
                            found_loc = "Pan-Africa"
                            for city in TARGET_CITIES:
                                if city in (title + snippet).lower():
                                    found_loc = city
                                    break
                            
                            send_telegram_card(name, found_loc, snippet, link)
                            total_leads += 1
                            time.sleep(1.5) 

            except Exception as e:
                print(f"Skipping query due to error: {e}")

        # Vercel Success Response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "active",
            "leads_pushed": total_leads,
            "targeting": "X_ONLY_PAN_AFRICA"
        }).encode())
    
