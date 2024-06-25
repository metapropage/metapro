import streamlit as st
from menu import menu

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
    else:
        st.error("Incorrect username or password")

# If the user is not authenticated, show the login form
if not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        authenticate(username, password)

# If authenticated, show the role selection and menu
if st.session_state.authenticated:
    st.title("Welcome!")
    
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
    
    # Apply custom styling
    st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        section[data-testid="stSidebar"] div:first-child {top: 0; height: 100vh;}
    </style>
    """, unsafe_allow_html=True)
