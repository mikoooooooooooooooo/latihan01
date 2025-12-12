import streamlit as st
import json
import os

# ======================
# PATH SETTINGS
# ======================
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")

# ======================
# IO SETTINGS
# ======================
def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings():
    payload = {
        "app_theme": "Dark Blue",
        "line_template": st.session_state.get("line_template", "plotly"),
        "map_template": st.session_state.get("map_template", "plotly"),
        "palette_mode": st.session_state.get("palette_mode", "Fixed"),
        "palette_fixed": st.session_state.get(
            "palette_fixed",
            ["#e41a1c", "#ff7f00", "#377eb8", "#4daf4a", "#984ea3"]
        ),
    }
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

# ======================
# INIT SETTINGS
# ======================
def init_settings():
    defaults = {
    "app_theme": "Dark Blue",
    "line_template": "plotly",
    "map_template": "plotly",
    "palette_mode": "Fixed",
    "palette_fixed": ["#e41a1c", "#ff7f00", "#377eb8", "#4daf4a", "#984ea3"],
    "filter_countries": None,
    "filter_year_range": None,
}

    if st.session_state.get("_settings_inited", False):
        return
        
    file_settings = load_settings()
    for k, v in defaults.items():
        st.session_state[k] = file_settings.get(k, v)

    st.session_state["_settings_inited"] = True

# ======================
# APPLY CSS THEME
# ======================
def apply_app_theme_css():
    theme = st.session_state.get("app_theme", "Dark Blue")

    # NORMALISASI
    if theme not in ("Dark Blue", "Dark Green"):
        theme = "Dark Blue"
        st.session_state["app_theme"] = "Dark Blue"

    # ======================
    # DARK BLUE (default)
    # ======================
    if theme == "Dark Blue":
        bg = "#0e1117"
        fg = "#e6edf3"
        card = "#161b22"
        border = "#30363d"
        sidebar = "#0b1220"

    # ======================
    # DARK GREEN
    # ======================
    else:  
        bg = "#0f1f17"
        fg = "#e6f4ea"
        card = "#152d22"
        border = "#2d4a3e"
        sidebar = "#0b1a14"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {bg};
            color: {fg};
        }}

        section[data-testid="stSidebar"] > div {{
            background: {sidebar};
            border-right: 1px solid {border};
        }}

        div[data-testid="stMetric"] {{
            background: {card};
            border: 1px solid {border};
            border-radius: 14px;
            padding: 10px 12px;
        }}

        .stDataFrame {{
            background: {card};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ======================
# RUN
# ======================
init_settings()
apply_app_theme_css()

pages = [
    st.Page("pages/page1.py", title="Inflasi Dunia", icon="🌍"),
    st.Page("pages/page2.py", title="Pengaturan", icon="⚙️"),
    st.Page("pages/page3.py", title="Tentang", icon="ℹ️"),
]

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()
