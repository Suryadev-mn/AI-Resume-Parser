import PyPDF2
import re
import spacy
from skills import skills_list

import subprocess
import sys

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(
        [sys.executable, "-m", "spacy", "download", "en_core_web_sm"]
    )
    nlp = spacy.load("en_core_web_sm")

def extract_text(pdf_file):
    text = ""

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text

def extract_email(text):
    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    match = re.search(pattern, text)

    return match.group() if match else "Not Found"

def extract_phone(text):
    pattern = r'\+?\d[\d\s\-]{8,15}'
    match = re.search(pattern, text)

    return match.group() if match else "Not Found"

def extract_name(text):
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Not Found"

def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills

def extract_education(text):

    education_keywords = [
        "B.Tech",
        "B.E",
        "M.Tech",
        "M.E",
        "BCA",
        "MCA",
        "B.Sc",
        "M.Sc",
        "Bachelor",
        "Master"
    ]

    found_education = []

    for edu in education_keywords:
        if edu.lower() in text.lower():
            found_education.append(edu)

    return found_education

def extract_experience(text):

    experience_keywords = [
        "Intern",
        "Internship",
        "Software Engineer",
        "Developer",
        "Data Analyst",
        "Machine Learning Engineer",
        "Project"
    ]

    found_experience = []

    for exp in experience_keywords:
        if exp.lower() in text.lower():
            found_experience.append(exp)

    return found_experience

def calculate_resume_score(skills, education, experience):

    score = 0

    # Skills
    score += min(len(skills) * 5, 40)

    # Education
    score += min(len(education) * 15, 30)

    # Experience
    score += min(len(experience) * 10, 30)

    return score
def match_job_description(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())

    matches = resume_words.intersection(jd_words)

    if len(jd_words) == 0:
        return 0

    score = (len(matches) / len(jd_words)) * 100

    return round(score, 2)