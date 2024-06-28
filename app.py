import streamlit as st

# Assuming the menu function is defined in a module named 'menu'
from menu import menu

# Apply custom styling
st.markdown("""
    <style>
        #MainMenu, header, footer {
            visibility: hidden;
        }
        section[data-testid="stSidebar"] {
            top: 0;
            height: 10vh;
        }
    </style>
    """, unsafe_allow_html=True)

# Predefined username and password (for demonstration purposes)
USERNAME = "admin"
PASSWORD = "dian"

# Initialize st.session_state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

if "rerun" not in st.session_state:
    st.session_state.rerun = False

# Authentication function
def authenticate(username, password):
    if username == USERNAME and password == PASSWORD:
        st.session_state.authenticated = True
        st.session_state.role = "super-admin"  # Directly set the role to "super-admin"
        st.session_state.rerun = True
    else:
        st.error("Incorrect username or password")

# If the user is not authenticated, show the login form
if not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        authenticate(username, password)

# If authenticated, show the menu and additional information
if st.session_state.authenticated:
    if st.session_state.rerun:
        st.session_state.rerun = False
        st.rerun()

    menu()  # Render the dynamic menu

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.success("Logged out successfully.")

    # Additional Information
    st.markdown("### Why Choose MetaPro?")
    st.markdown("""

    **Affordable: Low cost but high quality, always number one.

    **Website-based: Easy to use and compatible with any operating system: Windows, macOS, Linux, and Android.
    
    **AI-Powered Precision:** Generate highly relevant and descriptive titles and tags for your images with unprecedented accuracy and relevance.
    
    **Streamlined Workflow:** Upload your images in just a few clicks. Our app processes each photo, embeds the generated metadata, and prepares it for upload automatically and effortlessly.

    **Magic Prompts:** Generate Custom Prompts from Your Images and Create Similar Prompts with Ease! Download the Generated Prompts and Similar Prompts as Excel Files.

    *How It Works:
    1. Upload Your Images: Drag and drop your JPG/JPEG files into the uploader.
    2. Generate Metadata: Watch as the app uses AI to create descriptive titles and relevant tags.
    3. Embed Metadata: The app embeds the metadata directly into your images.
    4. Securely Download with Embedded Metadata Directly to Your Private Google Drive Account for Faster Access.
    4. Effortlessly and Quickly Send Images Embedded with Metadata via SFTP.
    5. Magic Prompts: Generate Custom Prompts from Your Images and Create Similar Prompts with Ease
    
    **Subscribe Now and Experience the Difference:**
    
    - Upgrade to the MetaPro Plan for just $10 for a 3-month one-time payment!
    
    - Upgrade to the MetaPro Plan for just $35 for a lifetimes one-time payment!
    
    **Enjoy these benefits:**
    
      **✓.** Unlimited Upload
      
      **✓.** Private Website Link

      **✓.** Private Google Drive Account
      
      **✓.** Unlock All Features
      
      **✓.** Free Daily Website Updates

      **✓.** Customizable: Manually generate titles and tags with your own commands
    
    **Ready to revolutionize your workflow? Subscribe today and take the first step towards a smarter, more efficient image management solution.**

    """)
