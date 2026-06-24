import streamlit as st
import pandas as pd
from parser import *

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Parser",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Parser")
st.markdown("Upload one or more resumes and analyze them instantly.")

# -----------------------------
# Job Description
# -----------------------------
st.subheader("📝 Job Description")

job_description = st.text_area(
    "Paste Job Description Here",
    height=150
)

# -----------------------------
# Upload Multiple Resumes
# -----------------------------
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# -----------------------------
# Process Resumes
# -----------------------------
if uploaded_files:

    all_data = []

    for uploaded_file in uploaded_files:

        st.divider()

        st.header(f"📄 {uploaded_file.name}")

        text = extract_text(uploaded_file)

        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)

        skills = extract_skills(text)
        education = extract_education(text)
        experience = extract_experience(text)

        score = calculate_resume_score(
            skills,
            education,
            experience
        )

        # -----------------------------
        # Metrics Section
        # -----------------------------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👤 Name", name)

        with col2:
            st.metric("📧 Email", email)

        with col3:
            st.metric("📞 Phone", phone)

        with col4:
            st.metric("📊 Resume Score", f"{score}/100")

        # -----------------------------
        # Details
        # -----------------------------
        st.write("### 🛠 Skills")
        st.write(skills)

        st.write("### 🎓 Education")
        st.write(education)

        st.write("### 💼 Experience")
        st.write(experience)

        # -----------------------------
        # Resume Score
        # -----------------------------
        st.subheader("📊 Resume Score")

        st.progress(score / 100)

        st.write(f"Score: {score}/100")

        # -----------------------------
        # Job Match Score
        # -----------------------------
        match_score = 0

        if job_description:

            match_score = match_job_description(
                text,
                job_description
            )

            st.subheader("🎯 Job Match Score")

            st.progress(match_score / 100)

            st.write(f"Match Score: {match_score}%")

        # -----------------------------
        # Save For CSV
        # -----------------------------
        all_data.append({
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Skills": ", ".join(skills),
            "Education": ", ".join(education),
            "Experience": ", ".join(experience),
            "Resume Score": score,
            "Job Match Score": match_score
        })

    # -----------------------------
    # CSV Download
    # -----------------------------
    st.divider()

    st.subheader("📥 Download Results")

    df = pd.DataFrame(all_data)

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name="resume_analysis.csv",
        mime="text/csv"
    )

    st.dataframe(df, use_container_width=True)