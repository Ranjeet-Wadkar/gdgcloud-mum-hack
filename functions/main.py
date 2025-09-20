"""
Firebase Cloud Function for Research-to-Startup AI Agent Swarm
"""

import functions_framework
import json
import os
import tempfile
import logging
from flask import Flask, request, jsonify
from google.cloud import storage
from google.cloud import firestore
import subprocess
import sys
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase services
storage_client = storage.Client()
db = firestore.Client()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Research-to-Startup AI Agent Swarm</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.2em;
        }
        .upload-area {
            border: 3px dashed #3498db;
            border-radius: 15px;
            padding: 60px;
            text-align: center;
            margin: 30px 0;
            background: linear-gradient(45deg, #f8f9fa, #e3f2fd);
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            background: linear-gradient(45deg, #e3f2fd, #bbdefb);
            transform: translateY(-2px);
        }
        .upload-icon {
            font-size: 4em;
            color: #3498db;
            margin-bottom: 20px;
        }
        input[type="file"] {
            margin: 20px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: 100%;
            max-width: 400px;
        }
        button {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 18px;
            margin: 10px 5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
        }
        .result {
            margin-top: 30px;
            padding: 25px;
            border-radius: 10px;
            border-left: 5px solid #27ae60;
            background: linear-gradient(45deg, #e8f5e8, #d4edda);
        }
        .error {
            background: linear-gradient(45deg, #fdf2f2, #f8d7da);
            border-left-color: #e74c3c;
        }
        .loading {
            text-align: center;
            padding: 40px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 2s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .feature {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .feature-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Research-to-Startup AI Agent Swarm</h1>
        <p class="subtitle">Transform your research papers into investor-ready pitch decks using AI</p>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">📊</div>
                <h3>Market Analysis</h3>
                <p>AI-powered market intelligence and competitor analysis</p>
            </div>
            <div class="feature">
                <div class="feature-icon">💼</div>
                <h3>Business Planning</h3>
                <p>Comprehensive business plans and feasibility studies</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🎯</div>
                <h3>Investor Matching</h3>
                <p>Find the perfect investors for your startup</p>
            </div>
        </div>
        
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-area">
                <div class="upload-icon">📄</div>
                <h3>Upload Your Research Paper</h3>
                <p>Supported formats: PDF, TXT, DOCX</p>
                <input type="file" id="fileInput" name="file" accept=".pdf,.txt,.docx" required>
                <br>
                <button type="submit">Generate Pitch Deck</button>
            </div>
        </form>
        
        <div id="result" style="display: none;"></div>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const fileInput = document.getElementById('fileInput');
            const resultDiv = document.getElementById('result');
            
            if (!fileInput.files[0]) {
                alert('Please select a file');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            // Show loading
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>🤖 AI agents are analyzing your research paper...</p>
                    <p>This may take 2-3 minutes. Please don't close this page.</p>
                </div>
            `;
            
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    resultDiv.innerHTML = `
                        <div class="result">
                            <h3>✅ Pitch Deck Generated Successfully!</h3>
                            <p><strong>📁 Download:</strong> <a href="${result.download_url}" target="_blank" style="color: #3498db; text-decoration: none; font-weight: bold;">${result.filename}</a></p>
                            <p><strong>📋 Summary:</strong> ${result.summary}</p>
                            <p><strong>⏰ Generated:</strong> ${new Date().toLocaleString()}</p>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div class="result error">
                            <h3>❌ Error</h3>
                            <p>${result.error}</p>
                        </div>
                    `;
                }
            } catch (error) {
                resultDiv.innerHTML = `
                    <div class="result error">
                        <h3>❌ Error</h3>
                        <p>Failed to process request: ${error.message}</p>
                    </div>
                `;
            }
        });
    </script>
</body>
</html>
"""

@functions_framework.http
def app(request):
    """Main HTTP function for Firebase Hosting"""
    if request.method == 'GET':
        return HTML_TEMPLATE
    elif request.method == 'POST' and request.path == '/process':
        return process_research_paper(request)
    else:
        return jsonify({'error': 'Method not allowed'}), 405

def process_research_paper(request):
    """Process uploaded research paper and generate pitch deck"""
    try:
        # Get uploaded file
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'.pdf', '.txt', '.docx'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload PDF, TXT, or DOCX files.'}), 400
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            file.save(tmp_file.name)
            temp_file_path = tmp_file.name
        
        try:
            # Create a simple processing script
            processing_script = f'''
import sys
import os
sys.path.append("/workspace")

# Import required modules
try:
    from utils.parser import extract_text_from_pdf, clean_text, validate_text_input
    from agents.research_agent import run_research_agent
    from agents.market_agent import run_market_agent
    from agents.feasibility_agent import run_feasibility_agent
    from agents.stakeholder_agent import run_stakeholder_agent
    from agents.business_plan_agent import run_business_plan_agent
    from utils.deck_generator import create_pitch_deck, generate_deck_summary
    import json
    import os
    from datetime import datetime
    
    print("Starting processing...")
    
    # Process the file
    print("Extracting text from file...")
    text = extract_text_from_pdf("{temp_file_path}")
    cleaned_text = clean_text(text)
    
    if not validate_text_input(cleaned_text):
        print("ERROR: Invalid text input")
        sys.exit(1)
    
    print("Running research agent...")
    research_result = run_research_agent(cleaned_text)
    
    print("Running market agent...")
    market_result = run_market_agent(research_result["output"])
    
    print("Running feasibility agent...")
    feasibility_result = run_feasibility_agent(research_result["output"], market_result["output"])
    
    print("Running stakeholder agent...")
    stakeholder_result = run_stakeholder_agent(research_result["output"], market_result["output"], feasibility_result["output"])
    
    print("Running business plan agent...")
    business_plan_result = run_business_plan_agent(research_result["output"], market_result["output"], feasibility_result["output"], stakeholder_result["output"])
    
    # Generate pitch deck
    print("Generating pitch deck...")
    agent_outputs = {{
        "research_agent": research_result["output"],
        "market_agent": market_result["output"],
        "feasibility_agent": feasibility_result["output"],
        "stakeholder_agent": stakeholder_result["output"],
        "business_plan_agent": business_plan_result["output"]
    }}
    
    output_path = "/tmp/pitch_deck.pdf"
    create_pitch_deck(agent_outputs, output_path)
    summary = generate_deck_summary(agent_outputs)
    
    print(f"SUCCESS:{output_path}:{summary}")
    
except Exception as e:
    print(f"ERROR:{str(e)}")
    sys.exit(1)
'''
            
            # Write processing script to temporary file
            script_path = "/tmp/process_script.py"
            with open(script_path, 'w') as f:
                f.write(processing_script)
            
            # Run the processing script
            result = subprocess.run([
                'python', script_path
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                output_line = result.stdout.strip().split('\n')[-1]
                if output_line.startswith('SUCCESS:'):
                    parts = output_line.split(':', 2)
                    if len(parts) >= 3:
                        output_path = parts[1]
                        summary = parts[2]
                        
                        # Upload to Firebase Storage
                        bucket_name = os.environ.get('BUCKET_NAME', 'your-project-id.appspot.com')
                        bucket = storage_client.bucket(bucket_name)
                        
                        # Generate unique filename
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"pitch_deck_{timestamp}.pdf"
                        blob = bucket.blob(f"pitch_decks/{filename}")
                        
                        # Upload file
                        blob.upload_from_filename(output_path)
                        blob.make_public()
                        
                        # Store metadata in Firestore
                        doc_ref = db.collection('pitch_decks').document()
                        doc_ref.set({
                            'filename': filename,
                            'download_url': blob.public_url,
                            'summary': summary,
                            'created_at': datetime.now(),
                            'file_size': os.path.getsize(output_path)
                        })
                        
                        return jsonify({
                            'success': True,
                            'filename': filename,
                            'download_url': blob.public_url,
                            'summary': summary
                        })
                
            return jsonify({
                'success': False, 
                'error': f'Processing failed: {result.stderr}'
            }), 500
            
        finally:
            # Clean up temporary files
            for path in [temp_file_path, "/tmp/process_script.py"]:
                if os.path.exists(path):
                    os.unlink(path)
                
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'Internal server error: {str(e)}'
        }), 500
