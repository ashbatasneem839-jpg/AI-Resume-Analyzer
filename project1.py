
import streamlit as st
import pypdf
import io
import os
import json

from google import genai
from dotenv import load_dotenv
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
    override=True
)

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Resume & Career Analyzer",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. PURPLE THEME
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #100D1C;
    color: #FFFFFF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #191329;
    border-right: 1px solid #352653;
}

h1, h2, h3 {
    color: #FFFFFF !important;
}

p, label, .stMarkdown {
    color: #D8D2E8;
}

[data-testid="stMetric"] {
    background-color: #211A32;
    border: 1px solid #44315F;
    padding: 20px;
    border-radius: 14px;
}

[data-testid="stMetricValue"] {
    color: #C4A1FF;
}

.stButton > button {
    background-color: #8B5CF6;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #7C3AED;
    color: white;
}

.stTextInput input {
    background-color: #211A32;
    color: white;
    border: 1px solid #594276;
    border-radius: 8px;
}

[data-testid="stFileUploader"] {
    background-color: #211A32;
    border: 1px dashed #A78BFA;
    border-radius: 12px;
    padding: 15px;
}

.stProgress > div > div > div {
    background-color: #A78BFA;
}

hr {
    border-color: #44315F;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    override=True
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    st.success("Gemini API key loaded successfully!")
else:
    st.error("Gemini API key not found.")
    st.stop()
    
if not GEMINI_API_KEY:
    st.error("Gemini API key not loaded. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)


# ==========================================
# 4. SESSION STATE
# ==========================================

if "resume_data" not in st.session_state:
    st.session_state.resume_data = None


# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:
    st.title("💜 CareerAI")
    st.caption("AI Resume & Career Analyzer")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📄 Resume Analysis",
            "🎯 Skill Gap Analysis",
            "💼 Job Recommendations",
            "📚 Learning Roadmap"
        ]
    )

    st.divider()

    st.caption("Powered by Gemini AI")
    st.caption("Your career journey starts here.")


# ==========================================
# 6. HELPER FUNCTION: EXTRACT RESUME TEXT
# ==========================================

def extract_text_from_file(uploaded_file):

    file_type = uploaded_file.type

    if file_type == "application/pdf":
        pdf_reader = pypdf.PdfReader(
            io.BytesIO(uploaded_file.getvalue())
        )

        text = ""

        for pdf_page in pdf_reader.pages:
            text += (pdf_page.extract_text() or "") + "\n"

        return text

    elif file_type == "text/plain":
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")

    else:
        raise ValueError("Please upload a PDF or TXT file.")


# ==========================================
# 7. HELPER FUNCTION: DISPLAY CATEGORY SCORES
# ==========================================

def display_categories(resume_data):

    st.subheader("Category-wise Resume Ratings")

    for category in resume_data.get("categories", []):

        score = int(category.get("score", 0))
        score = max(0, min(score, 100))

        st.write(f"**{category.get('name', 'Category')}**")
        st.progress(score / 100)
        st.write(f"Score: {score}/100")
        st.caption(category.get("reason", ""))


# ==========================================
# 8. DASHBOARD PAGE
# ==========================================

if page == "🏠 Dashboard":

    st.title("💜 AI Resume & Career Analyzer")

    st.markdown(
        "### Welcome to your personal AI-powered career assistant"
    )

    st.caption(
        "Analyze your resume, discover skill gaps, "
        "and find suitable career opportunities."
    )

    st.divider()

    resume_data = st.session_state.resume_data

    col1, col2, col3, col4 = st.columns(4)

    if resume_data:

        with col1:
            st.metric(
                "📄 Resume Score",
                f"{resume_data.get('overall_score', 0)}/100"
            )

        with col2:
            st.metric(
                "🎯 Skills Analyzed",
                len(resume_data.get("skill_gap_analysis", []))
            )

        with col3:
            st.metric(
                "💼 Job Matches",
                len(resume_data.get("job_recommendations", []))
            )

        with col4:
            st.metric(
                "📚 Learning Tasks",
                len(resume_data.get("learning_roadmap", []))
            )

        st.divider()

        st.subheader("Resume Overview")

        st.write("**Resume Strengths**")

        for item in resume_data.get("strengths", []):
            st.write("✅", item)

        st.write("**Areas to Improve**")

        for item in resume_data.get("weaknesses", []):
            st.write("⚠️", item)

        st.info(
            "Use the sidebar to explore your detailed skill analysis, "
            "job recommendations, and learning roadmap."
        )

    else:

        with col1:
            st.metric("📄 Resume Analysis", "AI Powered")

        with col2:
            st.metric("🎯 Skill Analysis", "Smart")

        with col3:
            st.metric("💼 Job Matching", "AI Based")

        with col4:
            st.metric("📚 Learning Roadmap", "Personalized")

        st.divider()

        st.subheader("Get Started")

        st.write(
            "Upload your resume and let Gemini AI analyze "
            "your skills, experience, and career opportunities."
        )

        st.button(
            "Go to Resume Analysis",
            on_click=lambda: st.session_state.update(
                {"selected_page": "📄 Resume Analysis"}
            )
        )


# ==========================================
# 9. RESUME ANALYSIS PAGE
# ==========================================

elif page == "📄 Resume Analysis":

    st.title("📄 Resume Analysis")

    st.write(
        "Upload your resume and receive AI-powered feedback "
        "and career guidance."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or TXT)",
        type=["pdf", "txt"]
    )

    job_role = st.text_input(
        "Enter the job role you are targeting (optional)",
        placeholder="Example: Python Developer"
    )

    analyze = st.button("💜 Analyze Resume")

    if analyze:

        if uploaded_file is None:
            st.warning("Please upload your resume first.")

        else:

            try:

                with st.spinner("Reading your resume..."):

                    file_content = extract_text_from_file(uploaded_file)

                if not file_content.strip():
                    st.error("The uploaded file does not contain readable text.")

                else:

                    prompt = f"""
You are an expert resume reviewer and career advisor.

Analyze the following resume carefully.

Target job role: {job_role if job_role else "General job applications"}

RESUME CONTENT:
{file_content}

Perform the following tasks:

1. Evaluate the resume and its content.
2. Identify strengths and weaknesses.
3. Identify missing skills for the target job role.
4. Perform a detailed skill gap analysis.
5. Recommend 3 suitable job roles based on actual skills,
   education and projects.
6. Give a fair resume score out of 100.
7. Provide a personalized learning roadmap.

For skill gap analysis:
- Identify skills found in the resume.
- Identify skills required but missing.
- Classify each skill as Available, Missing, or Needs Improvement.
- Assign priority: High, Medium, or Low.
- Suggest a learning action for each skill.

For each recommended job role provide:
- Role name.
- Match percentage out of 100.
- Reasons for the match.
- Skills to improve.

Give each category a score out of 100:

1. Contact Information
2. Professional Summary
3. Education
4. Technical Skills
5. Work Experience
6. Projects
7. Certifications
8. ATS Compatibility
9. Formatting and Readability
10. Job Role Relevance

Scoring rules:
- Give a fair score based on the information actually present.
- For freshers, do not penalize missing work experience heavily.
- Evaluate projects and academic experience appropriately.
- Do not assume missing information.
- Explain each category score briefly.
- Calculate the overall score using the category scores.

Return valid JSON only using exactly this structure:

{{
    "overall_score": 0,
    "categories": [
        {{
            "name": "Contact Information",
            "score": 0,
            "reason": "Explanation"
        }}
    ],
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "suggestions": [],
    "learning_roadmap": [],
    "skill_gap_analysis": [
        {{
            "skill": "Python",
            "status": "Available",
            "priority": "Low",
            "learning_action": "Continue practising Python"
        }}
    ],
    "job_recommendations": [
        {{
            "role": "Python Developer",
            "match_percentage": 80,
            "reasons": ["Has Python knowledge"],
            "skills_to_improve": ["SQL", "Django"]
        }}
    ]
}}

Do not invent qualifications, skills, certifications, or experience.
Return JSON only. Do not use Markdown code fences.
"""

                    st.info("Starting Gemini AI resume analysis...")

                    with st.spinner("Gemini is analyzing your resume..."):

                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt
                        )

                    ai_feedback = response.text or ""

                    # Remove Markdown JSON code fences if present
                    ai_feedback = ai_feedback.strip()

                    if ai_feedback.startswith("```"):
                        ai_feedback = ai_feedback.replace(
                            "```json", "", 1
                        ).replace("```", "")

                    # Convert response into Python dictionary
                    resume_data = json.loads(ai_feedback.strip())

                    # Save results between navigation pages
                    st.session_state.resume_data = resume_data

                    st.success("Resume analysis completed successfully! 💜")

                    st.metric(
                        "Overall Resume Score",
                        f"{int(resume_data.get('overall_score', 0))}/100"
                    )

                    display_categories(resume_data)

                    st.subheader("Resume Strengths")

                    for item in resume_data.get("strengths", []):
                        st.write("✅", item)

                    st.subheader("Areas to Improve")

                    for item in resume_data.get("weaknesses", []):
                        st.write("⚠️", item)

                    st.subheader("Improvement Suggestions")

                    for item in resume_data.get("suggestions", []):
                        st.write("•", item)

            except json.JSONDecodeError:
                st.error(
                    "Gemini did not return valid JSON. "
                    "Please try analyzing the resume again."
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Show previous analysis when returning to this page
    if st.session_state.resume_data is not None and not analyze:

        st.info(
            "Your previous analysis is saved. "
            "You can explore it using the sidebar."
        )

        st.metric(
            "Overall Resume Score",
            f"{int(st.session_state.resume_data.get('overall_score', 0))}/100"
        )


# ==========================================
# 10. SKILL GAP ANALYSIS PAGE
# ==========================================

elif page == "🎯 Skill Gap Analysis":

    st.title("🎯 Skill Gap Analysis")

    resume_data = st.session_state.resume_data

    if resume_data is None:

        st.info("Please analyze your resume first.")

    else:

        skill_gap = resume_data.get("skill_gap_analysis", [])

        if not skill_gap:
            st.info("No skill gap information was returned.")

        for skill in skill_gap:

            st.subheader(skill.get("skill", "Unknown Skill"))

            st.write(
                f"**Status:** {skill.get('status', 'Not specified')}"
            )

            st.write(
                f"**Priority:** {skill.get('priority', 'Not specified')}"
            )

            st.write(
                f"**Learning Action:** "
                f"{skill.get('learning_action', 'No action provided')}"
            )

            st.divider()

        st.subheader("Missing Skills")

        for item in resume_data.get("missing_skills", []):
            st.write("•", item)


# ==========================================
# 11. JOB RECOMMENDATIONS PAGE
# ==========================================

elif page == "💼 Job Recommendations":

    st.title("💼 Job Role Recommendations")

    resume_data = st.session_state.resume_data

    if resume_data is None:

        st.info("Please analyze your resume first.")

    else:

        recommendations = resume_data.get(
            "job_recommendations", []
        )

        if not recommendations:
            st.info("No job recommendations were returned.")

        for job in recommendations:

            st.subheader(job.get("role", "Recommended Role"))

            match = int(job.get("match_percentage", 0))
            match = max(0, min(match, 100))

            st.metric("Match Percentage", f"{match}%")
            st.progress(match / 100)

            st.write("**Why this role matches:**")

            for reason in job.get("reasons", []):
                st.write("✅", reason)

            st.write("**Skills to improve:**")

            for skill in job.get("skills_to_improve", []):
                st.write("📌", skill)

            st.divider()


# ==========================================
# 12. LEARNING ROADMAP PAGE
# ==========================================

elif page == "📚 Learning Roadmap":

    st.title("📚 Career Learning Roadmap")

    resume_data = st.session_state.resume_data

    if resume_data is None:

        st.info("Please analyze your resume first.")

    else:

        roadmap = resume_data.get("learning_roadmap", [])

        if not roadmap:
            st.info("No learning roadmap was returned.")

        for index, item in enumerate(roadmap, start=1):

            st.write(f"**Step {index}**")
            st.write("📌", item)

            st.divider()

        st.subheader("Additional Improvement Suggestions")

        for item in resume_data.get("suggestions", []):
            st.write("•", item)
