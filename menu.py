import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users in the main page content
    st.write("[Home](app.py)")
    st.write("[Upload via Gdrive](pages/user.py)")
    if st.session_state.role in ["admin", "super-admin"]:
        st.write("[Upload via SFTP](pages/admin.py)")
        st.write(
            "[Describe Midjourney Prompts](pages/super-admin.py)",
            disabled=st.session_state.role != "super-admin",
        )

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users in the main page content
    st.write("[Log in](app.py)")

def menu():
    # Determine if a user is logged in or not, then show the correct navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
    else:
        authenticated_menu()

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.write("Redirecting to [Log in](app.py)...")
    else:
        menu()

# Sample application usage
# Ensure the script only runs when executed as the main module
if __name__ == "__main__":
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

        menu()
