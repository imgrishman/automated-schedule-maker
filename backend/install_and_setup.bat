@echo off
echo 🚀 Installing Automated Schedule Planner Backend...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing Python packages...
pip install -r requirements.txt

REM Run database setup
echo 🗄️ Setting up MongoDB database...
python scripts\setup_database.py

REM Verify database
echo ✅ Verifying database setup...
python scripts\verify_database.py

echo 🎉 Installation completed successfully!
echo.
echo 🚀 To start the server:
echo    venv\Scripts\activate.bat
echo    python main.py
echo.
echo 🔗 API will be available at: http://localhost:8000
echo 📖 API docs at: http://localhost:8000/docs
pause
