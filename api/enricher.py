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

# --- THE INTELLIGENCE QUERIES ---
# Designed to verify if a lead is a high-earning professional abroad
ENRICH_QUERIES = [
    'intitle:"About Us" "Director" (UK OR USA) "Nigeria"',
    'site:bloomberg.com "Nigeria" (London OR Houston)',
    'site:zoominfo.com "Nigeria" (Executive OR Manager) "London"',
    'inproceedings:"Nigerian" "Conference" (USA OR UK OR Canada) 2025..2026',
    'site:company-house.co.uk "Nigerian" Director'
]

def send_to_telegram(name, career_info, location, link, status):
    """Sends a high-end 'Intelligence Brief' to your phone."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Premium Executive Style Formatting
    message = (
        "📈 **PROFESSIONAL ENRICHMENT BRIEF**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Professional:** {name}\n"
        f"🏢 **Background:** {career_info}\n"
        f"📍 **Base:** {location}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ **Verification:** {status}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [VIEW FULL BIO]({link})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⭐ *High-value target for Luxury Real Estate*"
    )
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Enrichment Dispatch Error: {e}")

class handler(BaseHTTPRequestHandler):
    """Vercel Entry Point for Intelligence Enrichment"""
    def do_GET(self):
        # 2026 Stealth Browser Mimicry
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }

        enrich_count = 0
        for query in ENRICH_QUERIES:
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
                        link = link_elem['href']
                        title = title_elem.text
                        snippet = snippet_elem.text if snippet_elem else "Professional details found."

                        # Intelligence logic to determine wealth/status
                        status = "✅ Verified Professional"
                        if any(x in (title + snippet).lower() for x in ["director", "ceo", "founder", "manager"]):
                            status = "🔥 HIGH NET WORTH (HNW)"
                        
                        # Extract career info
                        career_info = "Professional listing"
                        if "-" in title:
                            career_info = title.split("-")[0].strip()

                        # Location Detection
                        location = "Diaspora Hub"
                        for hub in ["London", "UK", "Houston", "USA", "Canada", "Texas"]:
                            if hub.lower() in (snippet + title).lower():
                                location = hub
                                break

                        send_to_telegram(title[:50], career_info, location, link, status)
                        enrich_count += 1
                        time.sleep(4) # Slower delay for deep-dive stealth

            except Exception as e:
                print(f"Enrichment skip: {e}")

        # Final Response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "Enrichment Complete",
            "profiles_found": enrich_count,
            "engine": "Enricher-Premium-V3"
        }).encode())
        return
  
