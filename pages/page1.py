import streamlit as st
import pandas as pd
import os
import plotly.express as px
import random
import json
from pathlib import Path

# ==========================================================
# PATH SETTINGS (root/settings.json)
# ==========================================================
SETTINGS_PATH = Path(__file__).resolve().parents[1] / "settings.json"

# ==========================================================
# INIT default theme settings (jaga-jaga kalau session baru)
# ==========================================================
st.session_state.setdefault("app_theme", "Light")
st.session_state.setdefault("line_template", "plotly")
st.session_state.setdefault("map_template", "plotly")
st.session_state.setdefault("palette_mode", "Fixed")
st.session_state.setdefault("palette_fixed", ["#e41a1c", "#ff7f00", "#377eb8", "#4daf4a", "#984ea3"])

# ==========================================================
# HELPERS: save filter ke settings.json (merge-safe)
# ==========================================================
def save_filters_to_settings():
    if SETTINGS_PATH.exists():
        settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    else:
        settings = {}

    settings["filter_countries"] = st.session_state.get("ui_countries", [])
    settings["filter_year_range"] = list(st.session_state.get("ui_year_range", (2000, 2024)))

    SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")

# ==========================================================
# HELPERS: warna garis negara
# ==========================================================
def get_palette(selected_countries):
    fixed = st.session_state["palette_fixed"]
    mode = st.session_state["palette_mode"]

    palette = fixed.copy()
    if mode == "Random":
        rnd = random.Random(42)  # stabil
        rnd.shuffle(palette)

    return {c: palette[i] for i, c in enumerate(selected_countries)}

# ==========================================================
# HELPERS: tema peta (sinkron dengan app_theme)
# ==========================================================
def apply_geo_theme(fig):
    if st.session_state["app_theme"] == "Dark":
        fig.update_geos(
            bgcolor="#0e1117",
            landcolor="#1f2937",
            oceancolor="#0b1220",
            showcountries=True,
            countrycolor="#334155",
            showocean=True,
        )
        fig.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117")

# ==========================================================
# LOAD DATA (Wide -> Long)
# ==========================================================
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "Inflasi.csv")
    csv_path = os.path.normpath(csv_path)

    df = pd.read_csv(csv_path)

    year_cols = [c for c in df.columns if c.isdigit()]

    long_df = df.melt(
        id_vars=["Country Name"],
        value_vars=year_cols,
        var_name="Year",
        value_name="Inflation"
    )

    long_df["Year"] = long_df["Year"].astype(int)
    long_df = long_df.dropna(subset=["Inflation"])

    return long_df

# ✅ data harus dibuat sebelum dipakai
data = load_data()

# ==========================================================
# HEADER
# ==========================================================
st.title("🌍 Inflasi Dunia – CPI (World Bank)")
st.caption(
    "Pilih negara & rentang tahun untuk melihat tren inflasi tahunan "
    "serta highlight negara terpilih pada peta dunia."
)

# ==========================================================
# FILTER UTAMA (PERSIST KE JSON)
# ==========================================================
countries = sorted(data["Country Name"].unique())
min_year = int(data["Year"].min())
max_year = int(data["Year"].max())

default_countries = ["Indonesia"] if "Indonesia" in countries else [countries[0]]
default_year_range = (2000, max_year)

# Ambil filter tersimpan dari session_state (yang di-load dari settings.json via app.py),
# atau fallback ke default.
saved_countries = st.session_state.get("filter_countries") or default_countries
saved_year_range = st.session_state.get("filter_year_range") or default_year_range

# Normalisasi kalau dari JSON berbentuk list -> tuple
if isinstance(saved_year_range, list):
    saved_year_range = (saved_year_range[0], saved_year_range[1])

# Clamp tahun ke batas data
saved_year_range = (max(min_year, saved_year_range[0]), min(max_year, saved_year_range[1]))

# Init UI widget state (sekali saja / jika kosong)
if st.session_state.get("ui_countries") in (None, []):
    st.session_state["ui_countries"] = saved_countries

if st.session_state.get("ui_year_range") is None:
    st.session_state["ui_year_range"] = saved_year_range

# Callback saat filter berubah
def apply_filter_change():
    st.session_state["filter_countries"] = st.session_state["ui_countries"]
    st.session_state["filter_year_range"] = st.session_state["ui_year_range"]
    save_filters_to_settings()

st.multiselect(
    "Pilih hingga 5 negara",
    countries,
    max_selections=5,
    key="ui_countries",
    on_change=apply_filter_change,
)

st.slider(
    "Pilih rentang tahun",
    min_year,
    max_year,
    key="ui_year_range",
    on_change=apply_filter_change,
)

# Tombol reset (setelah filter)
if st.button("🔄 Reset Filter"):
    st.session_state["ui_countries"] = default_countries
    st.session_state["ui_year_range"] = default_year_range
    apply_filter_change()
    st.rerun()

selected_countries = st.session_state["ui_countries"]
year_range = st.session_state["ui_year_range"]

df_filtered = data[
    (data["Country Name"].isin(selected_countries)) &
    (data["Year"].between(*year_range))
].sort_values(["Country Name", "Year"])

# ==========================================================
# KPI SUMMARY
# ==========================================================
st.subheader("📌 Ringkasan Singkat")
cols = st.columns(len(selected_countries))

for col, country in zip(cols, selected_countries):
    sub = df_filtered[df_filtered["Country Name"] == country].sort_values("Year")
    if sub.empty:
        col.metric(label=country, value="–", delta=None)
        continue

    latest = sub.iloc[-1]
    value = f"{latest['Inflation']:.2f}%"

    if len(sub) > 1:
        prev = sub.iloc[-2]
        delta_val = latest["Inflation"] - prev["Inflation"]
        delta = f"{delta_val:+.2f} p.p."
    else:
        delta = None

    col.metric(label=country, value=value, delta=delta)

# ==========================================================
# TABS
# ==========================================================
tab1, tab2, tab3 = st.tabs(["📈 Tren", "🗺️ Peta", "📊 Data"])

# ---------- LINE CHART ----------
with tab1:
    fig = px.line(
        df_filtered,
        x="Year",
        y="Inflation",
        color="Country Name",
        color_discrete_map=get_palette(selected_countries),
        template=st.session_state["line_template"],
        markers=True
    )
    fig.update_layout(legend_title_text="Negara")
    st.plotly_chart(fig, use_container_width=True)

# ---------- MAP ----------
with tab2:
    latest_year = year_range[1]
    df_map = data[data["Year"] == latest_year].copy()

    df_map["Group"] = "Other"
    for c in selected_countries:
        df_map.loc[df_map["Country Name"] == c, "Group"] = c

    # Warna sama seperti line chart
    map_colors = {"Other": "#DDDDDD"}
    map_colors.update(get_palette(selected_countries))

    fig_map = px.choropleth(
        df_map,
        locations="Country Name",
        locationmode="country names",
        color="Group",
        color_discrete_map=map_colors,
        template=st.session_state["map_template"],
        title=f"Highlight negara terpilih (Tahun {latest_year})"
    )

    apply_geo_theme(fig_map)
    fig_map.update_layout(legend_title_text="Negara")
    st.plotly_chart(fig_map, use_container_width=True)

# ---------- DATA ----------
with tab3:
    st.dataframe(df_filtered, use_container_width=True)
