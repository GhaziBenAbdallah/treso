import streamlit as st
import base64
import time
import hashlib
import os

# Configuration
SESSION_TIMEOUT = 8 * 60 * 60  # 8 hours
TOKEN_SECRET = os.getenv("AUTH_SECRET", "default-secret-key-please-change")  # Use environment variable in production

def initialize_app():
    """One-time app initialization"""
    if 'app_initialized' not in st.session_state:
        st.set_page_config(
            layout="wide", 
            page_title="Tableau de board Trésorerie",
            initial_sidebar_state="auto"
        )
        st.session_state.app_initialized = True

def generate_auth_token(username):
    """Generate a secure authentication token"""
    timestamp = str(int(time.time()))
    raw_token = f"{username}{timestamp}{TOKEN_SECRET}"
    return hashlib.sha256(raw_token.encode()).hexdigest()

def validate_token(token):
    """Validate the auth token structure"""
    try:
        # Basic token validation (extend with proper verification in production)
        return len(token) == 64  # SHA-256 produces 64-character hex string
    except:
        return False

def validate_session():
    """Validate existing session or token"""
    # First check if we're already authenticated in session state
    if st.session_state.get('authenticated', False):
        if 'last_activity' in st.session_state:
            current_time = time.time()
            if current_time - st.session_state.last_activity > SESSION_TIMEOUT:
                logout()
                return False
            st.session_state.last_activity = current_time
            return True
        return True
    
    # Check for token in query parameters (for page refresh)
    if 'token' in st.query_params:
        token = st.query_params['token']
        if validate_token(token):
            st.session_state.auth_token = token
            st.session_state.authenticated = True
            st.session_state.last_activity = time.time()
            return True
    
    return False

def login(username):
    """Handle successful login"""
    st.session_state.auth_token = generate_auth_token(username)
    st.session_state.last_activity = time.time()
    st.session_state.authenticated = True
    st.session_state.current_user = username
    st.query_params['token'] = st.session_state.auth_token
    st.rerun()

def logout():
    """Handle logout clearing all session data"""
    keys = list(st.session_state.keys())
    for key in keys:
        del st.session_state[key]
    st.query_params.clear()
    st.rerun()


def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return ""

def render_login():
    """Login page with hidden sidebar and custom styling"""
    # Hide sidebar completely for login page
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Your custom login styling
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
        if username == "admin" and password == "1234":  # Replace with your auth logic
            login(username)
            st.success("Login successful. Redirecting...")
        else:
            st.error("Invalid username or password.")

def main():
    initialize_app()
    
    # Check authentication status - this is the key gatekeeper
    if validate_session():
        st.success("hello")
    else:
        render_login()

if __name__ == "__main__":
    main()