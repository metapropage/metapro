import streamlit as st
from menu import menu

# Hide the sidebar navigation
st.set_option("client.showSidebarNavigation", False)

# Initialize session state variables
if "role" not in st.session_state:
    st.session_state.role = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    """Login function to authenticate user."""
    username = st.session_state.username
    password = st.session_state.password
    
    # Replace the following lines with your authentication logic
    if username == "admin" and password == "password":  # Simple authentication logic for demo purposes
        st.session_state.logged_in = True
    else:
        st.error("Invalid username or password")

# Login form
if not st.session_state.logged_in:
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    st.button("Login", on_click=login)
else:
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
    
    # Render the dynamic menu
    menu()
