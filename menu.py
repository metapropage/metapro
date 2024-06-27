import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users with styling
    st.sidebar.markdown("<h2 style='color: blue;'>Navigation Menu</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: darkgreen;'>User Options</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='app.py' style='display: block; color: black; padding: 10px;'>Home</a>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='pages/user.py' style='display: block; color: black; padding: 10px;'>Upload via Gdrive</a>", unsafe_allow_html=True)
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.markdown("<h3 style='color: darkred;'>Admin Options</h3>", unsafe_allow_html=True)
        st.sidebar.markdown("<a href='pages/admin.py' style='display: block; color: black; padding: 10px;'>Upload via SFTP</a>", unsafe_allow_html=True)
        st.sidebar.markdown("<a href='pages/super-admin.py' style='display: block; color: black; padding: 10px;'>Magic Prompts</a>", unsafe_allow_html=True)

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users with styling
    st.sidebar.markdown("<h2 style='color: blue;'>Navigation Menu</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("<a href='app.py' style='display: block; color: black; padding: 10px;'>Log in</a>", unsafe_allow_html=True)

def menu():
    # Determine if a user is logged in or not, then show the correct navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
    else:
        authenticated_menu()

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.warning("You are not logged in. Redirecting to login page...")
        st.experimental_rerun()
    else:
        menu()
