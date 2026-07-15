# Smart Todo Manager

A production-ready, beautiful, and responsive **Todo List Management System** built with Python Streamlit. The application features a glassmorphic modern UI design, secure user authentication (with password hashing), custom multi-page navigation control, JSON-based storage (no SQL server needed), and full deployment configuration ready for Render.

## 🚀 Key Features

*   **🔒 Secure Auth System**: Secure user sign up & sign in with password hashing powered by `bcrypt`.
*   **🏠 Modern Dashboard**: responsive metric cards (Total, Pending, Completed, Deleted tasks) and tasks breakdown analysis charts.
*   **✅ Tasks List (CRUD)**: Create, edit, complete, delete, search, sort, and filter tasks.
*   **🕒 History & Archiving**: Whenever you delete a task, it's moved from the active list to history. You can restore it, permanently delete it, or empty your entire history.
*   **👤 User Profile Settings**: Update your display name and email address securely (with duplicate checking and database transfer), or change your password.
*   **⚙ App Customization**: Toggle between dynamic **Dark Mode** and **Light Mode** overrides instantly.
*   **📂 Corruption Handling**: Automatically restores corrupted database files and initializes a safe default structure.

---

## 📂 Project Structure

```text
TodoManager/
│
├── .streamlit/
│   └── config.toml          # Custom theme configuration (hides native sidebar menu)
│
├── assets/
│   ├── style.css            # Custom CSS styles (glassmorphic panels, badge tags, buttons)
│   └── logo.png             # Modern 3D digital art checkmark logo asset
│
├── database/
│   ├── users.json           # Stores encrypted user records
│   ├── todos.json           # Stores active todo tasks
│   └── history.json         # Stores deleted historical tasks
│
├── pages/
│   ├── dashboard.py         # Home KPIs and analytics graph
│   ├── todos.py             # Active task management and details editing
│   ├── history.py           # Trash bin with restore / clear triggers
│   ├── profile.py           # Personal name / password updater
│   └── settings.py          # Dark/Light toggles and mock filters
│
├── utils/
│   ├── auth.py              # Password hashing and account validation mechanics
│   ├── database.py          # Read / write JSON helpers and database bootstrap
│   └── helpers.py           # Shared navigation layout and layout settings
│
├── .env                     # App environment configuration variables (not committed)
├── .env.example             # Environment config template
├── .gitignore               # Ignored local databases and cache folders
├── app.py                   # Main entrance (Login/Registration panel redirector)
├── README.md                # Deployment and installation manual
└── requirements.txt         # Package dependency freeze
```

---

## 🛠 Local Setup & Running

Follow these simple steps to run the application on your computer:

### 1. Clone the repository
Clone your code files into a local folder:
```bash
git clone <your-repository-url>
cd todoai
```

### 2. Set up Virtual Environment
Create and activate a virtual environment:
```bash
# Windows Power Shell / Command Prompt
python -m venv venv
venv\Scripts\activate

# macOS / Linux Terminal
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all package packages listed inside `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Create Environmental Settings
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Inside `.env`, configure your values:
```env
SECRET_KEY=some_unique_secret_key_here
APP_NAME=Smart Todo Manager
```

### 5. Launch the Application
Run the Streamlit server command:
```bash
streamlit run app.py
```
Your default browser will launch and display the page at: [http://localhost:8501](http://localhost:8501).

---

## ☁ Deploying to Render

This repository is optimized for deployment to **Render** as a web service.

### Step-by-Step Render Deployment Guide

1.  **Commit and push** your files to a GitHub repository (excluding files in the `database/` folder and `.env`, which are already filtered in `.gitignore`).
2.  Log in to [Render Dashboard](https://dashboard.render.com/) and click **New > Web Service**.
3.  Connect your GitHub repository.
4.  Configure the Web Service options:
    *   **Name**: `smart-todo-manager` (or custom name)
    *   **Environment**: `Python 3`
    *   **Region**: Select a region close to your target users (e.g. Oregon, Frankfurt)
    *   **Branch**: `main`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5.  Set Environment Variables:
    *   Scroll down and click **Advanced**.
    *   Click **Add Environment Variable**:
        *   `SECRET_KEY` = `your_render_production_secret_key_123`
        *   `APP_NAME` = `Smart Todo Manager`
6.  Click **Deploy Web Service** and wait for the build process to finish. Once built, copy the public URL provided by Render to access your app from anywhere!
