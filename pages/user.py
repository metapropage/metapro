
import streamlit as st
import os
import tempfile
from PIL import Image
import google.generativeai as genai
import iptcinfo3
import zipfile
import time
import traceback
import re
import unicodedata
from datetime import datetime, timedelta
import pytz
import base64
import json
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set the timezone to UTC+7 Jakarta
JAKARTA_TZ = pytz.timezone('Asia/Jakarta')

# Initialize session state for license validation and upload count
if 'license_validated' not in st.session_state:
    st.session_state['license_validated'] = False

if 'upload_count' not in st.session_state:
    st.session_state['upload_count'] = {
        'date': datetime.now(JAKARTA_TZ).date(),
        'count': 0
    }

# Function to normalize and clean text
def normalize_text(text):
    normalized = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return normalized

# Function to generate metadata for images using AI model
def generate_metadata(model, img):
    caption = model.generate_content([
        "Create a descriptive title in English, 10-15 words long, relevant to the stock photo's subject, object, and background. Avoid mentioning human names, brand, or company names.", img])
    tags = model.generate_content([
        "Generate up to 45 keywords that are relevant to the image (each keyword must be one word, separated by commas). "
        "Do not include mathematical symbols, punctuation marks, separator symbols, emojis, or special characters. "
        "Ensure that the keywords are highly suitable for the image, only in English.", img
    ])

    # Filter out undesirable characters from the generated tags
    filtered_tags = re.sub(r'[^\w\s,]', '', tags.text)
    
    # Trim the generated keywords if they exceed 49 words
    keywords = filtered_tags.split(',')[:49]  # Limit to 49 words
    trimmed_tags = ','.join(keywords)
    
    return {
        'Title': caption.text.strip(),  # Remove leading/trailing whitespace
        'Tags': trimmed_tags
    }

# Function to embed metadata into images
def embed_metadata(image_path, metadata, progress_bar, files_processed, total_files):
    try:
        # Simulate delay
        time.sleep(1)

        # Open the image file
        img = Image.open(image_path)

        # Load existing IPTC data (if any)
        iptc_data = iptcinfo3.IPTCInfo(image_path, force=True)

        # Clear existing IPTC metadata
        for tag in iptc_data._data:
            iptc_data._data[tag] = []

        # Update IPTC data with new metadata
        iptc_data['keywords'] = [metadata.get('Tags', '')]  # Keywords
        iptc_data['caption/abstract'] = [metadata.get('Title', '')]  # Title

        # Save the image with the embedded metadata
        iptc_data.save()

        # Update progress bar
        files_processed += 1
        progress_bar.progress(files_processed / total_files)
        progress_bar.text(f"Embedding metadata for image {files_processed}/{total_files}")

        # Return the updated image path for further processing
        return image_path

    except Exception as e:
        st.error(f"An error occurred while embedding metadata: {e}")
        st.error(traceback.format_exc())  # Print detailed error traceback for debugging

def zip_processed_images(image_paths):
    try:
        zip_file_path = os.path.join(tempfile.gettempdir(), 'processed_images.zip')

        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for image_path in image_paths:
                zipf.write(image_path, arcname=os.path.basename(image_path))

        return zip_file_path

    except Exception as e:
        st.error(f"An error occurred while zipping images: {e}")
        st.error(traceback.format_exc())
        return None

def upload_to_drive(zip_file_path, credentials):
    try:
        service = build('drive', 'v3', credentials=credentials)
        file_metadata = {
            'name': os.path.basename(zip_file_path),
            'mimeType': 'application/zip'
        }
        media = MediaFileUpload(zip_file_path, mimetype='application/zip', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()

        # Make the file publicly accessible
        service.permissions().create(
            fileId=file['id'],
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        return file.get('webViewLink')
    except Exception as e:
        st.error(f"An error occurred while uploading to Google Drive: {e}")
        st.error(traceback.format_exc())
        return None


def main():
    """Main function for the Streamlit app."""
    
    # Apply custom styling
    st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        section[data-testid="stSidebar"] div:first-child {top: 0; height: 100vh;}
    </style>
    """, unsafe_allow_html=True)

    # Validation key input
    validation_key = st.text_input('Password', type='password')

    # Check if validation key is correct
    correct_key = "dian"  # Replace "your_validation_key" with your actual validation key

    if not validation_key:
        st.warning("Please enter a Password.")
        return

    if validation_key != correct_key:
        st.error("Invalid Password. Please enter the correct password.")
        return

    
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
        api_key = st.text_input('Enter your API Key')

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
                        if st.session_state['upload_count']['count'] + len(valid_files) > 125:
                            remaining_uploads = 125 - st.session_state['upload_count']['count']
                            st.warning(f"You have exceeded the upload limit. Remaining uploads for today: {remaining_uploads}")
                            return
                        else:
                            st.session_state['upload_count']['count'] += len(valid_files)
                            st.success(f"Uploads successful. Remaining uploads for today: {125 - st.session_state['upload_count']['count']}")

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

                            # Process each image and generate titles and tags using AI
                            metadata_list = []
                            process_placeholder = st.empty()
                            for i, image_path in enumerate(image_paths):
                                process_placeholder.text(f"Processing Generate Titles and Tags {i + 1}/{len(image_paths)}")
                                try:
                                    img = Image.open(image_path)
                                    metadata = generate_metadata(model, img)
                                    metadata_list.append(metadata)
                                except Exception as e:
                                    st.error(f"An error occurred while generating metadata for {os.path.basename(image_path)}: {e}")
                                    st.error(traceback.format_exc())
                                    continue

                            # Embed metadata into images
                            total_files = len(image_paths)
                            files_processed = 0

                            # Display the progress bar and current file number
                            progress_placeholder = st.empty()
                            progress_bar = progress_placeholder.progress(0)
                            progress_placeholder.text(f"Processing images 0/{total_files}")

                            processed_image_paths = []
                            for i, (image_path, metadata) in enumerate(zip(image_paths, metadata_list)):
                                process_placeholder.text(f"Embedding metadata for image {i + 1}/{len(image_paths)}")
                                updated_image_path = embed_metadata(image_path, metadata, progress_bar, files_processed, total_files)
                                if updated_image_path:
                                    processed_image_paths.append(updated_image_path)
                                    files_processed += 1
                                    # Update progress bar and current file number
                                    progress_bar.progress(files_processed / total_files)

                            # Zip processed images
                            zip_file_path = zip_processed_images(processed_image_paths)

                            if zip_file_path:
                                st.success(f"Successfully zipped processed images to {zip_file_path}")

                                # Upload zip file to Google Drive and get the shareable link
                                credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/drive.file'])
                                drive_link = upload_to_drive(zip_file_path, credentials)

                                if drive_link:
                                    st.success("File uploaded to Google Drive successfully!")
                                    st.markdown(f"[Download processed images from Google Drive]({drive_link})")

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.error(traceback.format_exc())  # Print detailed error traceback for debugging

        # Display "About" button
if st.button("About"):
    st.markdown("""
    ### Why Choose MetaPro?

    **AI-Powered Precision:** Leverage the power of Google Generative AI to automatically generate highly relevant and descriptive titles and tags for your images. Enhance your image metadata with unprecedented accuracy and relevance.

    **Streamlined Workflow:** Upload your images in just a few clicks. Our app processes each photo, embeds the generated metadata, and prepares it for upload—automatically and effortlessly.

    **Secure and Efficient Gdrive Upload:** Once processed, your images are securely uploaded to gdrive. Keep your workflow smooth and your data safe with our robust upload system.

    *How It Works:
    1. Upload Your Images: Drag and drop your JPG/JPEG files into the uploader.
    2. Generate Metadata: Watch as the app uses AI to create descriptive titles and relevant tags.
    3. Embed Metadata: The app embeds the metadata directly into your images.
    4. Directly upload to Google Drive for faster downloads.
    
    **Subscribe Now and Experience the Difference:**
    - **MetaPro Standard Plan: $9.99/month – Upload up to 1000 images daily for 1 month, includes access to one Adobe Stock account.
    - **MetaPro Premium Plan: $39.99/month – Unlimited image uploads and access to unlimited Adobe Stock accounts for lifetime.

    Ready to revolutionize your workflow? Subscribe today and take the first step towards a smarter, more efficient image management solution.

    """)

if __name__ == '__main__':
    main()
