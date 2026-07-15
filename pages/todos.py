import uuid
from datetime import datetime, date
import streamlit as st
from utils.helpers import init_page, render_sidebar
from utils.database import get_user_todos, save_user_todos, get_user_history, save_user_history

# Initialize page settings & authenticate
init_page("Todo List")

# Render custom sidebar
render_sidebar("Todo List")

user_email = st.session_state.user_email
todos = get_user_todos(user_email)

# Helper function to delete task to history
def delete_todo(task_id):
    history = get_user_history(user_email)
    updated_todos = []
    task_to_delete = None
    
    for t in todos:
        if t["id"] == task_id:
            task_to_delete = t
        else:
            updated_todos.append(t)
            
    if task_to_delete:
        task_to_delete["deleted_time"] = datetime.now().isoformat()
        history.append(task_to_delete)
        save_user_todos(user_email, updated_todos)
        save_user_history(user_email, history)
        st.success(f"Moved task '{task_to_delete['title']}' to history!")
        st.rerun()

# Helper function to toggle complete status
def toggle_status(task_id, completed):
    for t in todos:
        if t["id"] == task_id:
            t["completed"] = completed
            t["updated_time"] = datetime.now().isoformat()
            break
    save_user_todos(user_email, todos)
    st.success("Task status updated!")
    st.rerun()

# Helper function to edit/update task
def update_todo(task_id, new_title, new_desc, new_priority, new_due_date):
    for t in todos:
        if t["id"] == task_id:
            t["title"] = new_title
            t["description"] = new_desc
            t["priority"] = new_priority
            t["due_date"] = new_due_date.isoformat()
            t["updated_time"] = datetime.now().isoformat()
            break
    save_user_todos(user_email, todos)
    st.success("Task updated successfully!")
    st.session_state.editing_todo_id = None
    st.rerun()

# Header
st.markdown("<h1 class='gradient-text'>✅ Tasks Manager</h1>", unsafe_allow_html=True)
st.write("Create, edit, sort, and complete your tasks.")

# Edit Form Section (Appears conditionally when user clicked Edit)
if st.session_state.get("editing_todo_id"):
    editing_id = st.session_state.editing_todo_id
    # Find task details
    edit_task = next((t for t in todos if t["id"] == editing_id), None)
    
    if edit_task:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.markdown("### ✏️ Edit Task Details")
        
        with st.form("edit_todo_form"):
            e_title = st.text_input("Title*", value=edit_task["title"]).strip()
            e_desc = st.text_area("Description", value=edit_task.get("description", "")).strip()
            
            c1, c2 = st.columns(2)
            with c1:
                e_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(edit_task["priority"]))
            with c2:
                # Handle old string ISO dates safely
                try:
                    default_date = date.fromisoformat(edit_task["due_date"])
                except Exception:
                    default_date = date.today()
                e_due_date = st.date_input("Due Date", value=default_date)
                
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                save_changes = st.form_submit_button("Update Task")
            with c_btn2:
                cancel_changes = st.form_submit_button("Cancel")
                
            if save_changes:
                if not e_title:
                    st.error("Title is required!")
                else:
                    update_todo(editing_id, e_title, e_desc, e_priority, e_due_date)
            if cancel_changes:
                st.session_state.editing_todo_id = None
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Add Task Dialog Toggle or Form
with st.expander("➕ Create New Todo Task"):
    with st.form("add_todo_form", clear_on_submit=True):
        title = st.text_input("Title*").strip()
        desc = st.text_area("Description").strip()
        
        c1, c2 = st.columns(2)
        with c1:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1, key="add_priority")
        with c2:
            due_date = st.date_input("Due Date", min_value=date.today(), key="add_due_date")
            
        submit = st.form_submit_button("Add Task")
        if submit:
            if not title:
                st.error("Task title is required!")
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
                    st.success("Task created!")
                    st.rerun()

st.markdown("---")

# Filter Section
st.markdown("### Search & Filters")
col_search, col_status, col_prio, col_sort = st.columns([2, 1, 1, 1])

with col_search:
    search_q = st.text_input("🔍 Search tasks by title...", placeholder="Search...")
with col_status:
    filter_status = st.selectbox("Status", ["All", "Pending", "Completed"])
with col_prio:
    filter_prio = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
with col_sort:
    sort_by = st.selectbox("Sort By", ["Due Date", "Priority", "Created Time", "Updated Time"])

# Apply Filters
filtered_todos = todos.copy()

if search_q:
    filtered_todos = [t for t in filtered_todos if search_q.lower() in t["title"].lower() or search_q.lower() in t.get("description", "").lower()]

if filter_status != "All":
    is_completed = filter_status == "Completed"
    filtered_todos = [t for t in filtered_todos if t.get("completed", False) == is_completed]

if filter_prio != "All":
    filtered_todos = [t for t in filtered_todos if t.get("priority") == filter_prio]

# Apply Sorting
priority_weights = {"High": 3, "Medium": 2, "Low": 1}
if sort_by == "Due Date":
    filtered_todos.sort(key=lambda x: x.get("due_date", ""))
elif sort_by == "Priority":
    filtered_todos.sort(key=lambda x: priority_weights.get(x.get("priority", "Medium"), 2), reverse=True)
elif sort_by == "Created Time":
    filtered_todos.sort(key=lambda x: x.get("created_time", ""), reverse=True)
elif sort_by == "Updated Time":
    filtered_todos.sort(key=lambda x: x.get("updated_time", ""), reverse=True)

# Render Task List
if filtered_todos:
    for todo in filtered_todos:
        task_id = todo["id"]
        is_done = todo.get("completed", False)
        
        # Tags styling
        prio = todo["priority"]
        badge_cls = f"badge-{prio.lower()}"
        status_lbl = "Completed" if is_done else "Pending"
        status_cls = "status-completed" if is_done else "status-pending"
        
        # Format dates nicely
        try:
            due_dt = date.fromisoformat(todo["due_date"])
            formatted_due = due_dt.strftime("%b %d, %Y")
            
            # Highlight overdue tasks in red
            if not is_done and due_dt < date.today():
                due_style = "color: #ef4444; font-weight: 600;"
                formatted_due += " (Overdue!)"
            else:
                due_style = "color: #94a3b8;"
        except Exception:
            formatted_due = todo["due_date"]
            due_style = "color: #94a3b8;"

        # Render glassmorphic card for task
        st.markdown(
            f"<div class='glass-card' style='margin-bottom: 15px; border-left: 5px solid {'#10b981' if is_done else '#6366f1'};'>"
            f"<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;'>"
            f"<div style='flex: 1; min-width: 250px;'>"
            f"<h4 style='margin: 0; text-decoration: {'line-through' if is_done else 'none'}; opacity: {0.6 if is_done else 1.0}; font-weight: 600;'>{todo['title']}</h4>"
            f"<p style='color: #94a3b8; font-size: 0.9rem; margin-top: 5px; margin-bottom: 10px;'>{todo.get('description', '')}</p>"
            f"<div style='display: flex; gap: 10px; align-items: center; flex-wrap: wrap;'>"
            f"<span class='badge {badge_cls}'>{prio}</span>"
            f"<span class='badge {status_cls}'>{status_lbl}</span>"
            f"<span style='font-size: 0.8rem; {due_style}'>📅 Due: {formatted_due}</span>"
            f"</div>"
            f"</div>"
            f"<div style='display: flex; gap: 8px; margin-top: 10px; align-self: center;'>"
            f"<!-- Space for streamlit buttons -->"
            f"</div>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )
        
        # Interactive Streamlit buttons nested below each item's description layout block
        btn_cols = st.columns([6, 1, 1, 1])
        with btn_cols[1]:
            if is_done:
                st.button("↩️ Pending", key=f"pend_{task_id}", on_click=toggle_status, args=(task_id, False))
            else:
                st.button("✅ Complete", key=f"comp_{task_id}", on_click=toggle_status, args=(task_id, True))
        with btn_cols[2]:
            st.button("✏️ Edit", key=f"edit_{task_id}", on_click=lambda tid=task_id: st.session_state.update(editing_todo_id=tid))
        with btn_cols[3]:
            st.button("🗑️ Delete", key=f"del_{task_id}", on_click=delete_todo, args=(task_id,))
else:
    st.info("No tasks found matching your filters. Add a new task or change filters!")
