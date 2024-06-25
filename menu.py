import streamlit as st

def display_menu():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Admin", "Super Admin", "User"])

    if page == "Admin":
        import pages.admin as admin
        admin.display()
    elif page == "Super Admin":
        import pages.super_admin as super_admin
        super_admin.display()
    elif page == "User":
        import pages.user as user
        user.display()
