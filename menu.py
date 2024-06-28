import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.markdown('[🏠 Home](app.py)')
    st.sidebar.markdown('[📂 Upload via Gdrive](pages/user.py)')
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.markdown('[🔑 Upload via SFTP](pages/admin.py)')
        st.sidebar.markdown(
            '[✨ Magic Prompts](pages/super-admin.py)' if st.session_state.role == "super-admin" else '<span style="color:gray;">✨ Magic Prompts (super-admin only)</span>',
            unsafe_allow_html=True
        )
    # Add Telegram group link
    st.sidebar.markdown('[Join our Telegram group](https://t.me/joinchat/your_group_link)')


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.markdown('[🔒 Log in](app.py)')
    # Add Telegram group link
    st.sidebar.markdown('[Join our Telegram group](https://t.me/joinchat/your_group_link)')


def menu():
    # Determine if a user is logged in or not, then show the correct navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.experimental_rerun()
        st.sidebar.markdown('[Join our Telegram group](https://t.me/+hzLj9ZafjQdkYjBl)')
    menu()


# Example usage of the menu functions
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Your App Title")
    menu_with_redirect()
    st.write("Main content goes here.")
