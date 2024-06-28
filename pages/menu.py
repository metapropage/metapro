import streamlit as st

def menu_with_redirect():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.write("You are not logged in. Redirecting to login page...")
        st.stop()  # Stop further execution if not logged in

    st.sidebar.title("Menu")
    st.sidebar.button("Home")
    st.sidebar.button("Profile")
