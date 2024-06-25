import streamlit as st
from menu import authenticated_menu

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.experimental_rerun("app.py")
    else:
        authenticated_menu()

if __name__ == "__main__":
    menu_with_redirect()
