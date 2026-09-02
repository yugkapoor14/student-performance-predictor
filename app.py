import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

st.set_page_config(
    page_title="EduRisk AI | Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

ACCENT = "#F5B942"
ACCENT_DARK = "#D97706"

def icon(path_data, size=18, color=ACCENT, stroke=2, extra=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;flex-shrink:0;{extra}">{path_data}</svg>'''

ICONS = {
    "house": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "trending_up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "users": '<path d="M18 21a8 8 0 0 0-16 0"/><circle cx="10" cy="8" r="5"/><path d="M22 20c0-3.37-2-6.5-4-8a5 5 0 0 0-.45-8.3"/>',
    "chart": '<path d="M5 21v-6"/><path d="M12 21V3"/><path d="M19 21V9"/>',
    "file_text": '<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "settings": '<path d="M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915"/><circle cx="12" cy="12" r="3"/>',
    "clipboard_check": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "shield_check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "alert_triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "brain_circuit": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M9 13a4.5 4.5 0 0 0 3-4"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M12 13h4"/><path d="M12 18h6a2 2 0 0 1 2 2v1"/><path d="M12 8h8"/><path d="M16 8V5a2 2 0 0 1 2-2"/><circle cx="16" cy="13" r=".5"/><circle cx="18" cy="3" r=".5"/><circle cx="20" cy="21" r=".5"/><circle cx="20" cy="8" r=".5"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
    "bell": '<path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/>',
    "chevron_down": '<path d="m6 9 6 6 6-6"/>',
}

LOGO_SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="{ACCENT}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
<path d="M12 2 3.5 6v6c0 5 3.6 8.7 8.5 10 4.9-1.3 8.5-5 8.5-10V6z"/>
<path d="M8 11.5 12 9l4 2.5"/>
<path d="M8 11.5v3.2L12 17l4-2.3v-3.2"/>
<path d="M12 9v3.6"/>
<circle cx="8" cy="11.5" r=".6" fill="{ACCENT}"/>
<circle cx="16" cy="11.5" r=".6" fill="{ACCENT}"/>
</svg>'''

BG = "#0A0D13"
SIDEBAR_BG = "#0F131B"
CARD_BG = "#10141C"
INPUT_BG = "#151A24"
BORDER = "#262D3D"
TEXT = "#F8FAFC"
TEXT_MUTED = "#8792A6"
TEXT_DIM = "#5C6577"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{ font-family: 'Manrope', -apple-system, sans-serif; }}
    html {{ color-scheme: dark; }}
    .stApp {{ background: {BG}; }}
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* don't hide the whole header - sidebar collapse arrow lives inside it */
    header[data-testid="stHeader"] {{ background: transparent !important; height: 48px !important; }}
    div[data-testid="stToolbar"] {{ visibility: hidden !important; }}
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarExpandButton"],
    [data-testid="stSidebarCollapsedControl"],
    button[aria-label*="sidebar" i],
    button[title*="sidebar" i] {{
        display: none !important;
    }}
    div[data-testid="stSidebar"] {{ display: none !important; }}

    /* custom sidebar built from a column - can never collapse */
    div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child {{
        background: {SIDEBAR_BG};
        border-right: 1px solid #232A3A;
        min-height: 100vh;
        padding: 0.6rem 0.6rem 1rem 0.6rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:last-child {{
        padding: 0.9rem 1.6rem 1rem 1.6rem !important;
    }}

    .sidebar-logo {{
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        gap: 8px; text-align: center;
        font-size: 18px; font-weight: 800; color: {TEXT};
        margin-bottom: 14px; padding: 2px 0 12px 0;
        border-bottom: 1px solid #202632;
    }}
    .sidebar-logo span {{ color: {ACCENT}; }}

    .nav-item {{
        display: flex; align-items: center; gap: 11px; min-height: 42px;
        padding: 10px 12px; border-radius: 10px;
        color: #8F99AA; font-weight: 600; font-size: 13.5px;
        margin-bottom: 4px;
    }}
    .nav-item.active {{ background: {ACCENT}; color: #2B1B02; box-shadow: 0 5px 16px rgba(245,185,66,0.22); }}
    .nav-item.disabled {{ opacity: 0.55; }}

    .insight-card {{
        background: linear-gradient(160deg, #2E210A 0%, #1A1206 100%);
        border: 1px solid #4A3A1E; border-radius: 14px; padding: 16px; margin-top: 24px;
    }}
    .insight-card .ic-title {{ display:flex; align-items:center; gap:8px; color: #F1F5F9; font-size: 13px; font-weight:700; margin: 0 0 7px 0; }}
    .insight-card p {{ color: #8B96A8; font-size: 12px; line-height: 1.55; margin: 0; }}

    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {{
        background: #12161F !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        color: #E2E8F0 !important;
        font-size: 14px !important; font-weight: 600 !important;
        padding: 8px 16px !important; min-height: 40px !important;
        transition: all 0.15s;
    }}
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {{
        border-color: {ACCENT} !important; color: {ACCENT} !important;
    }}

    .stApp button[title="Notifications"] {{
        border-radius: 50% !important;
        width: 42px !important; height: 42px !important; padding: 0 !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        font-size: 17px !important; position: relative;
    }}
    .stApp button[title="Notifications"]::after {{
        content: ""; position: absolute; top: 9px; right: 11px;
        width: 7px; height: 7px; border-radius: 50%;
        background: #F87171; border: 1.5px solid #12161F;
    }}

    .stApp button[title="Account menu"] {{ padding: 6px 18px 6px 34px !important; position: relative; font-weight: 600 !important; }}
    .stApp button[title="Account menu"]::before {{
        content: "A"; position: absolute; left: 6px; top: 50%; transform: translateY(-50%);
        width: 26px; height: 26px; border-radius: 50%;
        background: {ACCENT}; color: #2B1B02; font-size: 12px; font-weight: 800;
        display: flex; align-items: center; justify-content: center; line-height: 26px; text-align: center;
    }}

    .greeting {{ font-size: 23px; font-weight: 800; color: {TEXT}; margin: -30px 0 2px 0; letter-spacing: -0.3px; }}
    .greeting-sub {{ color: {TEXT_MUTED}; font-size: 13.5px; margin-bottom: 18px; }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {CARD_BG};
        border: 1px solid {BORDER} !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        padding: 6px 4px !important;
    }}

    .card-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 17px; }}
    .card-icon {{
        background: #2E210A; width: 38px; height: 38px; border-radius: 11px;
        display: flex; align-items: center; justify-content: center; flex-shrink: 0;
        position: relative;
    }}
    .card-icon-badge {{
        position: absolute; bottom: 1px; right: 1px;
        width: 13px; height: 13px; border-radius: 50%;
        background: {ACCENT}; border: 1.5px solid {CARD_BG};
        display: flex; align-items: center; justify-content: center;
    }}
    .card-title {{ color: {TEXT}; font-weight: 700; font-size: 16px; margin: 0; letter-spacing: -0.2px; }}
    .card-subtitle {{ color: {TEXT_MUTED}; font-size: 12.5px; margin: 2px 0 0 0; }}

    .field-label {{
        color: #C7CEDA; font-weight: 700; font-size: 12px; text-transform: uppercase;
        letter-spacing: 0.35px; margin-bottom: 8px; margin-top: 8px;
    }}

    div[data-baseweb="select"] > div {{
        background-color: {INPUT_BG} !important;
        border: 1px solid #2E3648 !important;
        color: #F1F5F9 !important;
        border-radius: 10px !important;
        min-height: 50px !important;
        outline: none !important;
        box-shadow: none !important;
    }}
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:focus,
    div[data-baseweb="select"] > div:focus-within {{
        border-color: {ACCENT} !important;
        outline: none !important;
        box-shadow: 0 0 0 1px {ACCENT} !important;
    }}
    div[data-baseweb="select"] input {{ outline: none !important; box-shadow: none !important; }}
    div[data-baseweb="select"] span {{ color: #F1F5F9 !important; font-weight: 500; }}
    div[data-baseweb="popover"] ul,
    ul[data-testid="stSelectboxVirtualDropdown"] {{
        background: {INPUT_BG} !important; border: 1px solid #2E3648 !important;
    }}
    div[data-baseweb="popover"] li,
    li[data-testid="stSelectboxVirtualDropdownOption"],
    li[role="option"] {{
        color: #E2E8F0 !important;
    }}
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"],
    li[data-testid="stSelectboxVirtualDropdownOption"]:hover,
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {{
        background: #1E2534 !important; color: {ACCENT} !important;
    }}

    .stApp button[kind="primary"],
    .stApp button[title="Run prediction"],
    .stApp div[data-testid="stElementContainer"]:has(#predict-btn-marker) + div[data-testid="stElementContainer"] button {{
        background: linear-gradient(90deg, {ACCENT_DARK}, {ACCENT}) !important;
        border: none !important; border-radius: 12px !important;
        padding: 13px 0 !important; margin-top: 18px !important; min-height: 48px !important;
        box-shadow: 0 10px 24px rgba(245,185,66,0.20) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }}
    .stApp button[kind="primary"]:hover,
    .stApp button[title="Run prediction"]:hover,
    .stApp div[data-testid="stElementContainer"]:has(#predict-btn-marker) + div[data-testid="stElementContainer"] button:hover {{ transform: translateY(-1px); box-shadow: 0 13px 28px rgba(245,185,66,0.28) !important; }}
    .stApp button[kind="primary"] p,
    .stApp button[title="Run prediction"] p,
    .stApp div[data-testid="stElementContainer"]:has(#predict-btn-marker) + div[data-testid="stElementContainer"] button p {{ color: #2B1B02 !important; font-weight: 800 !important; font-size: 14px !important; }}

    .result-title-high {{ color: #F87171; font-size: 20px; font-weight: 800; margin: 0 0 6px 0; display:flex; align-items:center; gap:8px; }}
    .result-title-low {{ color: #4ADE80; font-size: 20px; font-weight: 800; margin: 0 0 6px 0; display:flex; align-items:center; gap:8px; }}
    .result-desc {{ color: #99A2B5; font-size: 13px; line-height: 1.55; margin-bottom: 14px; }}

    .tip-box {{ background: {INPUT_BG}; border: 1px solid {BORDER}; border-radius: 12px; padding: 13px 15px; margin-top: 12px; }}
    .tip-box .tip-title {{ display:flex; align-items:center; gap:7px; color: #F1F5F9; font-weight: 700; font-size: 13px; margin-bottom: 4px; }}
    .tip-box .tip-text {{ color: {TEXT_MUTED}; font-size: 12.5px; line-height: 1.55; margin: 0; }}

    .assurance-box {{
        background: #1A1206; border: 1px solid #4A3A1E; border-radius: 12px;
        padding: 13px 15px; margin-top: 10px;
        display: flex; align-items: flex-start; gap: 8px;
        color: {ACCENT}; font-size: 12.5px; font-weight: 600; line-height: 1.5;
    }}
    .assurance-box span {{ flex: 1; min-width: 0; }}

    .suggestion-box {{
        background: {INPUT_BG}; border: 1px solid {BORDER}; border-left: 3px solid {ACCENT};
        padding: 11px 14px; border-radius: 10px; margin-bottom: 8px;
        color: #E2E8F0; font-size: 13px; line-height: 1.55;
        display: flex; align-items: flex-start;
    }}
    .suggestion-box span {{ flex: 1; min-width: 0; }}

    .footer-note {{
        display:flex; align-items:center; justify-content:center; gap:8px;
        color: {TEXT_DIM}; font-size: 11.5px; margin-top: 16px; flex-wrap: wrap;
    }}
    .footer-note b {{ color: {ACCENT}; }}

    @media (max-width: 900px) {{
        div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child {{
            padding: 0.5rem !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:last-child {{
            padding: 0.6rem 0.8rem !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

try:
    model = joblib.load("risk_model.pkl")
except Exception:
    st.error("Unable to load risk_model.pkl. Make sure the model file is in the same folder as this app.")
    st.stop()

layout_sidebar, layout_main = st.columns([1, 3.6], gap="large")

with layout_sidebar:
    st.markdown(f'<div class="sidebar-logo">{LOGO_SVG}<div>Edu<span>Risk</span> AI</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="nav-item active">{icon(ICONS["house"], 16, "#2B1B02")} &nbsp; Dashboard</div>', unsafe_allow_html=True)

    upcoming = [
        ("trending_up", "Predictions"), ("users", "Students"),
        ("chart", "Analytics"), ("file_text", "Reports"), ("settings", "Settings"),
    ]
    for icon_name, label in upcoming:
        st.markdown(f'<div class="nav-item disabled">{icon(ICONS[icon_name], 16, "#E2E8F0")} &nbsp; {label}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <p class="ic-title">{icon(ICONS["sparkles"], 15)} AI-Powered Insights</p>
        <p>Helping educators identify at-risk students early and improve outcomes.</p>
    </div>
    """, unsafe_allow_html=True)

with layout_main:
    top_col1, top_col2, top_col3 = st.columns([7, 0.7, 1.3])
    with top_col2:
        if st.button("🔔", key="notif_btn", help="Notifications"):
            st.toast("No new notifications", icon="🔔")
    with top_col3:
        if st.button("Admin", key="admin_menu_btn", use_container_width=True, help="Account menu"):
            st.toast("Signed in as Admin", icon="👤")

    st.markdown('<p class="greeting">Welcome back, Admin 👋</p>', unsafe_allow_html=True)
    st.markdown('<p class="greeting-sub">Predict and analyze academic risk for students using AI</p>', unsafe_allow_html=True)

display_map = {
    "gender": {"female": "Female", "male": "Male"},
    "race": {"group A": "Group A", "group B": "Group B", "group C": "Group C", "group D": "Group D", "group E": "Group E"},
    "lunch": {"standard": "Standard", "free/reduced": "Free / Reduced"},
    "parent_edu": {
        "some high school": "Some High School", "high school": "High School",
        "some college": "Some College", "associate's degree": "Associate's Degree",
        "bachelor's degree": "Bachelor's Degree", "master's degree": "Master's Degree"
    },
    "test_prep": {"none": "None", "completed": "Completed"}
}

defaults = {"gender": "female", "race": "group A", "lunch": "standard", "parent_edu": "some high school", "test_prep": "none"}
for key, value in defaults.items():
    if f"sel_{key}" not in st.session_state:
        st.session_state[f"sel_{key}"] = value

def field_selector(field_key, field_label, number):
    st.markdown(f'<div class="field-label">{number}. {field_label}</div>', unsafe_allow_html=True)
    options = display_map[field_key]
    keys = list(options.keys())
    current_index = keys.index(st.session_state[f"sel_{field_key}"])
    selected = st.selectbox(
        field_label, keys, index=current_index,
        format_func=lambda k: options[k],
        key=f"select_{field_key}", label_visibility="collapsed"
    )
    st.session_state[f"sel_{field_key}"] = selected

with layout_main:
    with st.container(border=True):
        st.markdown(f"""
        <div class="card-header">
            <div class="card-icon">{icon(ICONS["clipboard_check"], 18)}<span class="card-icon-badge">{icon('<path d="m9 14 2 2 4-4"/>', 7, "#2B1B02", 3)}</span></div>
            <div>
                <p class="card-title">Student Risk Prediction</p>
                <p class="card-subtitle">Fill in the student details below to predict academic risk</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        row1_col1, row1_col2 = st.columns(2, gap="medium")
        with row1_col1:
            field_selector("gender", "Gender", 1)
        with row1_col2:
            field_selector("race", "Group", 2)

        row2_col1, row2_col2 = st.columns(2, gap="medium")
        with row2_col1:
            field_selector("lunch", "Lunch Type", 3)
        with row2_col2:
            field_selector("parent_edu", "Parental Education", 4)

        row3_col1, row3_col2 = st.columns(2, gap="medium")
        with row3_col1:
            field_selector("test_prep", "Test Preparation", 5)

        st.markdown('<div id="predict-btn-marker"></div>', unsafe_allow_html=True)
        submitted = st.button("Predict Risk  →", key="predict_btn", use_container_width=True, type="primary", help="Run prediction")

    if submitted:
        gender = st.session_state["sel_gender"]
        race = st.session_state["sel_race"]
        lunch = st.session_state["sel_lunch"]
        parent_edu = st.session_state["sel_parent_edu"]
        test_prep = st.session_state["sel_test_prep"]

        input_df = pd.DataFrame([{
            "gender": gender, "race_ethnicity": race, "parental_level_of_education": parent_edu,
            "lunch": lunch, "test_preparation_course": test_prep
        }])

        try:
            proba = model.predict_proba(input_df)[0][1]
        except Exception:
            st.error("The model could not process these inputs. Check that the model was trained on the same five columns.")
            st.stop()

        risk_pct = round(proba * 100, 1)
        is_high = risk_pct >= 50
        display_pct = risk_pct if is_high else round(100 - risk_pct, 1)
        ring_color = "#F87171" if is_high else "#4ADE80"

        with st.container(border=True):
            st.markdown(f"""
            <div class="card-header">
                <div class="card-icon">{icon(ICONS["target"], 18)}</div>
                <div>
                    <p class="card-title">Prediction Result</p>
                    <p class="card-subtitle">AI model prediction outcome</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            result_col1, result_col2, result_col3 = st.columns([1, 1.5, 1.3], gap="large")
            with result_col1:
                fig = go.Figure(go.Pie(
                    values=[display_pct, 100 - display_pct], hole=0.78,
                    marker=dict(colors=[ring_color, "#1E2534"]),
                    textinfo="none", direction="clockwise", sort=False, rotation=0,
                ))
                fig.update_layout(
                    showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=210, width=210,
                    paper_bgcolor="rgba(0,0,0,0)",
                    annotations=[dict(
                        text=f"<b>{display_pct}</b><span style='font-size:16px'>%</span><br><span style='font-size:12px;color:#8792A6'>Risk Score</span>",
                        x=0.5, y=0.5, font=dict(size=32, color="#F8FAFC", family="Manrope"), showarrow=False
                    )]
                )
                st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})

            with result_col2:
                if is_high:
                    st.markdown(f'<p class="result-title-high">{icon(ICONS["alert_triangle"], 19, "#F87171")} High Risk</p>', unsafe_allow_html=True)
                    st.markdown('<p class="result-desc">This student is predicted to be at high academic risk. Early intervention is recommended.</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="result-title-low">{icon(ICONS["shield_check"], 19, "#4ADE80")} Low Risk</p>', unsafe_allow_html=True)
                    st.markdown('<p class="result-desc">This student is predicted to perform well academically. Continue current support.</p>', unsafe_allow_html=True)

                suggestions = []
                if test_prep == "none":
                    suggestions.append(("clipboard_check", "Enroll in a <b>test preparation course</b> — historically raises scores by ~7-8 points."))
                if lunch == "free/reduced":
                    suggestions.append(("users", "Flag for <b>academic support program</b> — measurable performance gap observed."))
                if parent_edu in ["some high school", "high school"]:
                    suggestions.append(("file_text", "Provide <b>additional take-home material</b> for extra academic support."))
                if not suggestions:
                    suggestions.append(("shield_check", "No major risk factors detected — maintain current support."))

                for icon_name, s in suggestions:
                    st.markdown(f'<div class="suggestion-box">{icon(ICONS[icon_name], 16, ACCENT, extra="margin-right:8px;margin-top:2px;")}<span>{s}</span></div>', unsafe_allow_html=True)

            with result_col3:
                meaning = "higher" if is_high else "lower"
                action = "Consider additional support." if is_high else "Keep monitoring periodically."
                st.markdown(f"""
                <div class="tip-box">
                    <div class="tip-title">{icon(ICONS["lightbulb"], 14)} What does this mean?</div>
                    <p class="tip-text">Students with similar profiles show a {meaning} chance of academic difficulty. {action}</p>
                </div>
                <div class="assurance-box">
                    {icon(ICONS["shield_check"], 16)}
                    <span>Always use insights to support, not replace, human judgment.</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown(f"""
    <p class="footer-note">{icon(ICONS["shield_check"], 13, TEXT_DIM)} Predictions are based on machine learning models and historical data.<br>
    <b>Always use insights to support, not replace, human judgment.</b></p>
    """, unsafe_allow_html=True)
