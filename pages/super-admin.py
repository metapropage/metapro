import streamlit as st
import os
import tempfile
from PIL import Image
import google.generativeai as genai
import time
import traceback
import re
import unicodedata
from datetime import datetime, timedelta
import pytz
import json
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

# Function to normalize and clean text
def normalize_text(text):
    normalized = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return normalized

# Function to generate detailed description for images using AI model
def generate_description(model, img):
    description = model.generate_content(["Create two effective prompts in detailed based on the photo in SEO terms to make it easier for buyers to find this image on the microstock site, and create 49 keywords (MUST 1 word each keyword, separated by commas, no numbers) that are appropriate and relevant to the title"])
    return description.text.strip()

def main():
    """Main function for the Streamlit app."""

    # Add elements to the sidebar
    st.sidebar.title("Sidebar Title")
    st.sidebar.write("Sidebar content goes here")

    # Display WhatsApp chat link
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://wa.me/6285328007533" target="_blank">
            <button style="background-color: #1976d2; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                MetaPro
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Check if license has already been validated
    license_file = "license.txt"
    if not st.session_state['license_validated']:
        if os.path.exists(license_file):
            with open(license_file, 'r') as file:
                start_date_str = file.read().strip()
                start_date = datetime.fromisoformat(start_date_str)
                st.session_state['license_validated'] = True
        else:
            # License key input
            validation_key = st.text_input('License Key', type='password')

    # Check if validation key is correct
    correct_key = "dian12345"

    if not st.session_state['license_validated'] and validation_key:
        if validation_key == correct_key:
            st.session_state['license_validated'] = True
            start_date = datetime.now(JAKARTA_TZ)
            with open(license_file, 'w') as file:
                file.write(start_date.isoformat())
        else:
            st.error("Invalid validation key. Please enter the correct key.")

    if st.session_state['license_validated']:
        # Check the license file for the start date
        with open(license_file, 'r') as file:
            start_date_str = file.read().strip()
            start_date = datetime.fromisoformat(start_date_str)

        # Calculate the expiration date
        expiration_date = start_date + timedelta(days=31)
        current_date = datetime.now(JAKARTA_TZ)

        if current_date > expiration_date:
            st.error("Your license has expired. Please contact support for a new license key.")
            return
        else:
            days_remaining = (expiration_date - current_date).days
            st.success(f"License valid. You have {days_remaining} days remaining.")

        # API Key input
        api_key = st.text_input('Enter your API Key', value=st.session_state['api_key'] or '')

        # Save API key in session state
        if api_key:
            st.session_state['api_key'] = api_key

        # Upload image files
        uploaded_files = st.file_uploader('Upload Images (Only JPG and JPEG supported)', accept_multiple_files=True)

        if uploaded_files:
            valid_files = [file for file in uploaded_files if file.type in ['image/jpeg', 'image/jpg']]
            invalid_files = [file for file in uploaded_files if file not in valid_files]

            if invalid_files:
                st.error("Only JPG and JPEG files are supported.")

            if valid_files and st.button("Process"):
                with st.spinner("Processing..."):
                    try:
                        # Check and update upload count for the current date
                        if st.session_state['upload_count']['date'] != current_date.date():
                            st.session_state['upload_count'] = {
                                'date': current_date.date(),
                                'count': 0
                            }
                        
                        # Check if remaining uploads are available
                        if st.session_state['upload_count']['count'] + len(valid_files) > 1000:
                            remaining_uploads = 1000 - st.session_state['upload_count']['count']
                            st.warning(f"You have exceeded the upload limit. Remaining uploads for today: {remaining_uploads}")
                            return
                        else:
                            st.session_state['upload_count']['count'] += len(valid_files)
                            st.success(f"Uploads successful. Remaining uploads for today: {1000 - st.session_state['upload_count']['count']}")

                        genai.configure(api_key=api_key)  # Configure AI model with API key
                        model = genai.GenerativeModel('gemini-pro-vision')

                        # Create a temporary directory to store the uploaded images
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Save the uploaded images to the temporary directory
                            image_paths = []
                            for file in valid_files:
                                temp_image_path = os.path.join(temp_dir, file.name)
                                with open(temp_image_path, 'wb') as f:
                                    f.write(file.read())
                                image_paths.append(temp_image_path)

                            # Generate and display MidJourney prompt texts and thumbnails
                            st.markdown("## Generated MidJourney Prompts")
                            for image_path in image_paths:
                                img = Image.open(image_path)
                                description = generate_description(model, img)

                                # Display thumbnail
                                img.thumbnail((150, 150))
                                st.image(img)

                                # Display prompt text
                                st.markdown(f"**MidJourney Prompt:** {description}")

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.error(traceback.format_exc())  # Print detailed error traceback for debugging

if __name__ == '__main__':
    main()
