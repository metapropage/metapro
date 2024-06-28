import streamlit as st


def authenticated_menu():
    # Define CSS styles
    custom_css = """
    <style>
    .menu-item {
        font-size: 18px;
        font-weight: bold;
        color: #4CAF50;
    }
    .menu-item:hover {
        color: #3E8E41;
    }
    </style>
    """
    # Inject CSS styles
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Show a navigation menu for authenticated users
    st.sidebar.markdown(f'<a class="menu-item" href="app.py">🏠 Home</a>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<a class="menu-item" href="pages/user.py">📂 Upload via Gdrive</a>', unsafe_allow_html=True)
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.markdown(f'<a class="menu-item" href="pages/admin.py">🔑 Upload via SFTP</a>', unsafe_allow_html=True)
        st.sidebar.markdown(f'<a class="menu-item" href="pages/super-admin.py" {"disabled" if st.session_state.role != "super-admin" else ""}>✨ Magic Prompts</a>', unsafe_allow_html=True)


def unauthenticated_menu():
    # Define CSS styles
    custom_css = """
    <style>
    .menu-item {
        font-size: 18px;
        font-weight: bold;
        color: #4CAF50;
    }
    .menu-item:hover {
        color: #3E8E41;
    }
    </style>
    """
    # Inject CSS styles
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Show a navigation menu for unauthenticated users
    st.sidebar.markdown(f'<a class="menu-item" href="app.py">🔒 Log in</a>', unsafe_allow_html=True)


def menu():
    # Determine if a user is logged in or not, then show the correct navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()


# Example usage
if __name__ == "__main__":
    if 'role' not in st.session_state:
        st.session_state.role = None  # Default role for testing

    st.title("Menu Example")
    menu()
