# 🚀 Installation Guide - Automated Schedule Planner Backend

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for MongoDB Atlas)

## Quick Installation

### Option 1: Automatic Setup (Recommended)

\`\`\`bash
# Navigate to backend directory
cd backend

# Run quick setup
python quick_setup.py
\`\`\`

### Option 2: Manual Installation

#### Step 1: Install Dependencies

\`\`\`bash
# Install Python packages
pip install -r requirements.txt
\`\`\`

If you get permission errors, try:
\`\`\`bash
pip install --user -r requirements.txt
\`\`\`

#### Step 2: Set Up Database

\`\`\`bash
# Create database and seed data
python scripts/setup_database.py
\`\`\`

#### Step 3: Verify Installation

\`\`\`bash
# Verify everything is working
python scripts/verify_database.py
\`\`\`

#### Step 4: Start Server

\`\`\`bash
# Start the FastAPI server
python main.py
\`\`\`

## Using Virtual Environment (Recommended)

### Linux/Mac:
\`\`\`bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup
python scripts/setup_database.py

# Start server
python main.py
\`\`\`

### Windows:
\`\`\`batch
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run setup
python scripts\setup_database.py

# Start server
python main.py
