import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.title("Navigation Menu")
    st.sidebar.page_link("app.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/user.py", label="Upload via Gdrive", icon="🌐")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Upload via SFTP", icon="🚀")
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

    # Display WhatsApp chat link
    st.sidebar.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://wa.me/6282265298845" target="_blank">
            <button style="background-color: #1976d2; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                MetaPro
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Call the menu_with_redirect function to display the menu and redirect if needed
menu_with_redirect()
