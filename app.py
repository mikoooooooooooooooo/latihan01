import streamlit as st

pages=[
    st.Page(page="pages/page1.py",title="1",icon="🏚️"),
    st.Page(page="pages/page2.py",title="2",icon="🫂"),
    st.Page(page="pages/page3.py",title="3",icon="☂️"),
    st.Page(page="pages/page4.py",title="4",icon="☂️"),
]

pg=st.navigation(
    pages,
    position="sidebar",
    expanded=True
)

pg.run()