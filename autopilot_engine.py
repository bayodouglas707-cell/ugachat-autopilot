import os
import json
import smtplib
import urllib.request
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BLOGGER_POST_EMAIL = os.getenv("BLOGGER_POST_EMAIL")
GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

STRIPE_199_URL = "https://buy.stripe.com/cNieVda6tdaN2Bkgv424000"

def generate_ai_market_article(topic):
    """Generates an 800-word high-CPM SEO article via Gemini REST API"""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY secret is missing in GitHub repository!")
        return None, None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
    Write an 800-word high-converting SEO blog post about: '{topic}'.
    Target Audience: East African petroleum buyers, fuel depot managers in Kampala, and MetaTrader 4/5 Gold EA traders.
    
    Requirements:
    1. First line MUST be an engaging title starting with 'TITLE:'
    2. Include structured sections with <h2> subheadings targeting high CPM keywords (AGO Diesel Uganda, PMS Petrol Kampala, MT4 Gold Scalper EA, FTMO EA Bot).
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

def send_post_via_email(title, html_content):
    """Publishes article to Blogger via Email-to-Post (100% Reliability)"""
    if not BLOGGER_POST_EMAIL or not GMAIL_SENDER_EMAIL or not GMAIL_APP_PASSWORD:
        print("Notice: Email-to-Post credentials missing in GitHub Secrets.")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = GMAIL_SENDER_EMAIL
        msg['To'] = BLOGGER_POST_EMAIL

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_SENDER_EMAIL, BLOGGER_POST_EMAIL, msg.as_string())
        server.quit()
        print(f"✅ Article published to Blogger via Email-to-Post! Title: {title}")
        return True
    except Exception as e:
        print(f"Email-to-Post failed: {e}")
        return False

def ping_search_engines():
    """Notifies Google & Bing search crawlers to index new article instantly"""
    sitemap_url = "https://ugachat.mutan.store/sitemap.xml"
    google_ping = f"https://www.google.com/ping?sitemap={sitemap_url}"
    bing_ping = f"https://www.bing.com/ping?sitemap={sitemap_url}"
    
    for ping_url in [google_ping, bing_ping]:
        try:
            req = urllib.request.Request(ping_url, headers={'User-Agent': 'Mozilla/5.0'})
            urllib.request.urlopen(req)
            print(f"✅ Search Engine Indexing Ping Sent: {ping_url}")
        except Exception as e:
            print(f"Search engine ping notice: {e}")

def send_telegram_alert(title):
    """Dispatches breaking article alert with direct Stripe payment links to VIP Telegram Channel"""
    if not TELEGRAM_BOT_TOKEN:
        print("Telegram Token missing, skipping alert.")
        return

    msg = f"<b>📰 NEW MARKET REPORT PUBLISHED!</b>\n\n<b>{title}</b>\n\nRead full analysis &amp; price forecasts here:\n👉 <a href='https://ugachat.mutan.store'>ugachat.mutan.store</a>\n\n💳 <b>Buy Mutan Gold Scalper EA ($199 via Stripe Card):</b>\n👉 <a href='{STRIPE_199_URL}'>Instant Stripe Card Checkout</a>\n\n📲 <i>WhatsApp Desk: +256 779 595 328</i>"
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
            print("✅ Telegram alert sent to @mutanstore!")
    except Exception as e:
        print(f"Telegram dispatch notice: {e}")

def run_autopilot():
    print("🚀 === STARTING UGACHAT AUTOPILOT PUBLISHER ===")
    topics = [
        "Uganda AGO Diesel Price Per Liter & Kampala Depot Supply Forecast 2026",
        "Mutan Gold Scalper PRO EA: FTMO Challenge Pass & XAUUSD Scalping Strategy",
        "Kampala Petroleum Market Analysis: PMS Super Petrol & Jet A-1 Depot Clearance"
    ]
    for topic in topics:
        title, content = generate_ai_market_article(topic)
        if title and content:
            success = send_post_via_email(title, content)
            if success:
                send_telegram_alert(title)
                ping_search_engines()

if __name__ == "__main__":
    run_autopilot()
