import os
import streamlit as st
from dotenv import load_dotenv
from utils.helpers import init_page, inject_custom_css
from utils.auth import login_user, register_user

# Load environment variables
load_dotenv()
APP_NAME = os.getenv("APP_NAME", "Smart Todo Manager")

# Run basic page initialization
init_page("Login")

# If already logged in, redirect to dashboard
if st.session_state.get("logged_in", False):
    st.switch_page("pages/dashboard.py")
    st.stop()

# Set up page styling
inject_custom_css()

# Center Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Logo / Title
    st.markdown(
        f"<h1 style='text-align: center; margin-bottom: 5px;' class='gradient-text'>{APP_NAME}</h1>"
        "<p style='text-align: center; color: #94a3b8; font-size: 1.1rem; margin-bottom: 30px;'>"
        "Secure, glassmorphic task management dashboard"
        "</p>",
        unsafe_allow_html=True
    )
    
    # Auth Tabs Container
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    tab_login, tab_register = st.tabs(["🔑 Sign In", "📝 Create Account"])
    
    with tab_login:
        st.markdown("<h4 style='margin-top: 15px;'>Welcome Back</h4>", unsafe_allow_html=True)
        login_email = st.text_input("Email Address", key="login_email_input").strip()
        login_password = st.text_input("Password", type="password", key="login_password_input")
        
        login_btn = st.button("Sign In")
        if login_btn:
            success, msg, user_data = login_user(login_email, login_password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_email = user_data["email"]
                st.session_state.user_name = user_data.get("name", user_data["username"])
                st.session_state.user_data = user_data
                
                st.success(msg)
                st.switch_page("pages/dashboard.py")
                st.stop()
            else:
                st.error(msg)
                
    with tab_register:
        st.markdown("<h4 style='margin-top: 15px;'>Create a New Account</h4>", unsafe_allow_html=True)
        reg_username = st.text_input("Username", key="reg_user_input").strip()
        reg_email = st.text_input("Email Address", key="reg_email_input").strip()
        reg_password = st.text_input("Password", type="password", key="reg_pass_input")
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm_input")
        
        reg_btn = st.button("Register")
        if reg_btn:
            success, msg = register_user(reg_username, reg_email, reg_password, reg_confirm)
            if success:
                st.success(msg)
            else:
                st.error(msg)
                
    st.markdown("</div>", unsafe_allow_html=True)
