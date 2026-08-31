import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Student Performance & Academic Risk Analytics", layout="centered")

model = joblib.load("model.pkl") if False else joblib.load("risk_model.pkl")

st.title("📊 Student Performance Predictor & Academic Analytics")
st.caption("AI-based tool to flag academic risk early and suggest targeted interventions.")

st.markdown("### Enter Student Details")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["female", "male"])
    race = st.selectbox("Race/Ethnicity Group", ["group A", "group B", "group C", "group D", "group E"])
    lunch = st.selectbox("Lunch Type", ["standard", "free/reduced"])
with col2:
    parent_edu = st.selectbox("Parental Education", [
        "some high school", "high school", "some college",
        "associate's degree", "bachelor's degree", "master's degree"
    ])
    test_prep = st.selectbox("Test Preparation Course", ["none", "completed"])

if st.button("Predict Academic Risk", type="primary"):
    input_df = pd.DataFrame([{
        "gender": gender,
        "race_ethnicity": race,
        "parental_level_of_education": parent_edu,
        "lunch": lunch,
        "test_preparation_course": test_prep
    }])

    proba = model.predict_proba(input_df)[0][1]
    risk_pct = round(proba * 100, 1)

    st.markdown("---")
    st.markdown("### Result")

    if risk_pct >= 50:
        st.error(f"⚠️ At-Risk: {risk_pct}% probability of underperforming (avg score < 60)")
    else:
        st.success(f"✅ On Track: {100 - risk_pct}% probability of performing well")

    st.markdown("### 💡 Recommended Interventions")
    suggestions = []
    if test_prep == "none":
        suggestions.append("Enroll in a **test preparation course** — historically raises average scores by ~7-8 points.")
    if lunch == "free/reduced":
        suggestions.append("Flag for **academic support program** — students on free/reduced lunch show a measurable performance gap; consider free tutoring resources.")
    if parent_edu in ["some high school", "high school"]:
        suggestions.append("Provide **additional take-home learning material** to compensate for lower access to academic support at home.")
    if not suggestions:
        suggestions.append("No major risk factors detected — maintain current academic support.")

    for s in suggestions:
        st.write("- " + s)

    st.markdown("---")
    st.caption("Model: Random Forest Classifier | Trained on 1000 student records | Explainable, factor-based predictions")

with st.expander("ℹ️ About this tool"):
    st.write("""
    This tool predicts a student's risk of underperforming academically using demographic and
    contextual factors (parental education, lunch/economic indicator, test preparation access).
    It's designed to help schools **proactively identify** students who may need extra support,
    rather than reacting after grades are already low.

    **Scalability:** This model can be extended school-wide or district-wide by integrating live
    data (attendance systems, LMS activity, past grades) for continuous, automated risk monitoring.
    """)
