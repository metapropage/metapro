import streamlit as st
from pages import admin, super_admin, user

def main():
    st.sidebar.title("Navigation")
    menu = ["User", "Admin", "Super Admin"]
    choice = st.sidebar.selectbox("Go to", menu)

    if choice == "User":
        user.app()
    elif choice == "Admin":
        admin.app()
    elif choice == "Super Admin":
        super_admin.app()

if __name__ == '__main__':
    main()
