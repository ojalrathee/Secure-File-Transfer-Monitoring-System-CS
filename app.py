import os
from flask import Flask, render_template, request, redirect, url_for
from integrity import calculate_sha256
from logger import log_event

app = Flask(__name__)
UPLOAD_FOLDER = './monitored_folder'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Read the audit log file to display on the webpage
    logs = []
    if os.path.exists("audit_trail.log"):
        with open("audit_trail.log", "r") as f:
            logs = f.readlines()[-25:] # Get the last 25 log entries
    return render_template('index.html', logs=logs)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Calculate integrity hash
        file_hash = calculate_sha256(file_path)
        log_event("WEB_UPLOAD", f"File uploaded via web dashboard: {file.filename} [Hash: {file_hash}]", severity="INFO")
        
        # Policy check simulation for sensitive files
        if file.filename.endswith(('.env', '.pem', '.kdbx', '.xlsx')):
            log_event("POLICY_VIOLATION", f"Sensitive file uploaded: {file.filename}", severity="ALERT")
            
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("[*] Starting Secure File Monitor Web Dashboard at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)