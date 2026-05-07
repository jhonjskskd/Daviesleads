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

# --- THE SEARCH ENGINE QUERIES ---
# Designed to find Nigerians in the UK, USA, and Canada looking for property.
QUERIES = [
    'site:x.com "investing" "Lagos" "real estate" (London OR UK OR USA OR Canada)',
    'site:x.com "buying" "property" "Nigeria" (diaspora OR abroad OR Houston)',
    'site:x.com "Lekki" "house" (Toronto OR Maryland OR "UK")',
    'site:nairaland.com "Diaspora" "buy land" "Lagos" 2026',
    'site:reddit.com "Nigeria" "property" (London OR Houston OR Toronto)'
]

def get_intent_tag(text):
    """Categorizes the lead based on their message."""
    text = text.lower()
    if "buy" in text or "buying" in text: return "🏠 BUYER"
    if "invest" in text or "yield" in text: return "📈 INVESTOR"
    if "build" in text or "construction" in text: return "🏗️ BUILDER"
    return "💡 OPPORTUNITY"

def send_telegram_card(name, location, text, link, platform):
    """Sends a high-end, clean lead card to your Telegram Bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    intent = get_intent_tag(text)
    platform_icon = "🐦 X" if "x.com" in link else "🇳🇬 Forum"
    
    # Modern, scannable layout
    message = (
        f"💎 **{intent} FOUND**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Name:** {name}\n"
        f"📍 **Location:** {location}\n"
        f"🌐 **Platform:** {platform_icon}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Signal:** \"{text[:150]}...\"\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [ACT NOW: OPEN {platform_icon}]({link})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 *Forwarded by your Premium Sourcing Engine*"
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
        print(f"Error sending to Telegram: {e}")

class handler(BaseHTTPRequestHandler):
    """Vercel Entry Point"""
    def do_GET(self):
        # Professional Browser Mimicry
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        ]
        
        headers = {'User-Agent': random.choice(agents)}
        total_leads = 0

        for query in QUERIES:
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            try:
                response = requests.get(search_url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Sourcing results
                for result in soup.select('.tF2Cxc'):
                    title_elem = result.select_one('.DKV0Md')
                    link_elem = result.select_one('.yuRUbf a')
                    snippet_elem = result.select_one('.VwiC3b')

                    if title_elem and link_elem:
                        title = title_elem.text
                        link = link_elem['href']
                        snippet = snippet_elem.text if snippet_elem else "Details in link."

                        # Clean Lead Identification
                        name = title.split('(@')[0].split('|')[0].strip()
                        
                        # Identify specific Diaspora Hub
                        location = "Global Diaspora"
                        hubs = ["London", "UK", "USA", "Houston", "Texas", "Canada", "Toronto", "Maryland", "New York", "Chicago"]
                        for hub in hubs:
                            if hub.lower() in (snippet + title).lower():
                                location = hub
                                break

                        # Send the data to your phone
                        send_telegram_card(name, location, snippet, link, platform_icon)
                        total_leads += 1
                        time.sleep(2) # Prevent being flagged as a bot

            except Exception as e:
                print(f"Query skip: {e}")

        # Final Response to Vercel
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "complete",
            "leads_pushed": total_leads,
            "engine": "Premium Hunter V2"
        }).encode())
        return

