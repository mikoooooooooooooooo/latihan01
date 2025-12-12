import streamlit as st

# ==========================================================
# PAGE 3 — TENTANG
# ==========================================================

st.title("ℹ️ Tentang Aplikasi")

# ==========================================================
# 1) DESKRIPSI TUGAS
# ==========================================================
st.subheader("1) Deskripsi Tugas")
st.write(
    """
    **Tugas Individu – Latihan Aplikasi Streamlit**

    Aplikasi ini dibuat sebagai latihan pengembangan dashboard interaktif menggunakan **Streamlit**.
    Fokus utama aplikasi adalah menampilkan visualisasi data inflasi dunia berbasis CPI (Consumer Price Index)
    dengan fitur filter, grafik, serta peta dunia.
    """
)

st.markdown("---")

# ==========================================================
# 2) IDENTITAS MAHASISWA
# ==========================================================
st.subheader("2) Identitas Mahasiswa")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Nama:**")
    st.write("Muhammad Hery Prasetyo Wahyu Jatmiko")  

with col2:
    st.write("**NIM:**")
    st.write("021002414003") 

with col3:
    st.write("**Kelas:**")
    st.write("Praktikum Analisa Big Data Ekonomika")

st.markdown("---")

# ==========================================================
# 3) DESKRIPSI INFLASI DUNIA (CPI)
# ==========================================================
st.subheader("3) Deskripsi Inflasi Dunia (CPI)")

st.write(
    """
    **Inflasi** adalah kenaikan tingkat harga barang dan jasa secara umum dan terus-menerus dalam periode tertentu.
    Salah satu indikator inflasi yang sering digunakan secara internasional adalah **CPI (Consumer Price Index)**,
    yaitu indeks yang mengukur perubahan rata-rata harga dari “keranjang” barang dan jasa yang dikonsumsi rumah tangga.

    Dalam aplikasi ini, data CPI digunakan untuk menampilkan **inflasi tahunan (% per tahun)** pada berbagai negara,
    sehingga pengguna dapat:
    - membandingkan tren inflasi antar negara,
    - melihat perubahan inflasi dari waktu ke waktu,
    - dan memvisualisasikan negara terpilih pada peta dunia.
    """
)

st.caption("Sumber data: World Bank (indikator inflasi berbasis CPI).")
