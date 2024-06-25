import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/Gdrive.py", label="Upload via Gdrive")
    st.sidebar.page_link("pages/admin.py", label="Upload via SFTP")
    st.sidebar.page_link("pages/Prompts.py", label="Upload via SFTP")
        )


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()
