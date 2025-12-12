import streamlit as st

pages=[
    st.Page(page="pages/page1.py",title="Inflasi Dunia",icon="🌍"),
    st.Page(page="pages/page2.py",title="Pengaturan",icon="🫂"),
    st.Page(page="pages/page3.py",title="Tentang",icon="☂️"),
  ]

pg=st.navigation(
    pages,
    position="sidebar",
    expanded=True
)

pg.run()