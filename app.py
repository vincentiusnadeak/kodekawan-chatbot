"""KodeKawan - Chatbot tutor pemrograman berbasis LLM (Flask + Google Gemini API)."""
import json, os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import types

load_dotenv()
app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")
MEMORY_FILE = Path("memory.json")

# ---- Parameter kreatif -------------------------------------------------
STYLES = {
    "santai": "Gunakan bahasa Indonesia santai, akrab, seperti kakak tingkat yang sabar. Boleh pakai emoji secukupnya.",
    "formal": "Gunakan bahasa Indonesia baku, sopan, dan terstruktur seperti dosen pembimbing.",
}
DOMAINS = {
    "python": "Python", "web": "Pengembangan Web (HTML, CSS, JavaScript, PHP)",
    "database": "Basis Data (SQL, MySQL)", "algoritma": "Algoritma & Struktur Data",
}

def load_memory():
    return json.loads(MEMORY_FILE.read_text()) if MEMORY_FILE.exists() else {"facts": []}

def save_memory(m):
    MEMORY_FILE.write_text(json.dumps(m, ensure_ascii=False, indent=2))

def build_system_prompt(style, domain, memory_on):
    p = (
        "Kamu adalah KodeKawan, asisten belajar pemrograman untuk mahasiswa Informatika. "
        f"Fokus domain: {DOMAINS.get(domain, 'Python')}. {STYLES.get(style, STYLES['santai'])} "
        "Jelaskan konsep langkah demi langkah, beri contoh kode singkat dalam blok kode, "
        "lalu akhiri dengan 2 rekomendasi topik/latihan lanjutan dalam format daftar bertajuk 'Lanjut belajar:'. "
        "Tolak dengan sopan pertanyaan di luar topik pemrograman/belajar."
    )
    if memory_on:
        facts = load_memory()["facts"]
        if facts:
            p += "\nYang kamu ketahui tentang pengguna: " + "; ".join(facts)
    return p

def extract_fact(text):
    """Fitur memory sederhana: simpan info pengguna (nama/level) dari kalimat tertentu."""
    low = text.lower()
    for key in ("nama saya", "namaku", "saya sedang belajar", "aku lagi belajar", "saya mahasiswa"):
        if key in low:
            m = load_memory()
            if text not in m["facts"]:
                m["facts"].append(text[:200]); save_memory(m)
            return

@app.get("/")
def index():
    return render_template("index.html", domains=DOMAINS)

@app.post("/api/chat")
def chat():
    d = request.get_json()
    msgs = d.get("messages", [])
    style, domain, memory_on = d.get("style", "santai"), d.get("domain", "python"), d.get("memory", True)
    if memory_on and msgs:
        extract_fact(msgs[-1]["content"])
    try:
        contents = [
            types.Content(role="user" if m["role"] == "user" else "model",
                          parts=[types.Part(text=m["content"])])
            for m in msgs[-20:]
        ]
        r = client.models.generate_content(
            model=MODEL, contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=build_system_prompt(style, domain, memory_on),
                max_output_tokens=1000),
        )
        return jsonify({"reply": r.text})
    except Exception as e:
        return jsonify({"reply": f"Maaf, terjadi kesalahan: {e}"}), 500

@app.post("/api/reset")
def reset():
    save_memory({"facts": []})
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)
