import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ======================
# LOAD & RAPIHKAN DATA
# ======================
@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, "..", "data", "Inflasi.csv")
    csv_path = os.path.normpath(csv_path)

    df = pd.read_csv(csv_path)

    # kolom tahun = semua kolom yang namanya angka
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

data = load_data()

# ======================
# HEADER & DESKRIPSI
# ======================
st.title("🌍 Inflasi Dunia – CPI (World Bank)")

st.caption(
    "Pilih beberapa negara dan rentang tahun untuk melihat tren inflasi tahunan "
    "serta posisi masing-masing negara pada peta dunia."
)

# ======================
# FILTER NEGARA & TAHUN
# ======================
all_countries = sorted(data["Country Name"].unique())
default_country = "Indonesia" if "Indonesia" in all_countries else all_countries[0]

selected_countries = st.multiselect(
    "Pilih sampai 5 negara",
    all_countries,
    default=[default_country],
    max_selections=5,
)

if len(selected_countries) == 0:
    st.info("Silakan pilih minimal 1 negara.")
    st.stop()

min_year = int(data["Year"].min())
max_year = int(data["Year"].max())

year_range = st.slider(
    "Pilih rentang tahun",
    min_year,
    max_year,
    (2000, max_year),
    step=1,
)

mask_country = data["Country Name"].isin(selected_countries)
mask_year = data["Year"].between(year_range[0], year_range[1])
df_filtered = data[mask_country & mask_year].sort_values(["Country Name", "Year"])

# ======================
# WARNA UNTUK TIAP NEGARA
# ======================
palette = ["#e41a1c", "#ff7f00", "#377eb8", "#4daf4a", "#984ea3"]  # 5 warna beda

color_map = {
    country: palette[i]
    for i, country in enumerate(selected_countries)
}

# ======================
# KPI CARDS (st.metric)
# ======================
st.subheader("📌 Ringkasan Singkat")

cols = st.columns(len(selected_countries))

for col, country in zip(cols, selected_countries):
    sub = df_filtered[df_filtered["Country Name"] == country].sort_values("Year")
    if sub.empty:
        value = "–"
        delta = None
    else:
        latest = sub.iloc[-1]
        value = f"{latest['Inflation']:.2f}%"

        # bandingkan dengan tahun sebelumnya (kalau ada)
        if len(sub) >= 2:
            prev = sub.iloc[-2]
            diff = latest["Inflation"] - prev["Inflation"]
            delta = f"{diff:+.2f} p.p."
        else:
            delta = None

    col.metric(
        label=country,
        value=value,
        delta=delta
    )

st.markdown("---")

# ======================
# TABS: LINE, MAP, DATA
# ======================
tab_line, tab_map, tab_data = st.tabs(
    ["📈 Tren Waktu", "🗺️ Peta Dunia", "📊 Data Terfilter"]
)

# ---------- TAB 1: LINE CHART ----------
with tab_line:
    st.subheader("Tren inflasi per negara")

    if df_filtered.empty:
        st.warning("Tidak ada data untuk kombinasi negara & rentang tahun ini.")
    else:
        fig_line = px.line(
            df_filtered,
            x="Year",
            y="Inflation",
            color="Country Name",
            markers=True,
            color_discrete_map=color_map,
            labels={
                "Year": "Tahun",
                "Inflation": "Inflasi (% per tahun)",
                "Country Name": "Negara",
            },
            title=f"Inflasi tahunan ({year_range[0]}–{year_range[1]})",
        )
        fig_line.update_layout(legend_title_text="Negara")
        st.plotly_chart(fig_line, use_container_width=True)

# ---------- TAB 2: MAP ----------
with tab_map:
    st.subheader("Peta dunia – negara terpilih")

    year_for_map = year_range[1]  # pakai tahun terakhir di slider
    df_map = data[data["Year"] == year_for_map].copy()

    df_map["color_group"] = "Other"
    for c in selected_countries:
        df_map.loc[df_map["Country Name"] == c, "color_group"] = c

    map_color_map = {"Other": "#DDDDDD"}
    map_color_map.update(color_map)

    fig_map = px.choropleth(
        df_map,
        locations="Country Name",
        locationmode="country names",
        color="color_group",
        color_discrete_map=map_color_map,
        hover_name="Country Name",
        projection="natural earth",
        title=f"Highlight negara terpilih pada tahun {year_for_map}",
    )

    fig_map.update_layout(legend_title_text="Negara")
    st.plotly_chart(fig_map, use_container_width=True)

# ---------- TAB 3: DATA ----------
with tab_data:
    st.subheader("Data inflasi terfilter")

    st.caption(
        "Tabel di bawah hanya berisi negara & rentang tahun yang saat ini dipilih. "
        "Dapat diunduh untuk analisis lanjutan."
    )

    st.dataframe(df_filtered, use_container_width=True)

    # siapkan CSV untuk diunduh
    csv_out = df_filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="💾 Download data terfilter (CSV)",
        data=csv_out,
        file_name="inflasi_terfilter.csv",
        mime="text/csv",
    )
