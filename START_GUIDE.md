# ArcherySec - Simple Startup Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Open PowerShell in Project Directory
```powershell
cd c:\Users\NARASIMMAN\OneDrive\Desktop\projects\ISM\archerysec-master
```

### Step 2: Start the Application
```powershell
.\run.bat
```

### Step 3: Access the Application
Open your browser and go to:
- **URL**: http://localhost:8000/

---

## 📝 Alternative Methods

### Method A: Using Poetry (Recommended)
```powershell
poetry run python manage.py runserver 0.0.0.0:8000
```

### Method B: Using Virtual Environment
```powershell
.\venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

### Method C: Using Python Directly
```powershell
python manage.py runserver 0.0.0.0:8000
```

---

## 🛑 How to Stop the Server

Press `Ctrl + C` in the terminal window

---

## 🔐 First Time Setup (If Needed)

If this is your first time running the application, you may need to:

### 1. Install Dependencies (One-time)
```powershell
poetry install
```

### 2. Run Database Migrations (One-time)
```powershell
poetry run python manage.py migrate
```

### 3. Create Admin User (One-time)

**Option A: Using the initialization script**
```powershell
# First, initialize roles and organizations
poetry run python init_database.py

# Then create superuser
poetry run python manage.py createsuperuser
```

When prompted, enter:
- **Email**: your@email.com
- **Name**: Your Name
- **Role**: `1` (for Admin)
- **Organization**: `1` (for Default Organization)
- **Password**: YourSecurePassword

**Option B: Quick setup with environment variables**
```powershell
$env:NAME="Admin User"
$env:EMAIL="admin@archerysec.local"
$env:PASSWORD="Admin@123"
.\setup.bat
```

---

## ✅ Verification

After starting the server, you should see:
```
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```

---

## 🌐 Access Points

- **Main Application**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/

---

## 🆘 Troubleshooting

### Port Already in Use
If port 8000 is already in use, run on a different port:
```powershell
poetry run python manage.py runserver 0.0.0.0:8080
```

### Database Errors
Reset the database:
```powershell
poetry run python manage.py migrate
```

### Missing Dependencies
Reinstall dependencies:
```powershell
poetry install
```

---

## 📌 Summary

**Simplest way to start:**
1. Open PowerShell
2. Navigate to project folder
3. Run `.\run.bat`
4. Open http://localhost:8000/

That's it! 🎉
