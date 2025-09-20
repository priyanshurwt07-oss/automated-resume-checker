import streamlit as st
import pandas as pd

st.title("Bulk Resume-to-JD Relevance Checker")
st.write("Upload multiple Job Description (JD) files and multiple Resume files to find best matches.")

# Upload multiple JD files
jd_files = st.file_uploader("Upload JD files (txt)", type=["txt"], accept_multiple_files=True)

# Upload multiple Resume files
resume_files = st.file_uploader("Upload Resume files (txt)", type=["txt"], accept_multiple_files=True)

if st.button("Evaluate All"):
    if not jd_files or not resume_files:
        st.warning("Please upload both JD files and Resume files!")
    else:
        # Read JD files
        jd_texts = {}
        for jd in jd_files:
            jd_texts[jd.name] = jd.read().decode("utf-8").lower().replace("\n", ",").split(",")

        # Clean up JD skills
        for key in jd_texts:
            jd_texts[key] = [skill.strip() for skill in jd_texts[key] if skill.strip()]

        # Read Resume files
        resume_texts = {}
        for res in resume_files:
            resume_texts[res.name] = res.read().decode("utf-8").lower()

        # Prepare results list
        results = []

        # Compare each resume with each JD
        for res_name, res_text in resume_texts.items():
            best_score = -1
            best_jd = ""
            best_matched = []
            best_missing = []

            for jd_name, skills in jd_texts.items():
                matched = [skill for skill in skills if skill in res_text]
                missing = [skill for skill in skills if skill not in res_text]
                score = len(matched) / len(skills) * 100 if skills else 0

                if score > best_score:
                    best_score = score
                    best_jd = jd_name
                    best_matched = matched
                    best_missing = missing

            # Determine verdict
            if best_score >= 75:
                verdict = "High"
            elif best_score >= 50:
                verdict = "Medium"
            else:
                verdict = "Low"

            results.append({
                "Resume": res_name,
                "Best JD Match": best_jd,
                "Score": round(best_score, 2),
                "Verdict": verdict,
                "Matched Skills": ", ".join(best_matched),
                "Missing Skills": ", ".join(best_missing)
            })

        # Convert to DataFrame and display
        df = pd.DataFrame(results)
        st.subheader("Best JD Matches for Each Resume")
        st.dataframe(df)
