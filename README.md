
# 🎓 LectureLens — AI-Powered Lecture Summariser & Quiz Generator

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat)

> Transform any YouTube lecture into structured summaries and interactive quizzes — powered by Groq API and LLaMA 3.3.

---

## 📌 Table of Contents

- [What This System Does](#-what-this-system-does)
- [System Architecture](#️-system-architecture)
- [Repository Structure](#️-repository-structure)
- [Setup Instructions](#️-setup-instructions)
- [Running the Application](#-running-the-application)
- [How It Works](#-how-it-works)
- [Dashboard Features](#️-dashboard-features)
- [Tech Stack](#️-tech-stack)
- [Known Limitations](#️-known-limitations)
- [Future Improvements](#️-future-improvements)
- [Dataset](#-supported-youtube-videos)
- [Demo Video](#-demo-video)

---

## 🎯 What This System Does

| # | Stage | Description |
|---|-------|-------------|
| 1 | 🔗 **URL Input** | User pastes any YouTube lecture URL to begin |
| 2 | 📄 **Transcript Fetching** | `youtube-transcript-api` automatically fetches the video transcript |
| 3 | 🤖 **AI Summarisation** | Groq LLM (LLaMA 3.3-70B) generates structured summary with bullet points and key takeaways |
| 4 | 🧠 **Quiz Generation** | Same LLM auto-generates 10 MCQs with options A–D, correct answer, and explanation |
| 5 | ✅ **Interactive Quiz** | User submits answers, gets scored (Pass / Average / Fail), can retry anytime |
| 6 | 💾 **Persistent Storage** | All lectures, summaries, and quizzes saved to SQLite database automatically |
| 7 | 📋 **History Log** | All past lectures stored with read-only quiz answer keys for review |

---

## 🏗️ System Architecture

```text
User pastes YouTube URL
        │
        ▼
youtube-transcript-api  →  fetches transcript
        │
        ▼
Groq API (LLaMA 3.3-70B)
        │
        ├──►  Generate structured summary (bullet points + key takeaways)
        │
        └──►  Generate 10 MCQs (question + 4 options + answer + explanation)
                │
                ▼
        SQLite Database  →  lecturelens.db
                │
                ▼
        Streamlit UI
        ├──►  Live Monitor Tab  →  Summary + Interactive Quiz
        └──►  History Log Tab  →  Past lectures + Answer Keys
```

---

## 🗂️ Repository Structure

```
LectureLens/
│
├── README.md                  # Project documentation
├── app.py                     # Main Streamlit application (UI + logic)
├── summariser.py              # Transcript fetching + Groq AI summarisation & quiz generation
├── database.py                # SQLite database init, save, and retrieval functions
├── requirements.txt           # All dependencies pinned
├── Dockerfile                 # Docker deployment configuration
├── .env                       # API keys (not committed)
└── .gitignore                 # Files excluded from version control
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/umberqasim/LectureLens.git
cd LectureLens
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```
> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

Get a free API key at [console.groq.com](https://console.groq.com).

### 5. Initialise the Database
```bash
python database.py
```
This creates `lecturelens.db` locally with the required `history` table.

---

## 🚀 Running the Application

```bash
streamlit run app.py
```

Open your browser at: `http://localhost:8501`

---

## 🧠 How It Works

**Policy Parsing Equivalent — Transcript Extraction:**

The system automatically fetches transcripts — no manual input required.

1. **Transcript Fetching** — `youtube-transcript-api` extracts full transcript from the YouTube video
2. **AI Summarisation** — Transcript sent to Groq's `llama-3.3-70b-versatile` model with a structured prompt
3. **Quiz Generation** — Same LLM generates 10 MCQs with options, correct answer, and explanation
4. **Caching** — All results saved to SQLite — no re-processing needed for past lectures
5. **History** — Every session stored with timestamp for future review

**Why Groq/LLaMA?**
Ultra-fast inference, free tier available, and LLaMA 3.3-70B produces high-quality structured output — ideal for both summarisation and quiz generation tasks.

---

## 🖥️ Dashboard Features

### Live Monitor Tab
- YouTube URL input field
- AI-generated structured summary with bullet points
- 10 interactive MCQs with A–D options
- Submit answers → scored instantly (Pass / Average / Fail)
- Retry quiz anytime

### History Log Tab
- Complete list of all previously processed lectures
- Read-only quiz answer keys for review
- Persistent across sessions via SQLite

---

## 🛠️ Tech Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| Frontend / UI | Streamlit | Custom CSS, Google Fonts, dark theme |
| AI / LLM | Groq API · LLaMA 3.3-70B | Ultra-fast inference, free tier |
| Transcript | youtube-transcript-api | Auto + manual captions supported |
| Backend | Python 3.10+ | Core logic in `summariser.py` |
| Database | SQLite3 | Via `database.py` — persistent local storage |
| Deployment | Docker + Streamlit Cloud | `Dockerfile` included |
| Environment | python-dotenv | `.env` based API key management |

---

## 🗃️ Database Schema

```sql
CREATE TABLE history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT NOT NULL,
    summary     TEXT NOT NULL,
    quiz        TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

All lecture summaries and quizzes are saved automatically after generation and can be reviewed anytime from the **History Log** tab.

---

## ⚠️ Known Limitations

- Videos with captions disabled cannot be processed — transcript unavailable
- Groq free tier has rate limits — heavy usage may require retry logic
- Very long lectures may exceed LLM context window — chunking not yet implemented

---

## 🛣️ Future Improvements

- [ ] Export summary and quiz as PDF
- [ ] Support for multiple languages
- [ ] User authentication and personal history
- [ ] Upload local video/audio files
- [ ] Difficulty levels for quiz generation (Easy / Medium / Hard)
- [ ] Track quiz scores over time with performance analytics

---

## ✅ Supported YouTube Videos

| Type | Supported |
|---|---|
| Videos with original captions | ✅ Yes |
| Videos with auto-generated captions | ✅ Yes |
| Videos with auto-dubbed captions | ✅ Yes |
| Videos with captions disabled | ❌ No |

---

## 🔐 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com | ✅ Yes |

---

## 📹 Demo Video

[▶️ Watch Full System Demo](https://drive.google.com/file/d/1IuT4jeESBz0VSrcdYPnIJTkb-6f_N_xb/view?usp=sharing)

> The demo walkthrough covers:
> - Pasting a YouTube URL and fetching transcript
> - AI-generated summary with key takeaways
> - Interactive MCQ quiz with scoring
> - History Log with past lectures and answer keys

---

## 📦 Supported YouTube Videos

[**youtube-transcript-api**](https://pypi.org/project/youtube-transcript-api/) — PyPI  
Supports all YouTube videos with original or auto-generated captions enabled.

---

## 👩‍💻 Author

**Umber Qasim**

Software Engineering Student — Fatima Jinnah Women University, Rawalpindi

📧 umberqasim08@gmail.com

---

## 📄 License

This project is for educational purposes and was developed as part of the **NAVTTC Government-Certified AI Training Program** (Feb–May 2025).

---

> *"Don't just watch lectures — understand them."* 🎓
