import streamlit as st
from menu import menu

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page("Home", "app.py")
    st.sidebar.page("Upload via Gdrive", "pages/Gdrive.py")
    st.sidebar.page("Upload via SFTP (admin)", "pages/admin.py")
    st.sidebar.page("Upload via SFTP (prompts)", "pages/Prompts.py")

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.experimental_rerun("app.py")
    else:
        authenticated_menu()
