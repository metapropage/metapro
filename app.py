import streamlit as st
import os
from datetime import datetime, timedelta

# Assuming the menu function is defined in a module named 'menu'
from menu import menu

# Apply custom styling
st.markdown("""
    <style>
        #MainMenu, header, footer {
            visibility: hidden;
        }
        section[data-testid="stSidebar"] {
            top: 0;
            height: 100vh;
        }
    </style>
    """, unsafe_allow_html=True)

# Predefined username and password (for demonstration purposes)
USERNAME = "admin"
PASSWORD = "dian"

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
        set_lock(username)
        st.session_state.rerun = True
    else:
        st.error("Incorrect username or password")

# Function to check the lock file
def check_lock(username):
    lock_file = "lock.txt"
    if os.path.exists(lock_file):
        with open(lock_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                user, timestamp = line.strip().split(',')
                timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                if user == username and datetime.now() - timestamp <= timedelta(days=30):
                    return True
            # Remove entries older than 30 days
            lines = [line for line in lines if datetime.now() - datetime.strptime(line.strip().split(',')[1], '%Y-%m-%d %H:%M:%S') <= timedelta(days=30)]
            with open(lock_file, 'w') as file:
                file.writelines(lines)
    return False

# Function to set lock file
def set_lock(username):
    lock_file = "lock.txt"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(lock_file, 'a') as file:
        file.write(f"{username},{timestamp}\n")

# If the user is not authenticated, show the login form
if not st.session_state.authenticated:
    st.title("Login")
    if check_lock(USERNAME):
        st.error("You have been locked out due to a previous login. Please try again later.")
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            authenticate(username, password)

# If authenticated, show the menu and additional information
if st.session_state.authenticated:
    if st.session_state.rerun:
        st.session_state.rerun = False
        st.experimental_rerun()

    menu()  # Render the dynamic menu

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        # Remove the user's lock
        with open("lock.txt", 'r') as file:
            lines = file.readlines()
        with open("lock.txt", 'w') as file:
            for line in lines:
                if not line.startswith(USERNAME):
                    file.write(line)
        st.success("Logged out successfully.")

    # Additional Information
    st.markdown("### Why Choose MetaPro?")
    st.markdown("""
    **AI-Powered Precision:** Leverage the power of Google Generative AI to automatically...
    """)
