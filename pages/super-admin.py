import streamlit as st
import os
import tempfile
from PIL import Image
import google.generativeai as genai  # Ensure this is the correct module
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

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None

if 'upload_count' not in st.session_state:
    st.session_state['upload_count'] = {'date': datetime.now().date(), 'count': 0}

def generate_metadata(model, img_path):
    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()
    
    caption = model.generate_content([
        "Create a descriptive title in English, 10-15 words long, relevant to the stock photo's subject, object, and background. Avoid mentioning human names, brand, or company names.", img_data])
    tags = model.generate_content([
        "Generate up to 45 keywords that are relevant to the image (each keyword must be one word, separated by commas). "
        "Do not include mathematical symbols, punctuation marks, separator symbols, emojis, or special characters. "
        "Ensure that the keywords are highly suitable for the image, only in English.", img_data
    ])
    
    return caption, tags

def main():
    """Main function for the Streamlit app."""
    
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

    # API Key input
    api_key = st.text_input('Enter your API Key')

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
                    current_date = datetime.now()
                    
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
                        
                        # Generate metadata for each image
                        for img_path in image_paths:
                            caption, tags = generate_metadata(model, img_path)
                            st.write(f"Title: {caption}")
                            st.write(f"Keywords: {tags}")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.error(traceback.format_exc())  # Print detailed error traceback for debugging

if __name__ == '__main__':
    main()
