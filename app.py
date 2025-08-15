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