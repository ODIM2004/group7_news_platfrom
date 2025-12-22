from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY, 
                  name TEXT, 
                  preferences TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- NEWS FETCHING (UPDATED FOR REAL-TIME) ---
def get_news(category):
    """
    Fetches news. Tries the Live API first. 
    If no API key is provided, falls back to the Cached API.
    """
    
    # ---------------------------------------------------------
    # STEP 1: GET YOUR FREE KEY AT https://newsapi.org/register
    # STEP 2: PASTE IT INSIDE THE QUOTES BELOW
    # ---------------------------------------------------------
    api_key = "ebdafebcdf6d45cd94ba80073deb4f7c" 
    
    # 1. Try Live API (If key is set)
    if api_key != "YOUR_API_KEY_HERE":
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
        except:
            print("Live API failed, switching to backup...")

    # 2. Fallback to Cached API (If no key or error)
    # This ensures your project always works, even without a key.
    print(f"Using Cached/Backup news for {category}")
    url = f"https://saurav.tech/NewsAPI/top-headlines/category/{category}/us.json"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('articles', [])
    except:
        return []

# --- ROUTES ---

@app.route('/')
def home():
    articles = get_news('general')
    return render_template('index.html', news=articles, current_category='Top Headlines')

@app.route('/category/<category_name>')
def category_page(category_name):
    allowed = ['business', 'technology', 'sports', 'science', 'health', 'entertainment']
    if category_name not in allowed:
        return redirect(url_for('home'))
        
    articles = get_news(category_name)
    title = category_name.capitalize() + " News"
    return render_template('index.html', news=articles, current_category=title)

@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    name = request.form.get('name', 'Reader')
    selected_categories = request.form.getlist('categories')
    
    if not selected_categories:
        selected_categories = ['general']

    # Log to Database
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()
    prefs_str = ",".join(selected_categories)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (name, preferences, timestamp) VALUES (?, ?, ?)", 
              (name, prefs_str, timestamp))
    conn.commit()
    conn.close()

    # Fetch Data
    summary_data = {}
    for cat in selected_categories:
        articles = get_news(cat)
        summary_data[cat.capitalize()] = articles[:3]

    return render_template('summary.html', name=name, summary_data=summary_data, timestamp=timestamp)

@app.route('/admin')
def admin_panel():
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    
    html = """
    <div style="font-family: 'Segoe UI', sans-serif; padding: 40px; max-width: 800px; margin: 0 auto;">
        <h1 style="color: #0f172a;">📂 System Logs</h1>
        <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%; border-color: #e2e8f0;">
            <tr style="background-color: #f8fafc; text-align: left;">
                <th>ID</th><th>User</th><th>Topics</th><th>Time</th>
            </tr>
    """
    for row in logs:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    html += """</table><br><a href="/" style="color: #0891b2; text-decoration: none;">&larr; Back to App</a></div>"""
    return html

if __name__ == '__main__':
    app.run(debug=True)
