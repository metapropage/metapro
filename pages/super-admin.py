import streamlit as st
import os
import tempfile
from PIL import Image
import google.generativeai as genai
import traceback
import pytz
from datetime import datetime, timedelta
from menu import menu_with_redirect

st.set_option("client.showSidebarNavigation", False)

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

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

# Set the timezone to UTC+7 Jakarta
JAKARTA_TZ = pytz.timezone('Asia/Jakarta')

# Initialize session state for license validation
if 'license_validated' not in st.session_state:
    st.session_state['license_validated'] = False

if 'upload_count' not in st.session_state:
    st.session_state['upload_count'] = {
        'date': None,
        'count': 0
    }

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None

# Function to validate the API key and set up the Generative AI client
def validate_api_key(api_key):
    try:
        genai.init(api_key=api_key)
        st.session_state['api_key'] = api_key
        st.success("API key validated successfully!")
    except Exception as e:
        st.error("Invalid API key. Please try again.")
        st.session_state['api_key'] = None

# Sidebar for API key input
with st.sidebar:
    st.header("API Key")
    api_key = st.text_input("Enter your Google Generative AI API key", type="password")
    if st.button("Validate"):
        validate_api_key(api_key)

# Main content
st.title("Image Upload and Prompt Generation")

if st.session_state['api_key']:
    uploaded_file = st.file_uploader("Choose an image file (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Save the uploaded file to a temporary directory
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            
            # Open the image file
            image = Image.open(tmp_file_path)
            st.image(image, caption='Uploaded Image', use_column_width=True)

            # Generate text-to-image prompts using Generative AI
            prompts = genai.generate_prompts(
                description="I want to create text-to-image prompts using MidJourney. The prompts must be able to produce images exactly like this one. Please create 10 such prompts.",
                image=image
            )
            
            st.write("Generated Prompts:")
            for i, prompt in enumerate(prompts, start=1):
                st.write(f"{i}. {prompt}")

        except Exception as e:
            st.error("An error occurred while processing the image.")
            st.error(traceback.format_exc())
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
else:
    st.warning("Please enter and validate your API key to use the app.")
