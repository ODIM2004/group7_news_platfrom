from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "group7_secret_key" 

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()
    # We maintain the history table to satisfy Point 7 of the Project Outline (DBMS)
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY, 
                  name TEXT, 
                  preferences TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- NEWS FETCHING ENGINE ---
def get_news(category):
    # Live API Key
    api_key = "ebdafebcdf6d45cd94ba80073deb4f7c" 
    
    # Attempt live fetch first
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('articles', [])
    except:
        pass

    # Fallback to public mirror if primary API fails or limit is reached
    fallback_url = f"https://saurav.tech/NewsAPI/top-headlines/category/{category}/us.json"
    try:
        response = requests.get(fallback_url, timeout=5)
        data = response.json()
        return data.get('articles', [])
    except:
        return []

# --- CORE ROUTES ---

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
    # Mapping 'entertainment' to 'Culture' for the UI display
    title = category_name.capitalize() if category_name != 'entertainment' else 'Culture'
    return render_template('index.html', news=articles, current_category=title)

# --- GENERATOR LOGIC ---

@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    name = request.form.get('name', 'Reader')
    selected_categories = request.form.getlist('categories')
    
    if not selected_categories:
        selected_categories = ['general']

    # Log interaction to Database (Software Engineering Requirement)
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()
    prefs_str = ",".join(selected_categories)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (name, preferences, timestamp) VALUES (?, ?, ?)", 
              (name, prefs_str, timestamp))
    conn.commit()
    conn.close()

    # Prepare briefing data
    summary_data = {}
    for cat in selected_categories:
        articles = get_news(cat)
        summary_data[cat.capitalize()] = articles[:3] # Get top 3 per sector

    return render_template('summary.html', name=name, summary_data=summary_data, timestamp=timestamp)

# --- SYSTEM MONITORING (ADMIN) ---

@app.route('/admin')
def admin_panel():
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    
    # Styled System Log for Defense Presentation
    html = """
    <div style="font-family: 'Inter', sans-serif; padding: 40px; max-width: 1000px; margin: 0 auto; color: #1e293b;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px;">
            <div>
                <h1 style="margin: 0; color: #0f172a;">📂 System Activity Logs</h1>
                <p style="margin: 5px 0 0; color: #64748b;">Backend: Python/Flask | DBMS: SQLite3</p>
            </div>
            <a href="/" style="padding: 10px 20px; background: #0891b2; color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">&larr; Exit Admin</a>
        </div>
        
        <table style="width: 100%; border-collapse: collapse; margin-top: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-radius: 12px; overflow: hidden;">
            <tr style="background-color: #f8fafc; text-align: left; font-weight: bold; color: #475569; border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 15px;">REF_ID</td>
                <td style="padding: 15px;">EXECUTIVE NAME</td>
                <td style="padding: 15px;">TOPIC SELECTIONS</td>
                <td style="padding: 15px;">TIMESTAMP</td>
            </tr>
    """
    for row in logs:
        html += f"""
        <tr style='border-bottom: 1px solid #f1f5f9;'>
            <td style="padding: 15px; color: #94a3b8;">#00{row[0]}</td>
            <td style="padding: 15px; font-weight: 600;">{row[1]}</td>
            <td style="padding: 15px;"><span style="background: #ecfeff; color: #0891b2; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem;">{row[2]}</span></td>
            <td style="padding: 15px; color: #64748b; font-size: 0.9rem;">{row[3]}</td>
        </tr>"""
    
    if not logs:
        html += "<tr><td colspan='4' style='padding: 40px; text-align: center; color: #94a3b8;'>No system activity detected yet.</td></tr>"
        
    html += "</table></div>"
    return html

if __name__ == '__main__':
    app.run(debug=True)
