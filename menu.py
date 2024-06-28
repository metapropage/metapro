import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.title("Navigation Menu")
    if st.sidebar.button("Home", key="home_button"):
        st.experimental_set_query_params(page="app.py")
    if st.sidebar.button("Upload via Gdrive", key="gdrive_button"):
        st.experimental_set_query_params(page="pages/user.py")
    if st.session_state.role in ["admin", "super-admin"]:
        if st.sidebar.button("Upload via SFTP", key="sftp_button"):
            st.experimental_set_query_params(page="pages/admin.py")
        if st.session_state.role == "super-admin":
            if st.sidebar.button("Magic Prompts", key="magic_prompts_button"):
                st.experimental_set_query_params(page="pages/super-admin.py")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.title("Navigation Menu")
    if st.sidebar.button("Log in", key="login_button"):
        st.experimental_set_query_params(page="app.py")

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
        st.experimental_set_query_params(page="app.py")
    menu()

    # Logout button in the sidebar with a unique key
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.success("Logged out successfully.")

# Call the menu_with_redirect function to display the menu and redirect if needed
menu_with_redirect()
