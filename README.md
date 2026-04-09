# Resume-parser 🚀

An AI-powered resume parsing engine built with **FastAPI + Groq (Llama-3.3-70b)**.  
Extracts structured JSON from PDF, DOCX, DOC, and TXT resumes with maximum accuracy.

---

## Project Structure

```
Resume-parser/
├── backend/
│   ├── main.py            ← FastAPI server + file upload endpoint
│   ├── parser_engine.py   ← Text extraction + Groq API logic
│   ├── requirements.txt   ← Python dependencies
│   └── .env               ← Your Groq API key (never commit this)
└── frontend/
    └── index.html         ← Full UI (served by FastAPI)
```

---

## Setup (one-time)

### 1. Get a Groq API Key (free)
1. Go to https://console.groq.com
2. Sign up → API Keys → Create Key
3. Copy the key

### 2. Set up the project

```bash
# Clone / download the project, then:
cd Resume-parser/backend

# Create Python virtual environment
python -m venv venv

# Activate it:
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Add your API key

Open `backend/.env` and replace the placeholder:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Run Locally

```bash
# Make sure you're in the backend/ folder with venv activated:
cd Resume-parser/backend
source venv/bin/activate       # or venv\Scripts\activate on Windows

# Load env and start the server:
uvicorn main:app --reload --port 8000
```

Then open your browser at:
```
http://localhost:8000
```

---

## API Endpoints

| Method | Path     | Description                        |
|--------|----------|------------------------------------|
| GET    | /        | Serves the frontend UI             |
| POST   | /parse   | Upload a resume file → returns JSON|
| GET    | /health  | Check server + Groq key status     |

### Test via curl

```bash
curl -X POST http://localhost:8000/parse \
  -F "file=@/path/to/your/resume.pdf" | python -m json.tool
```

---

## What Gets Extracted

| Section              | Details                                          |
|----------------------|--------------------------------------------------|
| Personal Info        | Name, email, phone, location, LinkedIn, GitHub   |
| Professional Summary | Full summary paragraph                           |
| Work Experience      | Company, title, dates, responsibilities, achievements |
| Education            | Institution, degree, GPA, honors, courses        |
| Skills               | Technical, frameworks, tools, databases, cloud   |
| Certifications       | Name, issuer, date, credential ID                |
| Projects             | Name, description, technologies, URL            |
| Awards               | Title, issuer, date                              |
| Languages Spoken     | Language + proficiency level                     |
| Metadata             | Seniority level, total experience, resume score  |

---

## Suggested Future Features

1. **Batch Processing** — Upload a ZIP of multiple resumes, download all parsed JSONs
2. **ATS Score & Job Match** — Paste a JD and get a match % against the parsed resume  
3. **Resume Gap Detector** — Flag career gaps, missing sections, or weak bullet points
4. **Candidate Search / DB** — Store parsed resumes in PostgreSQL + full-text search
5. **Export to Google Sheets** — One-click export of multiple candidates into a spreadsheet
6. **LinkedIn Profile Import** — Parse directly from a LinkedIn public profile URL
7. **Resume Rewriter** — AI-powered bullet point improver (quantify achievements)
8. **OCR Support** — Handle scanned PDF resumes via Tesseract / AWS Textract
9. **Webhook / API Mode** — Integrate into your own ATS pipeline via REST webhook
10. **Duplicate Candidate Detection** — Fuzzy-match to flag the same person re-applying
