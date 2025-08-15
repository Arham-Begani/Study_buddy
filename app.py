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
    
    
    if "explain" in prompt.lower():
        return "explanation (offline): break the topic into definitions, key formulas, and 2–3 solved examples."
    
    if "quiz" in prompt.lower():
        return "1) Q: Define inertia. A: Resistance to change in motion.\n2) Q: State Ohm’s law. A: V=IR."
    return "offline mode: no API key set; add details and try again."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "GET":
        return render_template("schedule.html")
    
    subjects_raw = request.form.get("subjects", "").strip()
    
    hours_per_day = float(request.form.get("hours", "3") or 3)
    
    days = int(request.form.get("days", "14") or 14)
    
    start_time = request.form.get("start_time", "17:00").strip()

    subjects = [s.strip() for s in subjects_raw.split(",") if s.strip()]
    if not subjects:
        subjects = ["Physics", "Math", "Chemistry", "Biology", "Social"]


    schedule_plan = []
    per_subject_block = max(hours_per_day/2, 0.5)

    def time_add(tstr, hrs):
        
        h, m = map(int, tstr.split(":"))
        total = h*60 + m + int(hrs*60)
        total %= 24*60
        
        return f"{total//60:02d}:{total%60:02d}"

    rotation = subjects[:]
    idx = 0
    for d in range(1, days+1):
        s1 = rotation[idx % len(rotation)]
        s2 = rotation[(idx+1) % len(rotation)]
        
        idx += 2
        
        t1_start = start_time
        t1_end = time_add(t1_start, per_subject_block)
        t2_start = t1_end
        t2_end = time_add(t2_start, per_subject_block)
