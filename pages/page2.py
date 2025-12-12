import streamlit as st

PLOTLY_TEMPLATES = ["plotly", "plotly_dark", "ggplot2", "seaborn", "simple_white", "presentation"]

st.title("🫂 Pengaturan")
st.caption("Pengaturan tersimpan (persisten) dan berlaku untuk semua halaman.")

# ======================
# CALLBACK: sync UI -> SETTINGS + SAVE
# ======================
def apply_settings():
    # ambil dari widget UI
    st.session_state["app_theme"] = st.session_state["ui_app_theme"]
    st.session_state["line_template"] = st.session_state["ui_line_template"]
    st.session_state["map_template"] = st.session_state["ui_map_template"]
    st.session_state["palette_mode"] = st.session_state["ui_palette_mode"]

    # simpan ke settings.json (langsung)
    from pathlib import Path
    import json

    settings_path = Path(__file__).resolve().parents[1] / "settings.json"
    payload = {
        "app_theme": st.session_state["app_theme"],
        "line_template": st.session_state["line_template"],
        "map_template": st.session_state["map_template"],
        "palette_mode": st.session_state["palette_mode"],
        "palette_fixed": st.session_state.get(
            "palette_fixed",
            ["#e41a1c", "#ff7f00", "#377eb8", "#4daf4a", "#984ea3"]
        ),
    }
    settings_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

# ======================
# SET DEFAULT UI STATE (HANYA JIKA BELUM ADA)
# Ini kunci supaya widget tidak reset
# ======================
st.session_state.setdefault("ui_app_theme", st.session_state.get("app_theme", "Light"))
st.session_state.setdefault("ui_line_template", st.session_state.get("line_template", "plotly"))
st.session_state.setdefault("ui_map_template", st.session_state.get("map_template", "plotly"))
st.session_state.setdefault("ui_palette_mode", st.session_state.get("palette_mode", "Fixed"))

# ======================
# UI CONTROLS (pakai key ui_*)
# ======================
st.subheader("1) Tema Aplikasi")
st.radio(
    "Tema aplikasi",
    ["Dark Blue", "Dark Green"],
    key="ui_app_theme",
    horizontal=True,
    on_change=apply_settings
)


st.markdown("---")

st.subheader("2) Tema Line Chart")
st.selectbox(
    "Template Plotly (Line Chart)",
    PLOTLY_TEMPLATES,
    key="ui_line_template",
    on_change=apply_settings
)

st.markdown("---")

st.subheader("3) Tema Peta Dunia")
st.selectbox(
    "Template Plotly (Peta Dunia)",
    PLOTLY_TEMPLATES,
    key="ui_map_template",
    on_change=apply_settings
)

st.markdown("---")

st.subheader("4) Warna Garis Negara")
st.radio(
    "Mode warna",
    ["Fixed", "Random"],
    key="ui_palette_mode",
    horizontal=True,
    on_change=apply_settings
)

st.info("Tip: Setelah mengubah pengaturan, pindah ke page1 untuk melihat hasilnya.")
