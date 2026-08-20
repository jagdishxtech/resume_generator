"""
=============================================================================
AI RESUME PORTFOLIO GENERATOR - FLASK WEB APPLICATION
=============================================================================
Provides a web interface for users to upload (.txt, .html, .md) or paste resume text,
optionally upload custom HTML templates, generate structured portfolio HTML using Gemini API,
preview live in browser, and download portfolio.html with one click.
=============================================================================
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv

load_dotenv()

# Import generator functions from main.py
from main import (
    strip_html_tags,
    build_gemini_prompt,
    call_gemini_api,
    parse_and_validate_json,
    generate_html_portfolio,
    get_fallback_json_data
)

app = Flask(__name__, template_folder="templates")
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB Max upload

BASE_DIR = Path(__file__).parent


@app.route("/")
def index():
    """Renders the main web application UI."""
    return render_template("index.html")


@app.route("/style.css")
def serve_css():
    """Serves style.css for the portfolio iframe and standalone view."""
    return send_file(BASE_DIR / "style.css", mimetype="text/css")


@app.route("/portfolio.html")
def serve_generated_portfolio():
    """Serves the generated portfolio.html file."""
    portfolio_file = BASE_DIR / "portfolio.html"
    if not portfolio_file.exists():
        fallback_data = parse_and_validate_json(get_fallback_json_data())
        generate_html_portfolio(fallback_data, template_path=str(BASE_DIR / "template.html"), output_path=str(portfolio_file))
    return send_file(portfolio_file, mimetype="text/html")


@app.route("/api/generate", methods=["POST"])
def generate():
    """
    API Endpoint: Receives resume file upload (.txt, .html, .md) or pasted text,
    optional custom template HTML file, processes with Gemini API,
    generates portfolio.html, and returns JSON response.
    """
    try:
        resume_text = ""
        
        # Check for uploaded resume file (.txt, .html, .htm, .md)
        if 'file' in request.files and request.files['file'].filename != '':
            uploaded_file = request.files['file']
            filename = uploaded_file.filename.lower()
            raw_bytes = uploaded_file.read().decode('utf-8', errors='ignore')
            
            if filename.endswith('.html') or filename.endswith('.htm') or '<html' in raw_bytes.lower() or '<body' in raw_bytes.lower():
                print(f"[WEB APP] Extracting resume content from uploaded HTML file '{uploaded_file.filename}'...")
                resume_text = strip_html_tags(raw_bytes)
            else:
                resume_text = raw_bytes
        else:
            resume_text = request.form.get("resume_text", "")

        # Check for custom HTML template file
        custom_template_content = None
        if 'template_file' in request.files and request.files['template_file'].filename != '':
            t_file = request.files['template_file']
            custom_template_content = t_file.read().decode('utf-8', errors='ignore')
            print(f"[WEB APP] Using custom uploaded HTML template '{t_file.filename}'.")

        # Check for API Key input
        custom_api_key = request.form.get("api_key", "").strip()
        if custom_api_key:
            os.environ["GEMINI_API_KEY"] = custom_api_key

        cleaned_text = resume_text.strip()
        if not cleaned_text or len(cleaned_text) < 30:
            return jsonify({
                "success": False,
                "error": "Resume text is empty or too short. Please upload a valid .txt or .html resume file (at least 30 characters)."
            }), 400

        print(f"[WEB APP] Processing resume ({len(cleaned_text)} characters)...")
        
        # Build prompt & call Gemini API
        prompt = build_gemini_prompt(cleaned_text)
        raw_response = call_gemini_api(prompt)
        
        # Parse JSON data
        portfolio_data = parse_and_validate_json(raw_response)
        
        # Generate output portfolio.html
        output_file = BASE_DIR / "portfolio.html"
        generate_html_portfolio(
            data=portfolio_data,
            template_content=custom_template_content,
            template_path=str(BASE_DIR / "template.html"),
            output_path=str(output_file)
        )
        
        compiled_html = output_file.read_text(encoding="utf-8")
        
        return jsonify({
            "success": True,
            "message": "Portfolio generated successfully!",
            "portfolio_data": portfolio_data,
            "html_code": compiled_html
        })

    except Exception as e:
        print(f"[ERROR] Web generation failed: {e}")
        return jsonify({
            "success": False,
            "error": f"Failed to generate portfolio: {str(e)}"
        }), 500


@app.route("/api/download")
def download_portfolio():
    """Triggers browser download for portfolio.html."""
    portfolio_file = BASE_DIR / "portfolio.html"
    if not portfolio_file.exists():
        return jsonify({"error": "Portfolio has not been generated yet."}), 404
    return send_file(
        portfolio_file,
        as_attachment=True,
        download_name="portfolio.html",
        mimetype="text/html"
    )


if __name__ == "__main__":
    print("=========================================================================")
    print("[INFO] Starting AI Resume Portfolio Generator Web Application...")
    print("[INFO] Access the Web Portal at: http://127.0.0.1:5000")
    print("=========================================================================")
    app.run(host="127.0.0.1", port=5000, debug=True)
