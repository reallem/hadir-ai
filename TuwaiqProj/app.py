import streamlit as st
import json
import os
import re
import tempfile
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from duckduckgo_search import DDGS
import plotly.graph_objects as go

load_dotenv()

MEMORY_FILE = "user_memory.json"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

st.set_page_config(
    page_title="حضّر",
    layout="wide"
)

def load_css():
    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            

load_css()

lang_col, empty_col = st.columns([1, 5])

with lang_col:
    language = st.selectbox(
        "🌐",
        ["العربية", "English"],
        index=0,
        label_visibility="collapsed"
    )

TEXT = {
    "العربية": {
        "title": "حضّر",
        "subtitle": "مدرب مهني ذكي يبدأ معك من مرحلة البحث عن وظيفة، ويحلل مهاراتك، ويكشف نقاط النقص، ويحاكي المقابلات، ويطوّر جاهزيتك المهنية",
        "username": "اسم المستخدم",
        "major": "التخصص",
        "target_job": "الوظيفة المستهدفة",
        "target_job_placeholder": "مثال: Data Analyst",
        "experience": "مستوى الخبرة",
        "skills": "مهاراتك الحالية",
        "skills_placeholder": "Python, SQL, Excel...",
        "english_level": "مستوى اللغة الإنجليزية",
        "weak_area": "أكثر شيء تحس أنه يضعفك",
        "weak_area_placeholder": "التوتر، الإنجليزية، الإجابات التقنية...",
        "complete_profile": "كمّل بيانات الملف المهني أولاً عشان يبدأ المحاكي يعطي نتائج دقيقة.",
        "tab_gaps": "فجوات المهارات",
        "tab_plan": "خطة التطوير",
        "tab_sources": "المصادر",
        "tab_interview": "محاكي المقابلة",
        "tab_dashboard": "لوحة التقدم",
        "skill_gap_title": "تحليل فجوات المهارات",
        "detect_gaps": "حلّل فجوات مهاراتي",
        "growth_plan_title": "خطة تطوير شخصية",
        "generate_plan": "أنشئ خطة تطوير 14 يوم",
        "sources_title": "مصادر مخصصة",
        "find_sources": "ابحث عن مصادر لمهاراتي",
        "why_sources": "لماذا هذه المصادر مناسبة لك؟",
        "interview_title": "محاكي المقابلة الصوتية",
        "generate_question": "أنشئ سؤال مقابلة",
        "current_question": "السؤال الحالي",
        "record_answer": "سجل إجابتك هنا",
        "upload_audio": "أو ارفع ملف صوت",
        "validate_answer": "قيّم إجابتي",
        "generate_first": "أنشئ سؤال مقابلة أولاً.",
        "verified_transcript": "النص بعد التحقق",
        "raw_transcript": "النص الخام",
        "feedback": "تقييم الإجابة",
        "voice_feedback": "التقييم الصوتي",
        "dashboard": "لوحة التقدم",
        "history": "سجل الجلسات",
        "no_sessions": "لا توجد جلسات مقابلة بعد.",
        "question": "السؤال",
        "answer_score": "درجة الإجابة",
        "confidence_score": "درجة الثقة",
        "view_feedback": "عرض النص والتقييم",
        "open_source": "افتح المصدر",
        "no_sources": "لا توجد مصادر متاحة حاليًا.",
        "spinner_gaps": "جاري تحليل فجوات المهارات...",
        "spinner_plan": "جاري إنشاء الخطة...",
        "spinner_sources": "جاري البحث عن المصادر...",
        "spinner_interview": "جاري تحويل الصوت والتحقق والتقييم..."
    },
    "English": {
        "title": "Hadir",
        "subtitle": "AI Career Coach from job search to interview readiness: profile memory, skill gap detection, voice interview simulation, answer validation, and personalized learning sources.",
        "username": "Username",
        "major": "Major",
        "target_job": "Target Job",
        "target_job_placeholder": "Example: Data Analyst",
        "experience": "Experience Level",
        "skills": "Current Skills",
        "skills_placeholder": "Python, SQL, Excel...",
        "english_level": "English Level",
        "weak_area": "Main Weak Area",
        "weak_area_placeholder": "Stress, English, technical answers...",
        "complete_profile": "Complete your career profile first to generate accurate results.",
        "tab_gaps": "Skill Gaps",
        "tab_plan": "Growth Plan",
        "tab_sources": "Sources",
        "tab_interview": "Interview Simulator",
        "tab_dashboard": "Dashboard",
        "skill_gap_title": "Skill Gap Detector",
        "detect_gaps": "Detect My Skill Gaps",
        "growth_plan_title": "Personalized Growth Plan",
        "generate_plan": "Generate 14-Day Growth Plan",
        "sources_title": "Personalized Sources",
        "find_sources": "Find Sources For My Skills",
        "why_sources": "Why these sources fit you",
        "interview_title": "Voice Interview Simulator",
        "generate_question": "Generate Interview Question",
        "current_question": "Current Question",
        "record_answer": "Record your answer here",
        "upload_audio": "Or upload an audio file",
        "validate_answer": "Validate My Answer",
        "generate_first": "Generate an interview question first.",
        "verified_transcript": "Verified Transcript",
        "raw_transcript": "Raw Transcript",
        "feedback": "Validation Feedback",
        "voice_feedback": "Coach Voice Feedback",
        "dashboard": "Progress Dashboard",
        "history": "Session History",
        "no_sessions": "No interview sessions yet.",
        "question": "Question",
        "answer_score": "Answer Score",
        "confidence_score": "Confidence Score",
        "view_feedback": "View Transcript + Feedback",
        "open_source": "Open Source",
        "no_sources": "No sources available.",
        "spinner_gaps": "Detecting skill gaps...",
        "spinner_plan": "Building your plan...",
        "spinner_sources": "Searching for sources...",
        "spinner_interview": "Transcribing, verifying, and validating answer..."
    }
}

t = TEXT[language]

def clean_model_text(text):
    if not text:
        return ""

    text = re.sub(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+', '', text)
    text = re.sub(r'[^\u0600-\u06FFa-zA-Z0-9\s\.\,\:\;\-\_\(\)\/%؟!،\n]+', '', text)

    return text.strip()

def render_ai_text(text):
    text = clean_model_text(text)
    text = text.replace("\n", "<br>")
    st.markdown(
        f"""
        <div style="
            line-height: 2.1;
            font-size: 16px;
            direction: rtl;
            text-align: right;
            white-space: normal;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

def reset_section_memory(username, keys):
    for key in keys:
        if key in memory.get(username, {}):
            del memory[username][key]
    save_memory(memory)

def extract_score(text, default=60):
    match = re.search(r"(\d{1,3})\s*/\s*100", text)
    if match:
        return min(int(match.group(1)), 100)

    match = re.search(r"(\d{1,3})", text)
    if match:
        return min(int(match.group(1)), 100)

    return default

def chat_agent(prompt, system="You are a helpful career interview coach."):
    if not client:
        return "API key is missing. Please add GROQ_API_KEY in .env file."

    strict_system = system + """

Mandatory output rules:
- Respond in Arabic only.
- Do not use any language other than Arabic in the final answer.
- Do not use Chinese, Japanese, Korean, or random symbols.
- English is allowed only for common technical terms such as Python, SQL, Excel, API, GitHub, LinkedIn.
- Keep the tone professional, clear, and practical.
- Do not switch languages inside the response.
- If the user input contains English, understand it but answer in Arabic.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": strict_system},
            {"role": "user", "content": prompt}
        ]
    )

    return clean_model_text(response.choices[0].message.content)

def transcribe_audio(audio_file):
    if not client:
        return "API key is missing."

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as file:
            transcript = client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3",
                language="ar",
                response_format="text",
                temperature=0
            )
    finally:
        os.remove(tmp_path)

    return transcript

def verify_transcript(question, transcript, profile):
    prompt = f"""
You are a transcript verification agent for Arabic interview answers.

Interview question:
{question}

Raw speech transcript:
{transcript}

User profile:
{profile}

Task:
Verify whether the transcript makes sense in the context of the question.
Fix likely speech-to-text mistakes ONLY when the correction is obvious from context.

Strict rules:
- Final output must be Arabic only.
- Return only the verified transcript. No explanation.
- Do not invent new information.
- Do not add skills, experience, or examples the user did not say.
- Do not change the user's meaning.
- If a word sounds wrong but a close Arabic word makes sense in context, correct it.
- Example: if the transcript says "الحذف عن مصادر" but the context suggests "البحث عن مصادر", correct it to "البحث عن مصادر".
- If the transcript is too unclear to evaluate, write exactly: النص غير واضح ويحتاج إعادة تسجيل.
"""

    return chat_agent(
        prompt,
        "You verify Arabic speech transcripts before interview evaluation."
    )

def text_to_speech(text, filename="coach_voice.wav"):
    if not client:
        st.error("Groq API key is missing.")
        return None

    try:
        response = client.audio.speech.create(
            model="canopylabs/orpheus-arabic-saudi",
            voice="fahad",
            input=text[:900],
            response_format="wav"
        )
        response.write_to_file(filename)
        return filename

    except Exception as e:
        st.error(f"TTS failed: {e}")
        return None

def generate_interview_question(profile, history):
    prompt = f"""
You are a professional Saudi job interviewer.

User profile:
{profile}

Previous interview history:
{history[-5:]}

Task:
Write only ONE realistic interview question.
Do not explain.
Do not write more than one question.

Choose the question based on:
- Target job
- Major
- Skills
- Previous weaknesses
- Experience level

Final output:
- Arabic only.
- Saudi-friendly professional Arabic.
"""

    return chat_agent(
        prompt,
        "You are a Saudi Arabic interviewer. Ask one realistic interview question only."
    )

def validate_answer(question, transcript, profile, history):
    prompt = f"""
You are a strict interview answer validation agent.

Interview question:
{question}

Verified user answer transcript:
{transcript}

User profile:
{profile}

Previous history:
{history[-5:]}

Evaluate ONLY the verified transcript above.

Important evaluation rules:
- Do not reinterpret words incorrectly.
- Do not assume the user said "حذف" if the verified transcript says "بحث".
- Do not invent details not mentioned by the user.
- If the answer is unclear, say it is unclear instead of inventing meaning.
- Evaluate relevance to the question directly.
- Arabic only.

Return a structured result in Arabic only:

1. هل الإجابة جاوبت على السؤال؟ Correct / Needs Improvement / Weak
2. تقييم الإجابة من 100
3. مستوى الثقة التقريبي من 100
4. نقاط القوة
5. نقاط الضعف
6. هل يوجد كلام غير واضح أو يحتاج تعديل؟
7. نسخة محسنة من الإجابة بأسلوب مقابلات بدون إضافة خبرات غير مذكورة
8. السؤال التالي المقترح بناءً على ضعف المستخدم
9. نصيحة قصيرة قبل الإجابة القادمة

Do not diagnose psychologically. Focus only on career training, confidence, and communication.
"""

    return chat_agent(
        prompt,
        "You are a strict interview evaluator. Evaluate only what the user actually said."
    )

def detect_skill_gaps(profile, history):
    prompt = f"""
You are a Career Growth Agent.

User profile:
{profile}

Previous sessions:
{history[-5:]}

Return the result in Arabic only.

Use this exact format. Each field must be on a separate line.

المهارات التي تحتاج تطوير:

1. المهارة:
السبب:
مستوى الفجوة:
طريقة التطوير:
مهمة تدريبية:
مدة التحسن:

---

2. المهارة:
السبب:
مستوى الفجوة:
طريقة التطوير:
مهمة تدريبية:
مدة التحسن:

---

3. المهارة:
السبب:
مستوى الفجوة:
طريقة التطوير:
مهمة تدريبية:
مدة التحسن:

Rules:
- Arabic only.
- Do not write everything in one paragraph.
- Each field must be on a separate line.
- No table.
- Maximum 3 skills only.
"""

    return chat_agent(
        prompt,
        "You identify career skill gaps and create practical improvement plans."
    )

def generate_growth_plan(profile, history):
    prompt = f"""
Create a 14-day career development plan.

User profile:
{profile}

Previous history:
{history[-5:]}

Return in Arabic only.

Use this exact format. Each day must be on a separate line.

خطة تطوير لمدة 14 يوم:

- اليوم 1:
- اليوم 2:
- اليوم 3:
- اليوم 4:
- اليوم 5:
- اليوم 6:
- اليوم 7:
- اليوم 8:
- اليوم 9:
- اليوم 10:
- اليوم 11:
- اليوم 12:
- اليوم 13:
- اليوم 14:

Rules:
- Arabic only.
- Each day must be on a separate line.
- Keep each day short and clear.
- Do not write all days in one paragraph.
- No table.
"""

    return chat_agent(
        prompt,
        "You create personalized career preparation roadmaps."
    )

def search_sources(target_job, skills, level):
    query = (
        f"{target_job} {skills} interview preparation learning resources "
        f"site:coursera.org OR site:freecodecamp.org OR site:learn.microsoft.com OR site:roadmap.sh"
    )

    results = []

    trusted_domains = [
        "coursera.org",
        "freecodecamp.org",
        "learn.microsoft.com",
        "roadmap.sh",
        "kaggle.com",
        "w3schools.com",
        "geeksforgeeks.org"
    ]

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=10):
                url = r.get("href", "")
                title = r.get("title", "")
                snippet = r.get("body", "")

                if not url:
                    continue

                if not any(domain in url for domain in trusted_domains):
                    continue

                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet
                })

                if len(results) >= 4:
                    break

    except Exception:
        pass

    if not results:
        results = [
            {
                "title": "freeCodeCamp",
                "url": "https://www.freecodecamp.org",
                "snippet": "مصدر عملي لتعلم البرمجة وتحليل البيانات من خلال مشاريع وتمارين."
            },
            {
                "title": "Microsoft Learn",
                "url": "https://learn.microsoft.com",
                "snippet": "مسارات تعليمية منظمة للمهارات التقنية والمهنية."
            },
            {
                "title": "roadmap.sh",
                "url": "https://roadmap.sh",
                "snippet": "خرائط طريق واضحة لتطوير المهارات التقنية حسب المجال."
            },
            {
                "title": "Kaggle Learn",
                "url": "https://www.kaggle.com/learn",
                "snippet": "تمارين عملية مناسبة لتحليل البيانات وتعلم Python و SQL."
            }
        ]

    return results

def render_sources(sources):
    if not sources:
        st.warning("لا توجد مصادر متاحة حاليًا.")
        return

    shown_urls = set()

    for source in sources:
        title = source.get("title") or "Source"
        url = source.get("url") or ""
        snippet = source.get("snippet") or "No description available."

        if not url or url in shown_urls:
            continue

        shown_urls.add(url)

        with st.container():
            st.markdown(f"### 🔗 [{title}]({url})")
            st.write(snippet)
            st.link_button("افتح المصدر", url)
            st.divider()

def justify_sources(sources, profile):
    sources_text = "\n".join(
        [f"- {s.get('title', 'Source')} | {s.get('url', '')} | {s.get('snippet', '')}" for s in sources]
    )

    prompt = f"""
You are a learning resource recommendation agent.

User profile:
{profile}

Sources:
{sources_text}

Explain in Arabic only:
- Why these sources are useful for this user.
- Which skill they help improve.
- How to use them during one week.

Rules:
- Arabic only.
- Keep it short.
- Do not repeat the same source more than once.
- Do not write long numbered lists.
"""

    return chat_agent(
        prompt,
        "You recommend learning resources based on user profile and skill gaps."
    )

def make_progress_chart(history):
    dates = []
    answer_scores = []
    confidence_scores = []

    for item in history:
        if "answer_score" in item:
            dates.append(item.get("date", "Session"))
            answer_scores.append(item.get("answer_score", 0))
            confidence_scores.append(item.get("confidence_score", 0))

    if not dates:
        dates = ["Session 1", "Session 2", "Session 3"]
        answer_scores = [45, 60, 72]
        confidence_scores = [40, 55, 68]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=answer_scores,
        mode="lines+markers",
        name="Answer Quality"
    ))
    fig.add_trace(go.Scatter(
        x=dates,
        y=confidence_scores,
        mode="lines+markers",
        name="Confidence"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=360,
        yaxis=dict(range=[0, 100]),
        title="Interview Progress"
    )

    return fig

def get_profile_dict(name, major, target_job, experience, skills, english_level, weak_area):
    return {
        "name": name,
        "major": major,
        "target_job": target_job,
        "experience": experience,
        "skills": skills,
        "english_level": english_level,
        "weak_area": weak_area
    }

st.markdown(f"""
<div class="hero">
    <h1 style="text-align:right; direction:rtl; margin-bottom:20px;">
        {t["title"]}
    </h1>
     <h4 style="text-align:right; direction:rtl; margin-bottom:20px;">
    <p>{t["subtitle"]}</p>
     </h4>
</div>
""", unsafe_allow_html=True)

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing. Add it inside .env file.")

memory = load_memory()

col_left, col_center, col_right = st.columns([1, 1.35, 1])

with col_center:
    st.markdown('<div class="card profile-card">', unsafe_allow_html=True)
username = st.text_input(t["username"])

major = st.selectbox(
    t["major"],
    [
        "Computer Science",
        "Software Engineering",
        "Information Technology",
        "Information Systems",
        "Cybersecurity",
        "Data Science",
        "Artificial Intelligence",
        "Computer Engineering",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Industrial Engineering",
        "Architecture",
        "Business Administration",
        "Marketing",
        "Finance",
        "Accounting",
        "Economics",
        "Human Resources",
        "Supply Chain Management",
        "Law",
        "Medicine",
        "Nursing",
        "Pharmacy",
        "Dentistry",
        "Psychology",
        "Education",
        "English Language",
        "Translation",
        "Media & Communication",
        "Graphic Design",
        "Interior Design",
        "Mathematics",
        "Statistics",
        "Physics",
        "Chemistry",
        "Biology",
        "Other"
    ]
)

target_job = st.text_input(t["target_job"], placeholder=t["target_job_placeholder"])
experience = st.selectbox(t["experience"], ["Beginner", "Intermediate", "Advanced"])
skills = st.text_area(t["skills"], placeholder=t["skills_placeholder"])
english_level = st.selectbox(t["english_level"], ["ضعيف", "متوسط", "جيد", "ممتاز"] if language == "العربية" else ["Weak", "Average", "Good", "Excellent"])
weak_area = st.text_input(t["weak_area"], placeholder=t["weak_area_placeholder"])

profile_complete = all([
    username.strip(),
    target_job.strip(),
    skills.strip(),
    weak_area.strip()
])

if username and not profile_complete:
    st.warning("كمّل بيانات الملف المهني أولاً عشان يبدأ المحاكي يعطي نتائج دقيقة.")

if profile_complete:
    if username not in memory:
        memory[username] = {
            "profile": {},
            "sessions": [],
            "feedback": []
        }
        save_memory(memory)

    profile = get_profile_dict(
        username,
        major,
        target_job,
        experience,
        skills,
        english_level,
        weak_area
    )

    old_profile = memory[username].get("profile", {})
    if old_profile != profile:
        reset_section_memory(
            username,
            [
                "last_question",
                "last_skill_gaps",
                "last_growth_plan",
                "last_sources",
                "last_sources_explanation"
            ]
        )

    memory[username]["profile"] = profile
    history = memory[username]["sessions"]
    save_memory(memory)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t["tab_gaps"],
    t["tab_plan"],
    t["tab_sources"],
    t["tab_interview"],
    t["tab_dashboard"]
])
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(t["skill_gap_title"])

        if st.button(t["detect_gaps"]):
            with st.spinner(t["spinner_gaps"]):
                gaps = detect_skill_gaps(profile, history)
                memory[username]["last_skill_gaps"] = gaps
                save_memory(memory)

        if memory[username].get("last_skill_gaps"):
            render_ai_text(memory[username]["last_skill_gaps"])

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(t["growth_plan_title"])

        if st.button(t["generate_plan"]):
            with st.spinner(t["spinner_plan"]):
                plan = generate_growth_plan(profile, history)
                memory[username]["last_growth_plan"] = plan
                save_memory(memory)

        if memory[username].get("last_growth_plan"):
            render_ai_text(memory[username]["last_growth_plan"])

        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(t["sources_title"])

        if st.button(t["find_sources"]):
            with st.spinner(t["spinner_sources"]):
                sources = search_sources(target_job, skills, experience)
                explanation = justify_sources(sources, profile)

                memory[username]["last_sources"] = sources
                memory[username]["last_sources_explanation"] = explanation
                save_memory(memory)

        if memory[username].get("last_sources"):
            render_sources(memory[username]["last_sources"])

        if memory[username].get("last_sources_explanation"):
            st.subheader(t["why_sources"])
            render_ai_text(memory[username]["last_sources_explanation"])

        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(t["interview_title"])

        if st.button(t["generate_question"], disabled=not profile_complete):
            question = generate_interview_question(profile, history)
            memory[username]["last_question"] = question
            save_memory(memory)

            voice_path = text_to_speech(question, "interviewer_question.wav")
            if voice_path:
                st.audio(voice_path)

        current_question = memory[username].get("last_question", "")

        if current_question:
            st.info(f'{t["current_question"]}: {current_question}')

        audio = st.audio_input(t["record_answer"])
        uploaded_audio = st.file_uploader(
            t["upload_audio"],
            type=["wav", "mp3", "m4a", "ogg", "webm"]
        )

        audio_source = audio if audio else uploaded_audio

        if audio_source and st.button(t["validate_answer"]):
            if not current_question:
                st.warning(t["generate_first"])
            else:
                with st.spinner(t["spinner_interview"]):
                    raw_transcript = transcribe_audio(audio_source)

                    verified_transcript = verify_transcript(
                        current_question,
                        raw_transcript,
                        profile
                    )

                    validation = validate_answer(
                        current_question,
                        verified_transcript,
                        profile,
                        history
                    )

                    answer_score = extract_score(validation, 60)
                    confidence_score = extract_score(validation, 55)

                    session = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "question": current_question,
                        "raw_transcript": raw_transcript,
                        "transcript": verified_transcript,
                        "validation": validation,
                        "answer_score": answer_score,
                        "confidence_score": confidence_score
                    }

                    memory[username]["sessions"].append(session)
                    save_memory(memory)

                    voice_feedback = text_to_speech(validation[:800], "coach_feedback.wav")

                st.subheader(t["verified_transcript"])
                render_ai_text(verified_transcript)

                with st.expander(t["raw_transcript"]):
                    st.write(raw_transcript)

                st.subheader(t["feedback"])
                render_ai_text(validation)

                if voice_feedback:
                    st.subheader(t["voice_feedback"])
                    st.audio(voice_feedback)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(t["dashboard"])
        st.plotly_chart(make_progress_chart(history), use_container_width=True)

        st.subheader(t["history"])
        if history:
            for item in history[-5:]:
                st.write(f"**{item.get('date')}**")
                st.write(f'{t["question"]}:', item.get("question"))
                st.write(f'{t["answer_score"]}:', item.get("answer_score"))
                st.write(f'{t["confidence_score"]}:', item.get("confidence_score"))

                with st.expander(t["view_feedback"]):
                    st.write(f'{t["verified_transcript"]}:')
                    render_ai_text(item.get("transcript"))
                    if item.get("raw_transcript"):
                        st.write(f'{t["raw_transcript"]}:')
                        st.write(item.get("raw_transcript"))
                    st.write(f'{t["feedback"]}:')
                    render_ai_text(item.get("validation", ""))

                st.divider()
        else:
            st.write(t["no_sessions"])

        st.markdown('</div>', unsafe_allow_html=True)
st.markdown("""
<hr style="margin-top:40px;">

<div style="
text-align:center;
padding:20px;
font-size:15px;
color:#cbd5e1;
line-height:2;
">

<b>Developed By</b><br>

Sadeem Alzahrani &nbsp; | &nbsp;
Sara Albader &nbsp; | &nbsp;
Sarah Almubarak

</div>
""", unsafe_allow_html=True)