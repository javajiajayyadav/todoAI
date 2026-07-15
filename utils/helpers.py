import os
import streamlit as st
from streamlit_option_menu import option_menu

def inject_custom_css():
    """Read style.css and inject into Streamlit head."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            
            # Dynamic light theme override
            if st.session_state.get("theme", "Dark") == "Light":
                light_theme_css = """
                body, .stApp {
                    background-color: #f8fafc !important;
                    color: #0f172a !important;
                }
                .glass-container {
                    background: rgba(255, 255, 255, 0.7) !important;
                    border: 1px solid rgba(0, 0, 0, 0.08) !important;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
                }
                .glass-card {
                    background: rgba(255, 255, 255, 0.8) !important;
                    border: 1px solid rgba(0, 0, 0, 0.05) !important;
                    color: #0f172a !important;
                }
                .metric-card {
                    background: rgba(0, 0, 0, 0.02) !important;
                    border: 1px solid rgba(0, 0, 0, 0.05) !important;
                }
                .metric-label {
                    color: #64748b !important;
                }
                .metric-value {
                    color: #0f172a !important;
                }
                section[data-testid="stSidebar"] {
                    background-color: #f1f5f9 !important;
                    border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
                }
                .nav-link {
                    color: #334155 !important;
                }
                .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
                    color: #0f172a !important;
                }
                .gradient-text {
                    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #312e81 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                """
                css_content += light_theme_css
                
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Failed to load stylesheet: {str(e)}")

def init_page(page_name: str):
    """Set up Streamlit page configuration, inject CSS, and enforce authentication."""
    # Configure page settings
    st.set_page_config(
        page_title=f"{page_name} | Smart Todo Manager",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject CSS
    inject_custom_css()
    
    # Check authentication
    if page_name != "Login" and not st.session_state.get("logged_in", False):
        st.warning("Access Denied. Please log in first.")
        st.switch_page("app.py")
        st.stop()

def render_sidebar(current_page: str):
    """Render the custom sidebar navigation."""
    if not st.session_state.get("logged_in", False):
        return

    with st.sidebar:
        # App Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.markdown("<h2 style='text-align: center; color: #6366f1;'>📝 TodoAI</h2>", unsafe_allow_html=True)

        # Welcome Text
        user_name = st.session_state.get("user_name", "User")
        st.markdown(
            f"<div style='text-align: center; margin-bottom: 20px; font-weight: 500; color: #94a3b8;'>"
            f"Logged in as:<br><strong style='color: #f8fafc; font-size: 1.1rem;'>{user_name}</strong>"
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown("---")

        # Sidebar Menu Items
        menu_items = [
            "Dashboard",
            "Todo List",
            "History",
            "Profile",
            "Settings",
            "Logout"
        ]
        
        icons = [
            "house-door", 
            "check2-square", 
            "clock-history", 
            "person-circle", 
            "gear", 
            "box-arrow-left"
        ]

        # Determine index
        try:
            default_index = menu_items.index(current_page)
        except ValueError:
            default_index = 0

        selected = option_menu(
            menu_title=None,
            options=menu_items,
            icons=icons,
            menu_icon="cast",
            default_index=default_index,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#94a3b8", "font-size": "1.05rem"},
                "nav-link": {
                    "font-size": "0.95rem",
                    "text-align": "left",
                    "margin": "4px 0px",
                    "color": "#f1f5f9",
                    "border-radius": "8px",
                    "transition": "all 0.3s ease"
                },
                "nav-link-selected": {"background-color": "#6366f1", "color": "#ffffff", "font-weight": "600"},
            }
        )

        # Handle Routing
        if selected == "Logout":
            # Clear authentication session
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.session_state.user_data = None
            st.success("Successfully logged out!")
            st.switch_page("app.py")
            st.stop()
            
        elif selected != current_page:
            # Map selected option to path
            page_mapping = {
                "Dashboard": "pages/dashboard.py",
                "Todo List": "pages/todos.py",
                "History": "pages/history.py",
                "Profile": "pages/profile.py",
                "Settings": "pages/settings.py"
            }
            target_path = page_mapping.get(selected)
            if target_path:
                st.switch_page(target_path)
