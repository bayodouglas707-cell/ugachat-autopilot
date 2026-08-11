import os
import json
import urllib.request
import urllib.parse

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def generate_ai_market_article(topic="Uganda Bulk Fuel Prices & Gold Market Forecast"):
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY is missing!")
        return None, None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
    Write a 600-word high-converting SEO blog post about: '{topic}'.
    Target Audience: East African petroleum buyers, fuel depot managers in Kampala, and MetaTrader 4/5 Gold EA traders.
    Requirements:
    1. First line MUST be an engaging title starting with 'TITLE:'
    2. Provide 3 structured sections with <h2> subheadings.
    3. Include projected price trends for AGO Diesel, PMS Petrol, and Gold Spot (XAUUSD).
    4. Conclude with a strong Call to Action to contact UGAChat WhatsApp sales desk (+256779595328) or get Mutan Gold Scalper EA at ugachat.mutan.store.
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

def send_telegram_alert(title, article_url="https://ugachat.mutan.store"):
    if not TELEGRAM_BOT_TOKEN:
        print("Telegram Token missing, skipping Telegram broadcast.")
        return

    msg = f"<b>📰 NEW MARKET REPORT PUBLISHED!</b>\n\n<b>{title}</b>\n\nRead full analysis & price forecasts here:\n👉 <a href='{article_url}'>ugachat.mutan.store</a>\n\n📲 <i>WhatsApp Desk: +256 779 595 328</i>"
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
            print("Telegram alert successfully sent to @mutanstore!")
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
        send_telegram_alert(title)
        print("=== AUTOPILOT PIPELINE COMPLETE! ===")

if __name__ == "__main__":
    run_autopilot_pipeline()
