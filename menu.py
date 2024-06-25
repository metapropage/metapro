def authenticated_menu():
    import streamlit as st
    # Show a navigation menu for authenticated users
    st.sidebar.page("Home", "app.py")
    st.sidebar.page("Upload via Gdrive", "pages/Gdrive.py")
    st.sidebar.page("Upload via SFTP (admin)", "pages/admin.py")
    st.sidebar.page("Upload via SFTP (prompts)", "pages/Prompts.py")
