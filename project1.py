import streamlit as st
import pypdf 
import io
import os 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=".evn", override=True)


st.set_page_config(page_title="AI resume critiquer", page_icon="📃",layout="centered")

st.title("ai resume critiquer")
st.markdown("upload your resume and get AI-powered feedback tailored to your needs!")

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("API key not loaded.check your .env file.")

uploaded_file = st.file_uploader("upload your resume(PDF, TXT, PNG, OR JPG)",type=["pdf","txt","png","jpg","jpeg"])
accept_multiple_files=False
job_role = st.text_input("enter the job role that you are targeting (optional).")

analyze = st.button("analyze resume")


def extract_text_from_pdf(uploaded_file):
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text=""
    for page in pdf_reader.pages:
        text += (page.extract_text() or"") + "\n"
    return text



def extract_text_from_file(uploaded_file):
    if uploaded_file.type =="application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
       

if analyze and uploaded_file:
    st.info("analysis started...")
    try:
        file_content = extract_text_from_file(uploaded_file)
        st.write("step 1: resume text extracted.")
        st.write("checking resume text...")
        st.write("extracted text length:", len(file_content))
        st.write("debug: reached text check")

        if not file_content.strip():
            st.error("file does not have any content...")
            st.stop()

        st.write("debug: resume is not empty")

        st.write("resume text is not empty.continuing...")

        prompt = f"""please analyze this resume and provide constructive feedback.
            focus on the following aspects:
            1. content clarity and impact
            2. skills presentation
            3. experience description
            4. specific improvements for{job_role if job_role else 'general job applications'}

            resume content:
            {file_content}

            please provide your analysis in a clear, structured format with specific recommendations."""

        
        st.write("Step 2: Starting free resume analysis...")

        resume_lower = file_content.lower()
        feedback = []

        # Check contact information
        if "@" in file_content:
            feedback.append("✅ Email address appears to be included.")
        else:
            feedback.append("⚠️ Add a professional email address.")

        # Check important resume sections
        sections = {
            "Education": ["education", "degree", "college", "university"],
            "Skills": ["skills", "technical skills", "programming"],
            "Experience": ["experience", "internship", "work history"],
            "Projects": ["projects", "project"]
        }

        for section, keywords in sections.items():
            if any(word in resume_lower for word in keywords):
                feedback.append(f"✅ {section} section appears to be included.")
            else:
                feedback.append(f"⚠️ Consider adding a clear {section} section.")

        # Check the resume length
        word_count = len(file_content.split())
        feedback.append(f"📄 Resume word count: {word_count}")

        if word_count < 150:
            feedback.append("⚠️ Your resume may be too short. Add relevant details.")
        elif word_count > 800:
            feedback.append("⚠️ Consider shortening your resume and keeping it focused.")
        else:
            feedback.append("✅ Resume length looks reasonable.")

        # Give job-role-specific guidance
        if job_role.strip():
            feedback.append(
                f"🎯 Target role: {job_role}. Highlight relevant skills, "
                "projects, education, and achievements for this role."
            )

        st.write("### Resume Analysis Results")
        for item in feedback:
            st.write(item)

    except Exception as e:
        st.error(f"an error occured: {str(e)}")