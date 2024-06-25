import streamlit as st
import os
import tempfile
from PIL import Image
import google.generativeai as genai
import pytz
from datetime import datetime, timedelta

st.set_option("client.showSidebarNavigation", False)

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

# Initialize session state
if 'license_validated' not in st.session_state:
    st.session_state['license_validated'] = False

if 'upload_count' not in st.session_state:
    st.session_state['upload_count'] = {
        'date': None,
        'count': 0
    }

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None

# Function to generate detailed descriptions for files using AI model
def generate_description(model, file_path):
    with open(file_path, "rb") as img_file:
        img_bytes = img_file.read()
    description = model.generate_content(["Generate a very detailed description for this image:", img_bytes])
    return description.text.strip()

def main():
    """Main function for the Streamlit app."""

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
            correct_key = "dian12345"
            if validation_key and validation_key == correct_key:
                st.session_state['license_validated'] = True
                start_date = datetime.now(JAKARTA_TZ)
                with open(license_file, 'w') as file:
                    file.write(start_date.isoformat())
            elif validation_key:
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
        if api_key:
            st.session_state['api_key'] = api_key

        # Upload image files
        uploaded_files = st.file_uploader('Upload Images (JPG, PNG, SVG, EPS supported)', accept_multiple_files=True)
        if uploaded_files and st.button("Process"):
            with st.spinner("Processing..."):
                try:
                    # Check and update upload count for the current date
                    if st.session_state['upload_count']['date'] != current_date.date():
                        st.session_state['upload_count'] = {
                            'date': current_date.date(),
                            'count': 0
                        }

                    # Check if remaining uploads are available
                    if st.session_state['upload_count']['count'] + len(uploaded_files) > 50:
                        remaining_uploads = 50 - st.session_state['upload_count']['count']
                        st.warning(f"You have exceeded the upload limit. Remaining uploads for today: {remaining_uploads}")
                        return
                    else:
                        st.session_state['upload_count']['count'] += len(uploaded_files)
                        st.success(f"Uploads successful. Remaining uploads for today: {50 - st.session_state['upload_count']['count']}")

                    genai.configure(api_key=api_key)  # Configure AI model with API key
                    model = genai.GenerativeModel('gemini-pro-vision')

                    # Create a temporary directory to store the uploaded images
                    with tempfile.TemporaryDirectory() as temp_dir:
                        # Save the uploaded images to the temporary directory
                        file_paths = []
                        for file in uploaded_files:
                            temp_file_path = os.path.join(temp_dir, file.name)
                            with open(temp_file_path, 'wb') as f:
                                f.write(file.read())
                            file_paths.append(temp_file_path)

                        # Process each file and generate detailed descriptions using AI
                        descriptions = []
                        for i, file_path in enumerate(file_paths):
                            st.text(f"Generating description for file {i + 1}/{len(file_paths)}")
                            try:
                                description = generate_description(model, file_path)
                                descriptions.append((os.path.basename(file_path), description))
                            except Exception as e:
                                st.error(f"An error occurred while generating description for {os.path.basename(file_path)}: {e}")
                                continue

                        # Display the generated descriptions
                        st.markdown("## Generated Descriptions")
                        for file_name, description in descriptions:
                            st.markdown(f"**File Name:** {file_name}")
                            st.markdown(f"**Description:** {description}")

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
