import os
import json
import shutil
from datetime import datetime
import streamlit as st

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
USERS_FILE = os.path.join(DB_DIR, "users.json")
TODOS_FILE = os.path.join(DB_DIR, "todos.json")
HISTORY_FILE = os.path.join(DB_DIR, "history.json")

def init_db():
    """Ensure database directory and JSON files exist with proper empty structure."""
    try:
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR, exist_ok=True)
        
        for file_path in [USERS_FILE, TODOS_FILE, HISTORY_FILE]:
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({}, f, indent=4)
    except Exception as e:
        st.error(f"Failed to initialize database directories: {str(e)}")

def load_json(file_path):
    """Load JSON file safely, handles missing and corrupted files."""
    init_db()  # Make sure file exists or is initialized
    
    if not os.path.exists(file_path):
        return {}
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as jde:
        # Corruption handling: rename corrupt file and initialize new one
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        corrupt_backup = f"{file_path}.corrupt.{timestamp}"
        try:
            shutil.copy(file_path, corrupt_backup)
            st.warning(f"Corrupted database file detected. Restored backup to {os.path.basename(corrupt_backup)}.")
        except Exception as copy_err:
            st.error(f"Failed to backup corrupt file: {str(copy_err)}")
            
        # Re-initialize file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)
        except Exception as write_err:
            st.error(f"Failed to write fresh JSON structure: {str(write_err)}")
            
        return {}
    except Exception as e:
        st.error(f"Error reading database file {os.path.basename(file_path)}: {str(e)}")
        return {}

def save_json(file_path, data):
    """Save data to JSON file safely."""
    init_db()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Failed to save data to database file {os.path.basename(file_path)}: {str(e)}")
        return False

# USERS APIS
def get_all_users():
    return load_json(USERS_FILE)

def save_user(email, user_data):
    users = get_all_users()
    users[email.lower().strip()] = user_data
    return save_json(USERS_FILE, users)

def get_user_by_email(email):
    users = get_all_users()
    return users.get(email.lower().strip())

# TODOS APIS
def get_user_todos(email):
    """Get all todos for a given user email."""
    todos = load_json(TODOS_FILE)
    return todos.get(email.lower().strip(), [])

def save_user_todos(email, user_todos_list):
    """Save the full list of todos for a given user email."""
    todos = load_json(TODOS_FILE)
    todos[email.lower().strip()] = user_todos_list
    return save_json(TODOS_FILE, todos)

# HISTORY APIS
def get_user_history(email):
    """Get all history (deleted tasks) for a given user email."""
    history = load_json(HISTORY_FILE)
    return history.get(email.lower().strip(), [])

def save_user_history(email, user_history_list):
    """Save the full list of history tasks for a given user email."""
    history = load_json(HISTORY_FILE)
    history[email.lower().strip()] = user_history_list
    return save_json(HISTORY_FILE, history)
