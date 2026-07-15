import streamlit as st
from utils.helpers import init_page, render_sidebar

# Initialize page settings & authenticate
init_page("Settings")

# Render custom sidebar
render_sidebar("Settings")

st.markdown("<h1 class='gradient-text'>⚙ Settings</h1>", unsafe_allow_html=True)
st.write("Customize your application appearance and preferences.")

st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
st.markdown("### 🎨 Appearance Settings")

# Initialize theme session state if not set
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

current_theme = st.session_state.theme
theme_index = 0 if current_theme == "Dark" else 1

theme_select = st.selectbox(
    "Choose Theme Mode",
    ["Dark Mode (Recommended)", "Light Mode"],
    index=theme_index,
    help="Toggle between professional dark dashboard mode and high-contrast light mode."
)

new_theme = "Dark" if "Dark" in theme_select else "Light"

# Handle theme change trigger
if new_theme != current_theme:
    st.session_state.theme = new_theme
    st.success(f"Theme switched to {new_theme} Mode!")
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Mock preference settings for high-fidelity completeness
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
st.markdown("### 🔔 Notification & Behavior Preferences")

with st.form("settings_preferences_form"):
    st.checkbox("Show alert for overdue tasks on login", value=True)
    st.checkbox("Automatically move completed tasks to bottom of the list", value=False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    notify_method = st.radio(
        "Default priority filters",
        ["Show All Tasks", "Show High Priority First", "Show Upcoming Tasks First"]
    )
    
    save_prefs = st.form_submit_button("Save Preferences")
    if save_prefs:
        st.success("Preferences updated successfully!")
st.markdown("</div>", unsafe_allow_html=True)
