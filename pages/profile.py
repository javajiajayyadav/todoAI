import streamlit as st
from utils.helpers import init_page, render_sidebar
from utils.database import get_user_by_email
from utils.auth import update_user_profile, change_user_password

# Initialize page settings & authenticate
init_page("Profile")

# Render custom sidebar
render_sidebar("Profile")

user_email = st.session_state.user_email
user_data = get_user_by_email(user_email)

st.markdown("<h1 class='gradient-text'>👤 User Profile</h1>", unsafe_allow_html=True)
st.write("Manage your personal details and account credentials.")

# Two columns layout for Name/Email update and Password update
col_details, col_password = st.columns(2)

with col_details:
    st.markdown("<div class='glass-container' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("### Update Account Details")
    
    with st.form("profile_details_form"):
        curr_name = st.text_input("Name", value=user_data.get("name", user_data.get("username", ""))).strip()
        curr_email = st.text_input("Email Address", value=user_data.get("email", "")).strip()
        
        details_submit = st.form_submit_button("Update Details")
        
        if details_submit:
            success, msg = update_user_profile(user_email, curr_name, curr_email)
            if success:
                st.session_state.user_name = curr_name
                st.session_state.user_email = curr_email.lower().strip()
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    st.markdown("</div>", unsafe_allow_html=True)

with col_password:
    st.markdown("<div class='glass-container' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("### Change Password")
    
    with st.form("profile_password_form", clear_on_submit=True):
        old_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        
        password_submit = st.form_submit_button("Change Password")
        
        if password_submit:
            success, msg = change_user_password(user_email, old_pass, new_pass, confirm_pass)
            if success:
                st.success(msg)
            else:
                st.error(msg)
    st.markdown("</div>", unsafe_allow_html=True)
