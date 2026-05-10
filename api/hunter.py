import requests
import json
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler

# --- 2026 PROFESSIONAL CONFIGURATION ---
# Your Verified Credentials
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"
SERPER_API_KEY = "6c182913e988a6f03588ca60e4cd657a5fb66300"

# --- THE HARD FILTERS (Keeping the junk out) ---
BLOCK_LIST = ["texas", "houston", "dallas", "nepa", "phcn", "light bill", "solar", "freezer", "rent", "apartment for rent"]
TARGET_CITIES = ["lagos", "accra", "nairobi", "lekki", "epe", "abuja", "ibadan"]

# --- THE PREMIUM SEARCH QUERIES ---
# Optimized for high-ticket diaspora investors and competitors.
QUERIES = [
    'site:x.com "is it safe to buy land" (Lagos OR Epe OR Lekki) "verification"',
    'site:x.com "landwey" OR "veritasi" OR "alaro city" "review" OR "legit" OR "scam"',
    'site:x.com "Governor\'s Consent" OR "C of O" OR "Excision" (Lagos OR Abuja) "price"',
    'site:x.com "recommend a realtor" (Lagos OR Accra) "diaspora" -USA',
    'site:x.com "thinking of investing" (Nigeria OR Ghana) "real estate" -rent'
]

def get_intent_tag(text):
    """Categorizes the lead based on their message."""
    text = text.lower()
    if "buy" in text or "buying" in text: return "🏠 BUYER"
    if "invest" in text or "yield" in text: return "📈 INVESTOR"
    if "title" in text or "verify" in text or "consent" in text: return "🛡️ VERIFICATION"
    if "landwey" in text or "veritasi" in text or "alaro" in text: return "🕵️ COMPETITOR INTEL"
    return "💡 OPPORTUNITY"

def is_clean_lead(text):
    """The 'No-Noise' Filter. Checks for location and blocklisted terms."""
    text = text.lower()
    # Rule 1: Instant discard for blocked terms
    if any(word in text for word in BLOCK_LIST):
        return False
    # Rule 2: Must mention a target region or country
    continents = ["nigeria", "ghana", "kenya", "africa"]
    if any(loc in text for loc in TARGET_CITIES + continents):
        return True
    return False

def send_telegram_card(name, location, text, link):
    """Sends a high-end, agency-style lead card to your Telegram Bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    intent = get_intent_tag(text)
    
    # AGENCY BRANDED LAYOUT
    message = (
        f"💎 **{intent} FOUND**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Lead:** {name}\n"
        f"📍 **Focus:** {location.upper()}\n"
        f"🌐 **Source:** 🐦 X (via Serper)\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Signal:** \"{text[:180]}...\"\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [OPEN X PROFILE]({link})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🛡️ *Davies | Superite Partner Engine*"
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
        total_leads = 0
        serper_url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }

        for query in QUERIES:
            # We use POST for Serper for cleaner results
            payload = json.dumps({"q": query, "num": 15})
            try:
                response = requests.post(serper_url, headers=headers, data=payload, timeout=15)
                # Parse the 'organic' results from Serper
                results = response.json().get('organic', [])
                
                for result in results:
                    title = result.get('title', '')
                    snippet = result.get('snippet', '')
                    link = result.get('link', '')

                    # Apply Premium Filtering
                    if is_clean_lead(title + " " + snippet):
                        # Clean X profile name
                        name = title.split('(@')[0].split('|')[0].strip()
                        
                        # Identify specific city for the tag
                        found_loc = "Pan-Africa"
                        for city in TARGET_CITIES:
                            if city in (title + snippet).lower():
                                found_loc = city
                                break
                        
                        send_telegram_card(name, found_loc, snippet, link)
                        total_leads += 1
                        
            except Exception as e:
                print(f"Query Error: {e}")

        # Vercel Success Response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "active",
            "partner": "Davies | Superite Africa",
            "engine": "Serper_Premium_2026",
            "leads_pushed": total_leads
        }).encode())
    
