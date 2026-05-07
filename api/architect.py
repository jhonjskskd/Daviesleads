import requests
import json
import time
from http.server import BaseHTTPRequestHandler

# --- 2026 PROFESSIONAL CONFIGURATION ---
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

def generate_pitch(name, location, status):
    """
    Creates a tailored, high-end pitch based on the lead's profile.
    Uses a minimalist, corporate tone suitable for Diaspora professionals.
    """
    if "HNW" in status:
        # Pitch for Directors/CEOs
        pitch = (
            f"Hello {name}, I noticed your impressive work in {location}. "
            "I am representing Superite Africa, specializing in high-yield, "
            "title-verified luxury real estate for Diaspora executives. "
            "We focus on secure land banking and 'Smart Home' developments in Lekki and Ikoyi. "
            "Would you be open to a brief overview of our 2026 Portfolio?"
        )
    else:
        # Pitch for general professionals
        pitch = (
            f"Hi {name}, given your base in {location}, I wanted to reach out. "
            "Many Nigerians in the UK/US are looking for safe ways to build home. "
            "Superite Africa provides fully verified property options with zero-stress "
            "legal backing. I can help you secure a prime plot or home today."
        )
    return pitch

def send_to_telegram(name, pitch, link):
    """Delivers the ready-to-use pitch to your phone."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Premium Outreach Layout
    message = (
        "🚀 **READY-TO-SEND OUTREACH**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Recipient:** {name}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📋 **COPY THIS PITCH:**\n\n"
        f"_{pitch}_\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [OPEN SOURCE TO PASTE]({link})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⭐ *Tip: Send via DM or Email for best results.*"
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
        print(f"Architect Dispatch Error: {e}")

class handler(BaseHTTPRequestHandler):
    """Vercel Entry Point for Outreach Architecture"""
    def do_GET(self):
        # In a real factory, this would pull from a database. 
        # Here, it generates the 'Template of the Hour' for your top leads.
        
        # Simulated 'Hot Lead' for demonstration logic
        hot_leads = [
            {"name": "Dr. Adeyemi", "loc": "London, UK", "stat": "HNW", "url": "https://x.com"},
            {"name": "Engr. Okoro", "loc": "Houston, USA", "stat": "Verified", "url": "https://x.com"}
        ]

        for lead in hot_leads:
            pitch = generate_pitch(lead['name'], lead['loc'], lead['stat'])
            send_to_telegram(lead['name'], pitch, lead['url'])
            time.sleep(2)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "Outreach Templates Generated",
            "engine": "Architect-Premium-V4"
        }).encode())
        return

