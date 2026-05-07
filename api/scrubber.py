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

# --- THE DEEP SCRUB QUERIES ---
# Uses advanced 2026 operators to find discussion threads and contact info
DEEP_QUERIES = [
    'site:nairaland.com "diaspora" "property" 2026',
    'site:reddit.com "buy house" "Lagos" (UK OR USA OR Canada)',
    'site:quora.com "invest in Nigeria" "real estate" (London OR Houston)',
    'intext:"@gmail.com" "Nigerian professional" (UK OR USA) "real estate"',
    'intitle:"index of" "Nigerian diaspora" contact list filetype:csv'
]

def send_to_telegram(name, source, contact_snippet, link, category):
    """Sends a high-conversion 'Scrubber Card' to your phone."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Premium Dark-Mode Style Formatting
    message = (
        "🕵️ **DEEP SCRUBBER ALERT**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🏷️ **Category:** {category}\n"
        f"👤 **Lead/Source:** {name}\n"
        f"🌐 **Platform:** {source}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 **Data Found:** \"{contact_snippet[:150]}...\"\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [INVESTIGATE SOURCE]({link})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🛠️ *Ready for direct reach-out via Email/DM*"
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
        print(f"Telegram Dispatch Error: {e}")

class handler(BaseHTTPRequestHandler):
    """Vercel Entry Point for Deep Scrubbing"""
    def do_GET(self):
        # 2026 Stealth User-Agents
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        scrub_count = 0
        for query in DEEP_QUERIES:
            # udm=18 is the 2026 Google parameter for "Forums & Discussions"
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.google.com/search?q={encoded_query}&udm=18"
            
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
                        snippet = snippet_elem.text if snippet_elem else "Source inquiry."

                        # Logic to categorize the lead type
                        if "nairaland" in link: category, source = "Forum Thread", "Nairaland"
                        elif "@gmail" in snippet: category, source = "Direct Email Found", "Web Scan"
                        elif "reddit" in link: category, source = "Discussion", "Reddit"
                        else: category, source = "Business Lead", "Google Index"

                        send_to_telegram(title[:50], source, snippet, link, category)
                        scrub_count += 1
                        time.sleep(3) # Heavy stealth to protect Vercel IP

            except Exception as e:
                print(f"Scrubber skip: {e}")

        # Response for Vercel Cron
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "Scrub Complete",
            "new_leads": scrub_count,
            "engine": "Scrubber-Premium-V2"
        }).encode())
        return

