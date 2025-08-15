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

def chunk_list(xs, n):
    return [xs[i:i+n] for i in range(0, len(xs), n)]


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
        
        schedule_plan.append({
            "day": d,
            "slots": [
                {"subject": s1, "start": t1_start, "end": t1_end},
                {"subject": s2, "start": t2_start, "end": t2_end},
            ]
        })

 
    prompt = f"Make a short study strategy for {days} days, subjects={subjects}, {hours_per_day}h/day, 2 subjects/day."
    summary = ai_complete(prompt)

    if request.form.get("download") == "1":
        buf = StringIO()
        buf.write(f"# Study Schedule ({days} days)\n\n")
        buf.write(f"- Hours/day: **{hours_per_day}** starting **{start_time}**\n")
        buf.write(f"- Subjects: {', '.join(subjects)}\n\n")
        
        for entry in schedule_plan:
            buf.write(f"## Day {entry['day']}\n")
            for s in entry["slots"]:
                buf.write(f"- **{s['subject']}**: {s['start']}–{s['end']}\n")
            buf.write("\n")
            
        buf.write("## Strategy\n")
        buf.write(summary + "\n")
        data = buf.getvalue().encode("utf-8")
        
        return send_file(
            io.BytesIO(data),
            as_attachment=True,
            download_name="study_schedule.txt",
            mimetype="text/plain"
        )

    return render_template("schedule.html", plan=schedule_plan, summary=summary,
                           hours=hours_per_day, days=days, start_time=start_time,
                           subjects_text=",".join(subjects))
    
@app.route("/chat", methods=["GET"])
def chat_page():
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json or {}
    
    question = data.get("message", "").strip()
    
    style = data.get("style", "simple")
    
    if not question:
        return jsonify({"reply": "ask a question"}), 400
    
    prompt = f"Explain in style={style}. Question: {question}"
    reply = ai_complete(prompt)
    return jsonify({"reply": reply})

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "GET":
        return render_template("quiz.html")
    
    topic = request.form.get("topic", "General")
    count = int(request.form.get("count", "5") or 5)
    level = request.form.get("level", "easy")
    
    if USE_GEMINI:
        prompt = f"Create {count} {level} MCQs on {topic}. Return as numbered list with options A–D and the correct answer per question."
        text = ai_complete(prompt)
        
    else:
        
        text = "\n".join([
            "1) What is 2+2?\nA) 3  B) 4  C) 5  D) 22\nAnswer: B",
            "2) Unit of force?\nA) Joule  B) Newton  C) Watt  D) Pascal\nAnswer: B",
            "3) H2O common name?\nA) Oxygen  B) Hydrogen  C) Water  D) Helium\nAnswer: C",
        ])
        
    return render_template("quiz.html", generated=text, topic=topic, count=count, level=level)

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)