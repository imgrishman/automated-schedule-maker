#!/bin/bash

echo "🚀 Installing Automated Schedule Planner Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Run database setup
echo "🗄️ Setting up MongoDB database..."
python scripts/setup_database.py

# Verify database
echo "✅ Verifying database setup..."
python scripts/verify_database.py

echo "🎉 Installation completed successfully!"
echo ""
echo "🚀 To start the server:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "🔗 API will be available at: http://localhost:8000"
echo "📖 API docs at: http://localhost:8000/docs"
