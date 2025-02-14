import streamlit as st
import pdfplumber

import google.generativeai as genai
genai.configure(api_key="AIzaSyCQcAZpBJi2ox3FZB1zXHGvYhDH8VGepL0")
model = genai.GenerativeModel(model_name="gemini-pro")



def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""



def stage1(text):
  stage1_prompt=f"""
  Extract the following information from the provided resume text:
  - Name
  - Contact Information (email, phone, LinkedIn)
  - Summary/Objective
  - Work Experience (company, job title, dates, responsibilities)
  - Education (institution, degree, dates)
  - Skills (technical and soft skills)
  - Projects (project name, description, technologies used)
  - Awards and Recognition (if any)

  Resume Text: {text}
  """

  stage1_response = model.generate_content(stage1_prompt)
  return stage1_response.text

def analyze_resume(resume_text, job_role, domain):
  stage2_prompt=f"""
  Analyze the provided resume information for a candidate applying for the [Job Role] in the [Domain] domain. Evaluate the resume based on the following criteria:

  1. **Relevance to Job Role:** How well does the resume align with the target job role and domain?  Consider the match between skills, experience, and job requirements.
  2. **Strengths:** Identify the strongest aspects of the resume. What makes the candidate stand out?
  3. **Weaknesses:** Point out areas for improvement. Are there any missing skills, gaps in experience, or poorly written sections?
  4. **Actionable Suggestions:** Provide specific, actionable suggestions to improve the resume.  Focus on wording, structure, and content.  Examples:
    - "Quantify achievements whenever possible. Instead of 'Managed social media accounts,' write 'Increased social media engagement by 20% in six months.'"
    - "Tailor the summary/objective to the specific job role. Highlight relevant skills and experience."
    - "Use action verbs to describe responsibilities in the work experience section."

  Resume Information: {resume_text}
  Job Role: {job_role}
  Domain: {domain}
  """
  stage2_response = model.generate_content(stage2_prompt)
  return stage2_response.text










st.title("Resume Analyzer 🚀")
st.markdown("Enhance your resume with AI-powered insights!")

# Input fields
col1, col2 = st.columns(2)  # Create two columns for better layout

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    job_role = st.text_input("Target Job Role")

with col2:

    #domain = st.selectbox("Domain", ["Data Science", "Software Engineering", "Marketing", "Business Analyst", "Product Management","Machine Learning","Full Stack Web","App Development", "Other"]) # Add more domains
    domain=st.text_input("Domain")
    # Or use a text input for more flexibility:
    #domain = st.text_input("Domain (e.g., Data Science, Software Engineering)")

if st.button("Analyze"):
    if uploaded_file and job_role and domain:
        with st.spinner("Analyzing your resume..."): # Add a spinner
            text = extract_text_from_pdf(uploaded_file)
            resume_text = stage1(text)

            if resume_text:
                analysis = analyze_resume(resume_text, job_role, domain)
                st.markdown(analysis)  # Display the analysis using Markdown
    else:
        st.warning("Please upload a resume and provide the job role and domain.")
