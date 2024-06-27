import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.title("Navigation Menu")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Main Menu")
    st.sidebar.markdown("• [Home](app.py)")
    st.sidebar.markdown("• [Upload via Gdrive](pages/user.py)")

    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Admin Options")
        st.sidebar.markdown("• [Upload via SFTP](pages/admin.py)")
        st.sidebar.markdown("• [Magic Prompts](pages/super-admin.py)")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.title("Welcome to Our App!")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Get Started")
    st.sidebar.markdown("• [Log in](app.py)")


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
        st.markdown("Redirecting...")
        st.experimental_rerun()
    menu()


# Example usage
menu_with_redirect()
