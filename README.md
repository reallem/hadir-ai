# حضّر | Hadir

AI-powered career assistant that helps users identify skill gaps, prepare for interviews, and track their career progress through intelligent AI analysis and voice-based interview simulation.

---

## Overview

Hadir is an intelligent career preparation platform designed to support users from the job-search stage all the way to interview readiness.

The platform analyzes user skills, detects improvement areas, generates personalized growth plans, recommends learning resources, and simulates realistic interviews using AI-powered voice analysis.

---

## Features

- Skill gap detection based on user profile and interview history
- Personalized 14-day growth plans
- AI-generated interview questions
- Voice-based interview simulator
- Speech-to-text transcription using Whisper
- AI answer evaluation and feedback
- Progress tracking dashboard
- Personalized learning resource recommendations
- Arabic language support
- Text and voice interaction support

---

## Tech Stack

- Python
- Streamlit
- Groq API
- LLMs
- Whisper
- Plotly
- JSON-based local memory system

---

## How It Works

1. User enters career profile information
2. The system analyzes skills and weaknesses
3. Personalized learning plans and resources are generated
4. AI generates interview questions
5. User answers using voice or text
6. The system analyzes responses and provides feedback
7. Progress is tracked across sessions

---

## Project Structure

```bash
project/
│
├── app.py
├── style.css
├── user_memory.json
├── requirements.txt
├── logo_hadir_alternative.png
└── README.md
---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/hadir-ai.git

cd hadir-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Run the project:

```bash
streamlit run app.py
```

---

## Future Improvements

- User authentication and login system
- Individual user accounts and secure profile management
- Cloud database integration
- Resume analysis
- Real-time AI interview scoring
- Multi-language support
- Mobile-friendly version
