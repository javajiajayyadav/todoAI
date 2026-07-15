import re
import bcrypt
import streamlit as st
from utils.database import (
    get_user_by_email,
    save_user,
    get_all_users,
    save_json,
    USERS_FILE,
    load_json,
    TODOS_FILE,
    HISTORY_FILE
)

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password using bcrypt."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def validate_email(email: str) -> bool:
    """Basic regular expression check for email formatting."""
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return bool(re.match(regex, email))

def register_user(username, email, password, confirm_password):
    """Register a new user after validation."""
    username = username.strip()
    email = email.lower().strip()
    
    # 1. Validation for empty fields
    if not username or not email or not password or not confirm_password:
        return False, "All fields are required!"
        
    # 2. Email formatting validation
    if not validate_email(email):
        return False, "Please enter a valid email address!"
        
    # 3. Password length check
    if len(password) < 6:
        return False, "Password must be at least 6 characters long!"
        
    # 4. Confirm password match check
    if password != confirm_password:
        return False, "Passwords do not match!"
        
    # 5. Email uniqueness check
    if get_user_by_email(email) is not None:
        return False, "An account with this email already exists!"
        
    # 6. Save user to database
    user_data = {
        "username": username,
        "email": email,
        "password": hash_password(password),
        "name": username,  # Default display name
        "created_at": datetime_now_str()
    }
    
    if save_user(email, user_data):
        return True, "Registration successful! You can now log in."
    else:
        return False, "Failed to register. Please try again."

def login_user(email, password):
    """Verify credentials and login user."""
    email = email.lower().strip()
    
    if not email or not password:
        return False, "Please enter both email and password!", None
        
    user = get_user_by_email(email)
    if not user:
        return False, "Invalid email or password!", None
        
    if verify_password(password, user["password"]):
        return True, "Login successful!", user
    else:
        return False, "Invalid email or password!", None

def change_user_password(email, old_password, new_password, confirm_password):
    """Update user password after verification."""
    email = email.lower().strip()
    
    if not old_password or not new_password or not confirm_password:
        return False, "All password fields are required!"
        
    user = get_user_by_email(email)
    if not user:
        return False, "User not found!"
        
    if not verify_password(old_password, user["password"]):
        return False, "Incorrect current password!"
        
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long!"
        
    if new_password != confirm_password:
        return False, "New passwords do not match!"
        
    user["password"] = hash_password(new_password)
    if save_user(email, user):
        return True, "Password updated successfully!"
    return False, "Failed to update password. Please try again."

def update_user_profile(old_email, new_name, new_email):
    """Update profile details (name and email) and transfer database keys if email changes."""
    old_email = old_email.lower().strip()
    new_email = new_email.lower().strip()
    new_name = new_name.strip()
    
    if not new_name or not new_email:
        return False, "Name and Email cannot be empty!"
        
    if not validate_email(new_email):
        return False, "Please enter a valid email address!"
        
    user = get_user_by_email(old_email)
    if not user:
        return False, "User not found!"
        
    # Email change transaction
    if old_email != new_email:
        # Verify unique
        if get_user_by_email(new_email) is not None:
            return False, "Email address is already in use by another account!"
            
        # Update email in user dictionary
        user["email"] = new_email
        user["name"] = new_name
        
        # Load and write users json
        users = get_all_users()
        users[new_email] = user
        del users[old_email]
        
        if not save_json(USERS_FILE, users):
            return False, "Failed to update database profile details."
            
        # Transfer todos
        todos = load_json(TODOS_FILE)
        if old_email in todos:
            todos[new_email] = todos[old_email]
            del todos[old_email]
            save_json(TODOS_FILE, todos)
            
        # Transfer history
        history = load_json(HISTORY_FILE)
        if old_email in history:
            history[new_email] = history[old_email]
            del history[old_email]
            save_json(HISTORY_FILE, history)
            
        return True, "Profile details updated successfully!"
        
    else:
        # Standard name-only update
        user["name"] = new_name
        if save_user(old_email, user):
            return True, "Profile details updated successfully!"
        return False, "Failed to update profile details."

def datetime_now_str():
    from datetime import datetime
    return datetime.now().isoformat()
