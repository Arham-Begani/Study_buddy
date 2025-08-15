import os
import io
import google.generativeai as genai
from io import StringIO
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv


try:
    import google.generativeai as genai
except Exception:
    genai = None

load_dotenv()
API_KEY = os.getenv("keys", "").strip()
USE_GEMINI = bool(API_KEY and genai)

if USE_GEMINI:
    genai.configure(api_key=API_KEY)
    GEM_MODEL = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

def ai_complete(prompt: str) -> str:
    """Use Gemini if available, otherwise deterministic offline fallback."""
    
    if USE_GEMINI:
        try:
            resp = GEM_MODEL.generate_content(prompt)
            return (resp.text or "").strip() or "(empty AI response)"
        except Exception as e:
            return f"(AI error: {e})"
    
    
    

@app.route("/")
def home():
    return render_template("index.html")

