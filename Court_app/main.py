import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, date, timedelta
import pdfkit
import json
from io import BytesIO

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('court_data.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            year INTEGER,
            court_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            raw_response TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS case_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id INTEGER,
            parties TEXT,
            filing_date TEXT,
            next_hearing_date TEXT,
            case_status TEXT,
            judgment_url TEXT,
            FOREIGN KEY (query_id) REFERENCES queries (id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS cause_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            court_type TEXT,
            list_date DATE,
            pdf_path TEXT,
            raw_data TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

class CourtScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_high_court(self, case_type, case_number, year):
        """Scrape data from High Court portal"""
        try:
            # This is a simplified example - actual implementation would need to reverse engineer the portal
            base_url = "https://hcservices.ecourts.gov.in/hcservices/main.php"
            
            # First, get the session and required tokens (this would need actual reverse engineering)
            response = self.session.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Mock data for demonstration - in real implementation, you'd parse the actual response
            mock_data = {
                'parties': f"Petitioner: John Doe vs Respondent: State of Example",
                'filing_date': "2023-05-15",
                'next_hearing_date': (date.today() + timedelta(days=7)).strftime("%Y-%m-%d"),
                'case_status': "Pending",
                'judgment_url': None  # Would be actual URL if available
            }
            
            return mock_data, response.text
            
        except Exception as e:
            return {'error': str(e)}, None
    
    def scrape_district_court(self, case_type, case_number, year):
        """Scrape data from District Court portal"""
        try:
            base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"
            
            # Similar approach as high court
            response = self.session.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Mock data for demonstration
            mock_data = {
                'parties': f"Applicant: Jane Smith vs Opponent: ABC Corporation",
                'filing_date': "2023-06-20",
                'next_hearing_date': (date.today() + timedelta(days=5)).strftime("%Y-%m-%d"),
                'case_status': "Hearing",
                'judgment_url': None
            }
            
            return mock_data, response.text
            
        except Exception as e:
            return {'error': str(e)}, None
    
    def download_cause_list(self, court_type, target_date=None):
        """Download and parse cause list for a specific date"""
        if target_date is None:
            target_date = date.today() + timedelta(days=1)  # Tomorrow's list
        
        try:
            # This would need actual implementation based on court portal structure
            if court_type == "high_court":
                url = "https://hcservices.ecourts.gov.in/hcservices/main.php"
            else:
                url = "https://services.ecourts.gov.in/ecourtindia_v6/"
            
            response = self.session.get(url)
            
            # Mock cause list data
            cause_list_data = {
                'court': f"{court_type.replace('_', ' ').title()} Court",
                'date': target_date.strftime("%Y-%m-%d"),
                'cases': [
                    {'case_number': 'CR123/2023', 'case_type': 'Criminal', 'parties': 'State vs John Doe'},
                    {'case_number': 'CV456/2023', 'case_type': 'Civil', 'parties': 'Smith vs Jones'},
                    {'case_number': 'FA789/2023', 'case_type': 'Family', 'parties': 'Doe vs Doe'}
                ]
            }
            
            # Generate PDF
            pdf_content = self.generate_cause_list_pdf(cause_list_data)
            
            return cause_list_data, pdf_content, response.text
            
        except Exception as e:
            return {'error': str(e)}, None, None
    
    def generate_cause_list_pdf(self, cause_list_data):
        """Generate PDF from cause list data"""
        html_content = f"""
        <html>
        <head>
            <title>Cause List - {cause_list_data['court']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>{cause_list_data['court']} - Cause List</h1>
            <h2>Date: {cause_list_data['date']}</h2>
            <table>
                <tr>
                    <th>Case Number</th>
                    <th>Case Type</th>
                    <th>Parties</th>
                </tr>
                {"".join(f'<tr><td>{case["case_number"]}</td><td>{case["case_type"]}</td><td>{case["parties"]}</td></tr>' 
                         for case in cause_list_data['cases'])}
            </table>
        </body>
        </html>
        """
        
        try:
            return pdfkit.from_string(html_content, False)
        except:
            # Fallback: Create simple text PDF
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, f"{cause_list_data['court']} - Cause List")
            p.drawString(100, 730, f"Date: {cause_list_data['date']}")
            
            y_position = 700
            for case in cause_list_data['cases']:
                p.drawString(100, y_position, f"{case['case_number']} - {case['case_type']}")
                p.drawString(100, y_position - 15, f"Parties: {case['parties']}")
                y_position -= 40
                if y_position < 100:
                    p.showPage()
                    y_position = 750
            
            p.save()
            return buffer.getvalue()

scraper = CourtScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_case', methods=['POST'])
def search_case():
    case_type = request.form.get('case_type')
    case_number = request.form.get('case_number')
    year = request.form.get('year')
    court_type = request.form.get('court_type', 'district_court')
    
    if not all([case_type, case_number, year]):
        return jsonify({'error': 'All fields are required'}), 400
    
    try:
        year = int(year)
    except ValueError:
        return jsonify({'error': 'Year must be a number'}), 400
    
    # Scrape data based on court type
    if court_type == 'high_court':
        case_data, raw_response = scraper.scrape_high_court(case_type, case_number, year)
    else:
        case_data, raw_response = scraper.scrape_district_court(case_type, case_number, year)
    
    if 'error' in case_data:
        return jsonify({'error': case_data['error']}), 500
    
    # Store query and response in database
    conn = sqlite3.connect('court_data.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO queries (case_type, case_number, year, court_type, raw_response)
        VALUES (?, ?, ?, ?, ?)
    ''', (case_type, case_number, year, court_type, raw_response))
    
    query_id = c.lastrowid
    
    c.execute('''
        INSERT INTO case_details (query_id, parties, filing_date, next_hearing_date, case_status, judgment_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (query_id, case_data['parties'], case_data['filing_date'], 
          case_data['next_hearing_date'], case_data['case_status'], case_data.get('judgment_url')))
    
    conn.commit()
    conn.close()
    
    return jsonify(case_data)

@app.route('/download_cause_list', methods=['POST'])
def download_cause_list():
    court_type = request.form.get('court_type', 'district_court')
    target_date = request.form.get('date')
    
    if target_date:
        try:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    else:
        target_date = date.today() + timedelta(days=1)
    
    cause_list_data, pdf_content, raw_response = scraper.download_cause_list(court_type, target_date)
    
    if 'error' in cause_list_data:
        return jsonify({'error': cause_list_data['error']}), 500
    
    # Store cause list in database
    conn = sqlite3.connect('court_data.db')
    c = conn.cursor()
    
    pdf_filename = f"cause_list_{court_type}_{target_date.strftime('%Y%m%d')}.pdf"
    pdf_path = os.path.join('static', 'pdfs', pdf_filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    with open(pdf_path, 'wb') as f:
        f.write(pdf_content)
    
    c.execute('''
        INSERT INTO cause_lists (court_type, list_date, pdf_path, raw_data)
        VALUES (?, ?, ?, ?)
    ''', (court_type, target_date.strftime('%Y-%m-%d'), pdf_path, raw_response))
    
    conn.commit()
    conn.close()
    
    return send_file(
        BytesIO(pdf_content),
        download_name=pdf_filename,
        as_attachment=True,
        mimetype='application/pdf'
    )

@app.route('/check_case_in_cause_list', methods=['POST'])
def check_case_in_cause_list():
    case_number = request.form.get('case_number')
    court_type = request.form.get('court_type', 'district_court')
    target_date = request.form.get('date')
    
    if not case_number:
        return jsonify({'error': 'Case number is required'}), 400
    
    if target_date:
        try:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    else:
        target_date = date.today() + timedelta(days=1)
    
    cause_list_data, _, _ = scraper.download_cause_list(court_type, target_date)
    
    if 'error' in cause_list_data:
        return jsonify({'error': cause_list_data['error']}), 500
    
    # Check if case is in cause list
    found = any(case['case_number'] == case_number for case in cause_list_data.get('cases', []))
    
    return jsonify({
        'found': found,
        'date': target_date.strftime('%Y-%m-%d'),
        'court': court_type,
        'case_number': case_number
    })

if __name__ == '__main__':
    app.run(debug=True)