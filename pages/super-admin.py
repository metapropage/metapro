import streamlit as st

# Configure the page with sidebar initially opened
st.set_page_config(
    page_title="Meta Pro",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",  # This ensures the sidebar is open by default
)

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/user.py", label="Upload via Gdrive", icon="📂")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Upload via SFTP", icon="🔑")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Magic Prompts",
            disabled=st.session_state.role != "super-admin",
            icon="✨"
        )

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in", icon="🔒")

def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()

# Initialize the menu
menu_with_redirect()
