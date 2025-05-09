import streamlit as st
import base64

def login_page():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(331deg,#000000 0%, #83c2c2 30%, #d35e210f 70%) !important;
            height: 100vh;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .logo-container img {
            width: 200px;
            height: auto;
            border-radius: 10px;
        }
        .login-box {
            background-color: rgba(255, 255, 255, 0.15);
            padding: 2rem;
            border-radius: 10px;
            backdrop-filter: blur(10px);
            width: 300px;
            margin: auto;
        }
        .stButton > button {
            background-color: #1f77b4;
            color: white;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #0d4b78;
            color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)

    def get_base64_of_bin_file(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return ""

    # Display logo
    image_base64 = get_base64_of_bin_file('img/mas_group.png')
    if image_base64:
        st.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{image_base64}">
            </div>
            """, unsafe_allow_html=True
        )

    # Login form
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        login_button = st.button("Login")
        st.markdown('</div>', unsafe_allow_html=True)

    if login_button:
        if username == "admin" and password == "1234":
            st.session_state.authenticated = True
            st.session_state.logged_in = True
            st.session_state.current_page = "home"
            st.query_params["page"] = "home"
            st.success("Login successful. Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password.")