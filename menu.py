import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.markdown("### Navigation")
    st.sidebar.markdown("- [Home](app.py)")
    st.sidebar.markdown("- [Upload via Gdrive](pages/user.py)")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.markdown("- [Upload via SFTP](pages/admin.py)")
        if st.session_state.role == "super-admin":
            st.sidebar.markdown("- [Magic Prompts](pages/super-admin.py)")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.markdown("### Navigation")
    st.sidebar.markdown("- [Log in](app.py)")

def main():
    # Determine if a user is logged in or not, then show the correct menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
    else:
        authenticated_menu()

if __name__ == "__main__":
    main()
