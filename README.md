# 🩺 ReportSathi

**ReportSathi** is an AI agent that reads your medical reports (PDF or photo) and explains them in plain, everyday language — so you actually understand what your report says before you see the doctor.

🔗 **Live app:** https://reportsathi-89d227bu8bqpz6mpsayefm.streamlit.app/

---

## ✨ Features

- **📄 Upload any report** — PDF or a photo of a printed report (lab tests, ultrasounds, ECGs, etc.)
- **🌐 Multi-language explanations** — get your report explained in **English, Hindi, or Bengali**
- **🗣️ Voice input & output** — ask questions by speaking, and listen to your explanation read aloud
- **🔍 Every value & finding, explained** — normal and abnormal lab values, and imaging/pathology findings, each with a short, plain-language note (not just numbers restated)
- **⚠️ Urgency flagging** — the app flags whether a report needs urgent attention, a doctor visit soon, routine follow-up, or is all-normal, based on the report's own printed ranges and wording
- **💬 Ask a question** — a Q&A chat that answers strictly from the facts in *your* report, so it never invents information
- **🩺 Doctor-visit summary (PDF)** — a downloadable summary with key points and suggested questions to ask your doctor
- **📈 Health Timeline** — tracks lab values across multiple reports over time and flags slow drift toward abnormal ranges, even before a single report crosses the line
- **🔐 Secure login** — sign up with email/password or continue with Google Sign-In

---

## 🧠 How it works

1. **Extraction** — the report is parsed to pull out structured lab values, printed reference ranges, and narrative findings (for imaging/pathology reports).
2. **Flagging** — each value is checked against its own report's printed range to decide normal/low/high, and how far outside the range it is.
3. **Urgency scoring** — the report's own wording and the flagged values decide an overall urgency level.
4. **Explanation** — an LLM turns the facts into a warm, simple, Class-8-reading-level explanation — no jargon, no invented information, grounded strictly in the extracted facts.
5. **Q&A** — follow-up questions are answered using only the same extracted facts.
6. **Trend tracking** — repeat tests are matched across a user's saved reports to chart trends and flag slow drift over time.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Auth:** [Authlib](https://authlib.org/) (Google OAuth) + bcrypt (email/password hashing)
- **AI / LLM:** Google Gemini (`google-genai`) — structured extraction, plain-language explanation, and grounded Q&A
- **Voice (STT/TTS):** [Sarvam AI](https://www.sarvam.ai/) — speech-to-text and text-to-speech tuned for Indian languages (Hindi, Bengali)
- **PDF generation:** ReportLab — for the doctor-visit summary PDF
- **Data validation:** Pydantic — structured, schema-validated LLM outputs
- **Data & trends:** pandas, numpy — Health Timeline drift analysis
- **Database:** SQLite

---

## 📌 Disclaimer

ReportSathi explains medical reports in simple language. It does **not** diagnose or prescribe. Always discuss your results with a qualified doctor.

---

## 👤 Author

Built by **Nitin Sharma**.
