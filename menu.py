import streamlit as st
from pages import admin, super_admin, user

def display_menu():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Admin", "Super Admin", "User"])

    if page == "Admin":
        admin.display()
    elif page == "Super Admin":
        super_admin.display()
    elif page == "User":
        user.display()

def main():
    st.title("Main App")
    display_menu()

if __name__ == "__main__":
    main()
