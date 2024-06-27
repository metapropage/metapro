import streamlit as st
import os
import tempfile
from PIL import Image, ImageOps
import google.generativeai as genai
import iptcinfo3
import traceback
import re
import unicodedata
from datetime import datetime, timedelta
import pytz
from menu import menu_with_redirect
from io import BytesIO

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

def generate_description(model, img, num_prompts):
    description = model.generate_content([f"create {num_prompts} prompts for microstock photostock Adobe Stock. The prompts must be able to produce images exactly like this one. include subject, style, and context.", img])
    return description.text.strip()

def format_midjourney_prompt(description):
    prompt_text = f"{description} -ar 16:9"
    return prompt_text

def convert_svg_to_png(svg_path):
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM

        drawing = svg2rlg(svg_path)
        png_path = svg_path.replace('.svg', '.png')
        renderPM.drawToFile(drawing, png_path, fmt='PNG')
        return png_path
    except Exception as e:
        st.error(f"Failed to convert SVG to PNG: {e}")
        return None

def convert_eps_to_jpeg(eps_path):
    try:
        from wand.image import Image as WandImage

        with WandImage(filename=eps_path) as img:
            img.format = 'jpeg'
            jpeg_path = eps_path.replace('.eps', '.jpg')
            img.save(filename=jpeg_path)
            return jpeg_path
    except Exception as e:
        st.error(f"Failed to convert EPS to JPEG: {e}")
        return None

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

        # Number of files to upload
        num_files = st.number_input('Enter the number of files to upload', min_value=1, max_value=10, value=1)

        # Number of prompts to generate
        num_prompts = st.number_input('Enter the number of prompts to generate', min_value=1, max_value=10, value=4)

        # Upload image files
        uploaded_files = st.file_uploader(f'Upload {num_files} Image(s) (JPG, JPEG, PNG, SVG, EPS supported)', type=['jpg', 'jpeg', 'png', 'svg', 'eps'], accept_multiple_files=True, key="file_uploader")

        if uploaded_files and len(uploaded_files) == num_files and st.button("Process"):
            with st.spinner("Processing..."):
                try:
                    # Check and update upload count for the current date
                    if st.session_state['upload_count']['date'] != current_date.date():
                        st.session_state['upload_count'] = {
                            'date': current_date.date(),
                            'count': 0
                        }

                    # Check if remaining uploads are available
                    if st.session_state['upload_count']['count'] >= 1000:
                        remaining_uploads = 0
                        st.warning(f"You have exceeded the upload limit. Remaining uploads for today: {remaining_uploads}")
                        return
                    else:
                        st.session_state['upload_count']['count'] += num_files
                        st.success(f"Upload successful. Remaining uploads for today: {1000 - st.session_state['upload_count']['count']}")

                    genai.configure(api_key=api_key)  # Configure AI model with API key
                    model = genai.GenerativeModel('gemini-pro-vision')

                    # Create a temporary directory to store the uploaded images
                    with tempfile.TemporaryDirectory() as temp_dir:
                        for uploaded_file in uploaded_files:
                            # Save the uploaded image to the temporary directory
                            temp_image_path = os.path.join(temp_dir, uploaded_file.name)
                            with open(temp_image_path, 'wb') as f:
                                f.write(uploaded_file.read())

                            # Convert SVG and EPS to JPEG if needed
                            if uploaded_file.type == 'image/svg+xml':
                                temp_image_path = convert_svg_to_png(temp_image_path)
                            elif uploaded_file.type == 'application/postscript':
                                temp_image_path = convert_eps_to_jpeg(temp_image_path)

                            # Open the image
                            if temp_image_path:
                                img = Image.open(temp_image_path)

                                # Generate description and prompts
                                description = generate_description(model, img, num_prompts)
                                prompts = description.split("\n")

                                # Display thumbnail and prompts
                                st.image(img, width=100)
                                st.markdown("## Prompts\n")
                                for j, prompt in enumerate(prompts):
                                    st.markdown(f"### Prompt {j+1}\n")
                                    st.markdown(f"{prompt.strip()} -ar 16:9\n")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.error(traceback.format_exc())  # Print detailed error traceback for debugging

if __name__ == '__main__':
    main()
