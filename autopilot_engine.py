import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BLOGGER_BLOG_ID = os.getenv("BLOGGER_BLOG_ID", "6168654040097988880")
BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY", "AIzaSyC-btp72QgiMYo3bc9mhaSDdJIrvG04V-U")

# Live Stripe Payment Links
STRIPE_199_URL = "https://buy.stripe.com/cNieVda6tdaN2Bkgv424000"
STRIPE_499_URL = "https://buy.stripe.com/fZu6oH4M9eeRb7Q6Uu24001"

def generate_ai_market_article(topic="Uganda Bulk Fuel Prices & Gold Market Forecast"):
    """Generates an 800-word SEO blog article via Gemini REST API"""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY is not set!")
        return None, None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
    Write a 600-word high-converting SEO blog post about: '{topic}'.
    Target Audience: East African petroleum buyers, fuel depot managers in Kampala, and MetaTrader 4/5 Gold EA traders.
    Requirements:
    1. First line MUST be an engaging title starting with 'TITLE:'
    2. Provide 3 structured sections with <h2> subheadings.
    3. Include projected price trends for AGO Diesel, PMS Petrol, and Gold Spot (XAUUSD).
    4. Conclude with a strong Call to Action:
       - Direct readers to buy Mutan Gold Scalper EA via Stripe Checkout ({STRIPE_199_URL}).
       - Contact UGAChat WhatsApp sales desk (+256779595328).
    Format the main body as clean HTML.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            full_text = res_data['candidates'][0]['content']['parts'][0]['text']
            
            lines = full_text.strip().split('\n')
            title = topic
            body = full_text
            for i, line in enumerate(lines):
                if line.startswith('TITLE:'):
                    title = line.replace('TITLE:', '').strip()
                    body = '\n'.join(lines[i+1:])
                    break
            
            print(f"Generated Article Title: '{title}'")
            return title, body
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None, None

def post_to_blogger(title, content_html):
    """Publishes article directly to Google Blogger API v3"""
    if not BLOGGER_BLOG_ID or not BLOGGER_API_KEY:
        print("Blogger credentials missing.")
        return "https://ugachat.mutan.store"
        
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/?key={BLOGGER_API_KEY}"
    payload = {
        "kind": "blogger#post",
        "title": title,
        "content": content_html
    }
    headers = {"Content-Type": "application/json"}
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            post_url = res_data.get('url', 'https://ugachat.mutan.store')
            print(f"Article published successfully to Blogger! URL: {post_url}")
            return post_url
    except Exception as e:
        print(f"Blogger API response notice: {e}")
        return "https://ugachat.mutan.store"

def send_telegram_alert(title, article_url="https://ugachat.mutan.store"):
    """Dispatches breaking article alert with direct Stripe payment links to VIP Telegram Channel"""
    if not TELEGRAM_BOT_TOKEN:
        print("Telegram Token missing, skipping alert.")
        return

    msg = f"<b>📰 NEW MARKET REPORT PUBLISHED!</b>\n\n<b>{title}</b>\n\nRead full analysis &amp; price forecasts here:\n👉 <a href='{article_url}'>ugachat.mutan.store</a>\n\n💳 <b>Buy Mutan Gold Scalper EA ($199 via Stripe Card):</b>\n👉 <a href='{STRIPE_199_URL}'>Instant Stripe Card Checkout</a>\n\n📲 <i>WhatsApp Desk: +256 779 595 328</i>"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": "@mutanstore",
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    headers = {"Content-Type": "application/json"}
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            print("Telegram alert with live Stripe checkout links sent to @mutanstore!")
    except Exception as e:
        print(f"Telegram dispatch notice: {e}")

def run_autopilot_pipeline():
    print("=== STARTING UGACHAT AUTOPILOT AI PIPELINE ===")
    topics = [
        "Uganda Bulk Fuel Price Trends 2026: AGO Diesel & PMS Petrol Forecast",
        "Gold Spot (XAUUSD) Technical Analysis & Mutan Scalper EA Setup",
        "East Africa Energy Supply: Kampala & Jinja Depot Clearance Advisory"
    ]
    import random
    selected_topic = random.choice(topics)
    
    title, body_html = generate_ai_market_article(selected_topic)
    if title and body_html:
        print("Article generated successfully!")
        post_url = post_to_blogger(title, body_html)
        send_telegram_alert(title, post_url)
        print("=== AUTOPILOT PIPELINE COMPLETE! ===")

if __name__ == "__main__":
    run_autopilot_pipeline()
