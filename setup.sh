#!/bin/bash

# JyotiGPT Dashboard Quick Start Script

set -e

echo "🚀 JyotiGPT Dashboard Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    
    # Generate a secure secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # Replace the secret key in .env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here-generate-with-python-secrets/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-here-generate-with-python-secrets/$SECRET_KEY/" .env
    fi
    
    echo "✅ .env file created with secure secret key"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and configure:"
    echo "   - ADMIN_PASSWORD"
    echo "   - OPENWEBUI_URL"
    echo "   - OPENWEBUI_ADMIN_TOKEN"
    echo "   - HF_TOKEN (optional)"
    echo "   - HF_SPACE_IDS (optional)"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials"
echo "2. Run: python app.py"
echo "3. Open: http://localhost:5000"
echo ""
echo "For production deployment, use:"
echo "  gunicorn -w 4 -b 0.0.0.0:5000 app:app"
echo ""
echo "Or with Docker:"
echo "  docker-compose up -d"
echo "================================"
