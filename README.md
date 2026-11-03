# KodeKawan - Chatbot Tutor Pemrograman AI

Final Project: chatbot berbasis LLM (Google Gemini API) untuk membantu mahasiswa Informatika belajar pemrograman.

## Use case
Education bot - tutor pemrograman.

## Parameter kreatif
- **Gaya bahasa**: santai / formal (mengubah system prompt)
- **Domain pengetahuan**: Python, Web, Basis Data, Algoritma
- **Memory**: mengingat info pengguna (nama, level) di `memory.json`
- **Rekomendasi**: setiap jawaban ditutup dengan topik "Lanjut belajar"

## Menjalankan
```bash
pip install -r requirements.txt
cp .env.example .env   # isi GEMINI_API_KEY
python app.py          # buka http://127.0.0.1:5000
```

## Screenshot
Lihat folder `screenshots/`.
