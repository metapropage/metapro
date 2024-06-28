import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.title("Navigation Menu")
    st.sidebar.page_link("app.py", label="Home", icon="🏠")
    st.sidebar.empty()  # Adding space
    st.sidebar.page_link("pages/user.py", label="Upload via Gdrive", icon="🌐")
    st.sidebar.empty()  # Adding space
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Upload via SFTP", icon="🚀")
        st.sidebar.empty()  # Adding space
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Magic Prompts",
            disabled=st.session_state.role != "super-admin",
            icon="✨"
        )

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.title("Navigation Menu")
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

    # Adding space before the logout button
    st.sidebar.empty()  # Adding space
    st.sidebar.empty()  # Adding more space
    st.sidebar.empty()  # Adding more space
    st.sidebar.empty()  # Adding more space

    # Logout button in the sidebar with a unique key
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.success("Logged out successfully.")

# Call the menu_with_redirect function to display the menu and redirect if needed
menu_with_redirect()
