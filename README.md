# AI-Assisted Resume Portfolio Generator & Web App

> **3-Week Bootcamp Group Project (5 Students)**  
> An automated application & web portal that converts raw resume text into a modern, glassmorphic HTML portfolio webpage using Python, Flask, Google Gemini API, JSON, HTML5, and CSS3.

---

## 📌 Project Overview
The **AI-Assisted Resume Portfolio Generator** takes a plain text resume (`resume.txt` or uploaded file), cleans and validates the content, sends it to the **Google Gemini API** with a strictly constrained prompt to extract verified structured data in **JSON** format, and dynamically renders a high-end, responsive HTML portfolio (`portfolio.html`).

### 🎯 Key Features & Web Portal
- **Web Portal (`app.py`):** Interactive browser webpage allowing users to drag-and-drop or paste their resume, preview live rendered portfolio, and download `portfolio.html` with one click!
- **CLI Tool (`main.py`):** Command-line script to convert `resume.txt` directly to `portfolio.html`.
- **AI Processing:** Google Gemini API (`gemini-2.5-flash`) returning JSON-only output with zero hallucinations.
- **Modern Styling:** Fully responsive glassmorphic design system (`style.css`).

---

## 📁 Repository Structure
```
resume-portfolio-generator/
│
├── app.py              # Flask Web Server (Web portal, API upload, live preview, download)
├── main.py             # Core application logic (file reading, Gemini API, JSON parser, HTML generator)
├── templates/
│   └── index.html      # Interactive Web Application UI (Upload dropzone, live preview tabs, download)
├── resume.txt           # Input plain text resume file
├── template.html        # HTML5 semantic portfolio template
├── style.css            # Glassmorphic CSS design system with animations & dark mode
├── requirements.txt     # Python dependencies (google-genai, python-dotenv, flask)
├── README.md            # Project documentation and submission guide
├── .gitignore           # Version control ignore configuration
├── .env.example         # Template for environment variables (Gemini API key)
└── portfolio.html       # Generated final portfolio webpage
```

---

## 🛠️ Technology Stack
| Technology | Role / Purpose |
| :--- | :--- |
| **Python 3.10+** | File processing, text cleaning, API integration, JSON validation, and HTML generation |
| **Flask** | Web server providing file upload portal, live preview endpoint, and portfolio download |
| **Gemini API** | Generative AI model (`gemini-2.5-flash`) for extracting structured JSON from text |
| **JSON** | Intermediate data schema linking Python and HTML template rendering |
| **HTML5 & CSS3** | Modern glassmorphism aesthetic, custom properties, Google Fonts, micro-animations |

---

## ⚡ Quick Start & Installation

### 1. Install Dependencies
```bash
cd resume-portfolio-generator
pip install -r requirements.txt
```

### 2. Environment Setup (Gemini API Key)
Copy `.env.example` to `.env` and add your key:
```env
GEMINI_API_KEY=AIzaSyYourActualGeminiApiKeyHere
```
*(Note: If no API key is set, the application operates in safe demo fallback mode for offline testing.)*

---

## 🚀 Running the Application

### Option A: Interactive Web App (Recommended)
Run the Flask server and open the web portal in your browser:
```bash
python app.py
```
👉 **Open Browser:** `http://127.0.0.1:5000`
- Drag & drop your `resume.txt` file or paste text directly.
- Click **"✨ Generate Portfolio Webpage"**.
- Preview live portfolio on screen and click **"📥 Download portfolio.html"**.

### Option B: Command Line (CLI Mode)
Place your resume text inside `resume.txt` and run:
```bash
python main.py
```
Open `portfolio.html` directly in your browser.
