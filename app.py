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
    """, unsafe_allow_html=True)

# Predefined username and password (for demonstration purposes)
USERNAME = "a"
PASSWORD = "a"

# Initialize st.session_state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

if "rerun" not in st.session_state:
    st.session_state.rerun = False

# Authentication function
def authenticate(username, password):
    if username == USERNAME and password == PASSWORD:
        st.session_state.authenticated = True
        st.session_state.role = "super-admin"  # Directly set the role to "super-admin"
        set_lock("logged_in")
        st.session_state.rerun = True
    else:
        st.error("Incorrect username or password")

# Function to check the lock file
def check_lock():
    lock_file = "lock.txt"
    if os.path.exists(lock_file):
        with open(lock_file, 'r') as file:
            status = file.read()
        return status == "logged_in"
    return False

# Function to set lock file
def set_lock(status):
    lock_file = "lock.txt"
    with open(lock_file, 'w') as file:
        file.write(status)

    menu()  # Render the dynamic menu

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        set_lock("")
        st.success("Logged out successfully.")

    
