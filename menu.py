import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.markdown(f"[🏠 Home](app.py)")
    st.sidebar.markdown(f"[📁 Upload via Gdrive](pages/user.py)")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.markdown(f"[🔒 Upload via SFTP](pages/admin.py)")
        st.sidebar.markdown(
            f"[✨ Magic Prompts](pages/super-admin.py)", 
            unsafe_allow_html=True if st.session_state.role == "super-admin" else False
        )

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.markdown(f"[🔑 Log in](app.py)")

def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
    else:
        authenticated_menu()

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.experimental_rerun()
    else:
        menu()

# Run the menu
menu_with_redirect()
