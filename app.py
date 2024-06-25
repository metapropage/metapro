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
    st.title("Dashboard")
    
    def set_role(role):
        st.session_state.role = role

    # Button to choose super-admin role
    if st.button("Pilih peran sebagai super-admin"):
        set_role("super-admin")
        st.success("Peran 'super-admin' telah dipilih.")
    
    # Display the selected role if already set
    if st.session_state.role:
        st.write(f"Peran Anda saat ini: {st.session_state.role}")
    
    menu()  # Render the dynamic menu

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        set_lock("")
        st.success("Berhasil keluar.")

    # Additional Information
    st.markdown("### Mengapa Memilih MetaPro?")
    st.markdown("""
    **AI-Powered Precision:** Manfaatkan kekuatan Google Generative AI untuk secara otomatis menghasilkan judul dan tag yang sangat relevan dan deskriptif untuk gambar Anda. Tingkatkan metadata gambar Anda dengan akurasi dan relevansi yang belum pernah ada sebelumnya.

    **Alur Kerja yang Efisien:** Unggah gambar Anda hanya dengan beberapa klik. Aplikasi kami memproses setiap foto, menyematkan metadata yang dihasilkan, dan menyiapkannya untuk diunggah—secara otomatis dan mudah.

    **Upload Gdrive yang Aman dan Efisien:** Setelah diproses, gambar Anda diunggah dengan aman ke Google Drive. Jaga alur kerja Anda tetap lancar dan data Anda aman dengan sistem upload kami yang kuat.

    **Cara Kerjanya:**
    1. **Unggah Gambar Anda:** Seret dan lepas file JPG/JPEG Anda ke pengunggah.
    2. **Hasilkan Metadata:** Lihat bagaimana aplikasi menggunakan AI untuk membuat judul deskriptif dan tag yang relevan.
    3. **Sematkan Metadata:** Aplikasi menyematkan metadata langsung ke dalam gambar Anda.
    4. **Unggah langsung ke Google Drive untuk pengunduhan lebih cepat.**

    **Berlangganan Sekarang dan Rasakan Perbedaannya:**
    - **Paket MetaPro Basic:** $10 untuk 3 bulan – Unggah hingga 1.000 gambar setiap hari.
    - **Paket MetaPro Premium:** $40 untuk unggahan gambar tak terbatas seumur hidup.

    Siap untuk merevolusi alur kerja Anda? Berlangganan hari ini dan ambil langkah pertama menuju solusi manajemen gambar yang lebih cerdas dan efisien.
    """)
