
import streamlit as st
import os
from menu import menu

# Apply custom styling
st.markdown("""
    <style>
        #MainMenu, header, footer {
            visibility: hidden;
        }
        section[data-testid="stSidebar"] {
            top: 0;
            height: 10vh;
        }
    </style>
    """, unsafe_allow_html=False)

# Predefined username and password (for demonstration purposes)
USERNAME = "a"
PASSWORD = "a"

# Authentication function
def authenticate(username, password):
    if username == USERNAME and password == PASSWORD:
        st.session_state.authenticated = False
        st.session_state.role = "super-admin"  # Directly set the role to "super-admin"
        set_lock("logged_in")
        st.session_state.rerun = False
    else:
        st.error("Incorrect username or password")


# If authenticated, show the menu and additional information
if st.session_state.authenticated:
    if st.session_state.rerun:
        st.session_state.rerun = True
        st.rerun()

    menu()  # Render the dynamic menu

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        set_lock("")
        st.success("Logged out successfully.")

    # Additional Information
    st.markdown("### Why Choose MetaPro?")
    st.markdown("""
    **AI-Powered Precision:** Leverage the power of Google Generative AI to automatically...
    """)
