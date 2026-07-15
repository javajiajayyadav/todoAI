from datetime import datetime, date
import streamlit as st
from utils.helpers import init_page, render_sidebar
from utils.database import get_user_todos, save_user_todos, get_user_history, save_user_history

# Initialize page settings & authenticate
init_page("History")

# Render custom sidebar
render_sidebar("History")

user_email = st.session_state.user_email
history = get_user_history(user_email)

# Helper function to restore task back to active todos
def restore_todo(task_id):
    todos = get_user_todos(user_email)
    updated_history = []
    task_to_restore = None
    
    for h in history:
        if h["id"] == task_id:
            task_to_restore = h
        else:
            updated_history.append(h)
            
    if task_to_restore:
        # Clean up delete keys and move back
        task_to_restore.pop("deleted_time", None)
        task_to_restore["updated_time"] = datetime.now().isoformat()
        todos.append(task_to_restore)
        
        save_user_todos(user_email, todos)
        save_user_history(user_email, updated_history)
        st.success(f"Task '{task_to_restore['title']}' restored to active list!")
        st.rerun()

# Helper function to permanently remove a task
def permanent_delete_todo(task_id):
    updated_history = [h for h in history if h["id"] != task_id]
    save_user_history(user_email, updated_history)
    st.success("Task permanently deleted!")
    st.rerun()

# Helper function to clear all history
def clear_all_history():
    save_user_history(user_email, [])
    st.success("All history cleared permanently!")
    st.rerun()

# Header
st.markdown("<h1 class='gradient-text'>🕒 History</h1>", unsafe_allow_html=True)
st.write("View, restore, or permanently remove deleted tasks.")

if not history:
    st.info("Your history is empty! Tasks you delete will appear here.")
else:
    # History action tools
    col_search, col_action = st.columns([3, 1])
    
    with col_search:
        search_q = st.text_input("🔍 Search deleted tasks...", placeholder="Type to search history...")
        
    with col_action:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        # Clear All History trigger button with popup confirm box standard in Streamlit
        confirm_clear = st.button("🚨 Clear All History")
        if confirm_clear:
            st.session_state.confirm_clear_active = True
            
    # Confirm double check box
    if st.session_state.get("confirm_clear_active", False):
        st.warning("Are you absolutely sure you want to permanently clear all task history? This action CANNOT be undone.")
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button("Yes, Clear Everything"):
                st.session_state.confirm_clear_active = False
                clear_all_history()
        with cc2:
            if st.button("Cancel"):
                st.session_state.confirm_clear_active = False
                st.rerun()
                
    st.markdown("---")

    # Filtered List
    filtered_history = history.copy()
    if search_q:
        filtered_history = [h for h in filtered_history if search_q.lower() in h["title"].lower() or search_q.lower() in h.get("description", "").lower()]

    # Display History Items
    if filtered_history:
        # Reverse chronological by deletion time (latest first)
        filtered_history.sort(key=lambda x: x.get("deleted_time", ""), reverse=True)
        
        for todo in filtered_history:
            task_id = todo["id"]
            prio = todo["priority"]
            badge_cls = f"badge-{prio.lower()}"
            
            # Format deletion time
            del_time_str = "Unknown"
            if "deleted_time" in todo:
                try:
                    dt = datetime.fromisoformat(todo["deleted_time"])
                    del_time_str = dt.strftime("%b %d, %Y at %I:%M %p")
                except Exception:
                    del_time_str = todo["deleted_time"]
            
            st.markdown(
                f"<div class='glass-card' style='margin-bottom: 15px; border-left: 5px solid #6b7280; opacity: 0.85;'>"
                f"<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;'>"
                f"<div style='flex: 1; min-width: 250px;'>"
                f"<h4 style='margin: 0; text-decoration: line-through; color: #94a3b8; font-weight: 600;'>{todo['title']}</h4>"
                f"<p style='color: #64748b; font-size: 0.9rem; margin-top: 5px; margin-bottom: 10px;'>{todo.get('description', '')}</p>"
                f"<div style='display: flex; gap: 10px; align-items: center; flex-wrap: wrap;'>"
                f"<span class='badge {badge_cls}'>{prio}</span>"
                f"<span style='font-size: 0.8rem; color: #94a3b8;'>🗑️ Deleted on: {del_time_str}</span>"
                f"</div>"
                f"</div>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            
            # Action button row underneath the static display card
            btn_cols = st.columns([7, 1.5, 1.5])
            with btn_cols[1]:
                st.button("↩️ Restore", key=f"rest_{task_id}", on_click=restore_todo, args=(task_id,))
            with btn_cols[2]:
                st.button("❌ Remove", key=f"pdel_{task_id}", on_click=permanent_delete_todo, args=(task_id,))
    else:
        st.info("No deleted tasks found matching your search.")
