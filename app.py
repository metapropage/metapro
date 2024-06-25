import streamlit as st
from streamlit import session_state as session

# Function to handle login
def login():
    st.session_state['logged_in'] = True

# Function to handle logout
def logout():
    st.session_state['logged_in'] = False

# Login form
def login_form():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Simple check, replace with actual authentication
        if username == "admin" and password == "password":
            login()
        else:
            st.error("Invalid username or password")

# Main app
def main():
    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_form()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Go to", ["User Page", "Admin Page", "Super Admin Page"])

        if st.sidebar.button("Logout"):
            logout()

        if page == "User Page":
            st.write("User Page Content")
            exec(open("pages/user.py").read())
        elif page == "Admin Page":
            st.write("Admin Page Content")
            exec(open("pages/admin.py").read())
        elif page == "Super Admin Page":
            st.write("Super Admin Page Content")
            exec(open("pages/super-admin.py").read())

if __name__ == "__main__":
    main()
