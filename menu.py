import streamlit as st

def display_menu():
    st.sidebar.title("Navigation")

    # Link to Home (app.py)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Main Pages")
    st.sidebar.page_config("app.py", label="Home")
    st.sidebar.page_config("pages/about.py", label="About")

    # Links to User Pages
    st.sidebar.markdown("---")
    st.sidebar.subheader("User Pages")
    st.sidebar.page_config("pages/user.py", label="Upload via Gdrive")
    
    # Links to Admin Pages
    st.sidebar.markdown("---")
    st.sidebar.subheader("Admin Pages")
    st.sidebar.page_config("pages/admin.py", label="Admin Page")
    st.sidebar.page_config("pages/super-admin.py", label="Super Admin Page")
