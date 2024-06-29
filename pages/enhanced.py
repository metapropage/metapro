import streamlit as st

st.set_page_config(page_title="Coming Soon", page_icon="🔜")

st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        color: #2e2e2e;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .coming-soon {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main"><div class="coming-soon">Coming Soon</div></div>', unsafe_allow_html=True)
