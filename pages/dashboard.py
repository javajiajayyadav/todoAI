import uuid
from datetime import datetime, date
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.helpers import init_page, render_sidebar
from utils.database import get_user_todos, save_user_todos, get_user_history

# Initialize page settings & authenticate
init_page("Dashboard")

# Render custom sidebar menu
render_sidebar("Dashboard")

user_email = st.session_state.user_email
todos = get_user_todos(user_email)
history = get_user_history(user_email)

# Calculate metrics
total_tasks = len(todos)
pending_tasks = sum(1 for t in todos if not t.get("completed", False))
completed_tasks = sum(1 for t in todos if t.get("completed", False))
deleted_tasks = len(history)

# Header Section
st.markdown(
    f"<h1 class='gradient-text'>🏠 Dashboard</h1>"
    f"<p style='color: #94a3b8; font-size: 1.1rem; margin-bottom: 25px;'>Welcome, <b>{st.session_state.user_name}</b>! Here is a summary of your tasks.</p>",
    unsafe_allow_html=True
)

# Responsive Metric Cards (using raw HTML for visual excellence)
st.markdown(
    f"""
    <div class="metric-row">
        <div class="metric-card total">
            <div class="metric-label">Total Active</div>
            <div class="metric-value">{total_tasks}</div>
        </div>
        <div class="metric-card pending">
            <div class="metric-label">Pending</div>
            <div class="metric-value">{pending_tasks}</div>
        </div>
        <div class="metric-card completed">
            <div class="metric-label">Completed</div>
            <div class="metric-value">{completed_tasks}</div>
        </div>
        <div class="metric-card deleted">
            <div class="metric-label">Deleted (History)</div>
            <div class="metric-value">{deleted_tasks}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Quick Add & Analytics Columns
col_quick, col_chart = st.columns([1, 1])

with col_quick:
    st.markdown("<div class='glass-container' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Add Task")
    
    with st.form("quick_add_form", clear_on_submit=True):
        title = st.text_input("Task Title*", placeholder="E.g. Buy groceries").strip()
        desc = st.text_area("Description", placeholder="E.g. Milk, eggs, bread", height=70).strip()
        
        c1, c2 = st.columns(2)
        with c1:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
        with c2:
            due_date = st.date_input("Due Date", min_value=date.today())
            
        submit = st.form_submit_button("Add Task")
        
        if submit:
            if not title:
                st.error("Task title cannot be empty!")
            else:
                new_todo = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "description": desc,
                    "priority": priority,
                    "due_date": due_date.isoformat(),
                    "completed": False,
                    "created_time": datetime.now().isoformat(),
                    "updated_time": datetime.now().isoformat()
                }
                todos.append(new_todo)
                if save_user_todos(user_email, todos):
                    st.success("Task added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to save task.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    st.markdown("<div class='glass-container' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("### 📊 Task Breakdown")
    
    if total_tasks > 0:
        # Convert to DataFrame for easier plotting
        df = pd.DataFrame(todos)
        
        # Color palettes matching our theme
        color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#3b82f6"}
        
        # Status/Priority Grouping
        df_group = df.groupby(["priority", "completed"]).size().reset_index(name="count")
        df_group["Status"] = df_group["completed"].map({True: "Completed", False: "Pending"})
        
        fig = px.bar(
            df_group,
            x="priority",
            y="count",
            color="priority",
            pattern_shape="Status",
            labels={"count": "Number of Tasks", "priority": "Priority"},
            color_discrete_map=color_map,
            category_orders={"priority": ["High", "Medium", "Low"]},
            template="plotly_dark" if st.session_state.get("theme", "Dark") == "Dark" else "plotly_white"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=10, b=20),
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No active tasks to show analytics for. Start by creating a task!")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Task Filters & High Priority Tasks
st.markdown("### 🕒 High Priority & Overdue Alerts")
today_str = date.today().isoformat()

overdue_or_soon = []
for t in todos:
    if not t.get("completed", False):
        due = t.get("due_date", "")
        # Overdue or high priority due today
        if (due and due <= today_str) or t.get("priority") == "High":
            overdue_or_soon.append(t)

if overdue_or_soon:
    for task in overdue_or_soon[:3]:  # Display top 3 critical tasks
        due_lbl = "Today" if task['due_date'] == today_str else task['due_date']
        is_overdue = task['due_date'] < today_str
        due_color = "red" if is_overdue else "orange"
        
        badge_cls = f"badge-{task['priority'].lower()}"
        
        st.markdown(
            f"<div class='glass-card' style='margin-bottom: 12px; border-left: 5px solid {due_color};'>"
            f"<div style='display: flex; justify-content: space-between; align-items: center;'>"
            f"<div>"
            f"<h5 style='margin: 0; font-weight: 600;'>{task['title']}</h5>"
            f"<small style='color: #94a3b8;'>{task['description'] if task['description'] else 'No description'}</small>"
            f"</div>"
            f"<div>"
            f"<span class='badge {badge_cls}'>{task['priority']}</span> "
            f"<span style='color: {due_color}; font-weight: 500; font-size: 0.85rem;'>Due: {due_lbl}</span>"
            f"</div>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )
else:
    st.success("No urgent or overdue tasks. Keep up the good work!")
