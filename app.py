import streamlit as st
import os

# Assuming the menu function is defined in a module named 'menu'
from menu import menu

st.set_option("client.showSidebarNavigation", False)

# Predefined username and password (for demonstration purposes)
USERNAME = "admin"
PASSWORD = "dian"

# Initialize st.session_state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

# Authentication function
def authenticate(username, password):
    if username == USERNAME and password == PASSWORD:
        st.session_state.authenticated = True
        set_lock("logged_in")
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

# If the user is not authenticated, show the login form
if not st.session_state.authenticated:
    st.title("Login")
    if check_lock():
        st.error("Another user is currently logged in. Please try again later.")
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            authenticate(username, password)

# If authenticated, show the role selection and menu
if st.session_state.authenticated:
    # Retrieve the role from Session State to initialize the widget
    st.session_state._role = st.session_state.role

    def set_role():
        # Callback function to save the role selection to Session State
        st.session_state.role = st.session_state._role

    # Selectbox to choose role
    st.selectbox(
        "Select your role:",
        ["super-admin"],
        key="_role",
        on_change=set_role,
    )

    menu()  # Render the dynamic menu

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        set_lock("")
        st.success("Logged out successfully.")
