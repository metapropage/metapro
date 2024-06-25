import streamlit as st
import os

# Assuming the menu function is defined in a module named 'menu'
from menu import menu

# Apply custom styling
st.markdown("""
    <style>
        #MainMenu, header, footer {
            visibility: hidden;
        }
        section[data-testid="stSidebar"] div:first-child {
            top: 0;
            height: 100vh;
        }
    </style>
    """, unsafe_allow_html=True)

st.set_option("client.showSidebarNavigation", False)

# Predefined username and password (for demonstration purposes)
USERNAME = "admin"
PASSWORD = "dian"

# Initialize st.session_state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

# Authentication function
def authenticate(username, password):
    if username == USERNAME and password == PASSWORD:
        st.session_state.authenticated = True
        set_lock("logged_in")
    else:
        st.error("Incorrect username or password")

# Function to check the lock file
def check_lock():
    lock_file = "lock.txt"
    if os.path.exists(lock_file):
        with open(lock_file, 'r') as file:
            status = file.read()
        return status == "logged_in"
    return False

# Function to set lock file
def set_lock(status):
    lock_file = "lock.txt"
    with open(lock_file, 'w') as file:
        file.write(status)

# If the user is not authenticated, show the login form
if not st.session_state.authenticated:
    st.title("Login")
    if check_lock():
        st.error("Another user is currently logged in. Please try again later.")
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            authenticate(username, password)

# If authenticated, show the role selection and menu
if st.session_state.authenticated:
    # Retrieve the role from Session State to initialize the widget
    st.session_state._role = st.session_state.role

    def set_role():
        # Callback function to save the role selection to Session State
        st.session_state.role = st.session_state._role

    # Selectbox to choose role
    st.selectbox(
        "Select your role:",
        ["super-admin"],
        key="_role",
        on_change=set_role,
    )

    menu()  # Render the dynamic menu

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        set_lock("")
        st.success("Logged out successfully.")

    # Additional Information
    st.markdown("### Why Choose MetaPro?")
    st.markdown("""
    **AI-Powered Precision:** Leverage the power of Google Generative AI to automatically generate highly relevant and descriptive titles and tags for your images. Enhance your image metadata with unprecedented accuracy and relevance.

    **Streamlined Workflow:** Upload your images in just a few clicks. Our app processes each photo, embeds the generated metadata, and prepares it for upload—automatically and effortlessly.

    **Secure and Efficient Gdrive Upload:** Once processed, your images are securely uploaded to Google Drive. Keep your workflow smooth and your data safe with our robust upload system.

    **How It Works:**
    1. **Upload Your Images:** Drag and drop your JPG/JPEG files into the uploader.
    2. **Generate Metadata:** Watch as the app uses AI to create descriptive titles and relevant tags.
    3. **Embed Metadata:** The app embeds the metadata directly into your images.
    4. **Directly upload to Google Drive for faster downloads.**

    **Subscribe Now and Experience the Difference:**
    - **MetaPro Basic Plan:** $10 for 3 months – Upload up to 1,000 images daily.
    - **MetaPro Premium Plan:** $40 for unlimited image uploads for a lifetime.

    Ready to revolutionize your workflow? Subscribe today and take the first step towards a smarter, more efficient image management solution.
    """)
