import streamlit as st
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

# Render the dynamic menu
menu()

# Additional Information
st.markdown("### Why Choose MetaPro?")
st.markdown("""
**AI-Powered Precision:** Leverage the power of Google Generative AI to automatically...
""")
