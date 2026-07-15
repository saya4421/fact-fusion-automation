#!/bin/bash
# Fact Fusion Automation - Smart Install Script for Fedora
# Author: Ironclaw V7
# Usage: ./INSTALL_FEDORA_SMART.sh

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║   Fact Fusion Automation - Smart Installer         ║"
echo "║   Fedora Edition (WiFi-friendly)                   ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if running in project directory
if [ ! -f "requirements.txt" ]; then
    log_error "Please run this script from the project root directory"
    exit 1
fi

# Step 1: Check Python version
log_info "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
log_info "Python version: $PYTHON_VERSION"

# Step 2: Create virtual environment
log_info "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    log_info "Virtual environment created"
else
    log_info "Virtual environment already exists"
fi

# Step 3: Activate virtual environment
log_info "Activating virtual environment..."
source .venv/bin/activate

# Step 4: Upgrade pip (with retry for slow WiFi)
log_info "Upgrading pip (this may take a while on slow WiFi)..."
for i in {1..3}; do
    if pip install --upgrade pip -q; then
        log_info "Pip upgraded successfully"
        break
    else
        log_warn "Attempt $i failed, retrying..."
        sleep 5
    fi
done

# Step 5: Install core dependencies (split into batches for slow WiFi)
log_info "Installing core dependencies (batch 1/3)..."
pip install numpy>=1.24.0 Pillow>=9.0.0 requests>=2.28.0 toml>=0.10.0 -q

log_info "Installing video dependencies (batch 2/3)..."
pip install moviepy==1.0.3 ffmpeg-python>=0.2.0 -q

log_info "Installing AI & TTS dependencies (batch 3/3)..."
pip install google-generativeai>=0.3.0 openai>=1.0.0 edge-tts>=6.1.0 -q

log_info "Installing upload dependencies..."
pip install google-api-python-client>=2.0.0 google-auth-httplib2>=0.1.0 google-auth-oauthlib>=0.4.0 -q

log_info "Installing utilities..."
pip install tqdm>=4.65.0 pytz>=2023.0 python-dotenv>=1.0.0 pydantic>=2.0.0 -q

log_info "Installing Web UI (optional)..."
pip install fastapi>=0.100.0 uvicorn>=0.23.0 python-multipart>=0.0.6 -q

# Step 6: Check FFmpeg
log_info "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n1)
    log_info "FFmpeg found: $FFMPEG_VERSION"
else
    log_warn "FFmpeg not found! Installing..."
    if command -v dnf &> /dev/null; then
        sudo dnf install -y ffmpeg
        log_info "FFmpeg installed"
    else
        log_error "Cannot install FFmpeg automatically. Please install manually:"
        echo "  sudo dnf install ffmpeg"
        exit 1
    fi
fi

# Step 7: Create .env from example
log_info "Setting up configuration..."
if [ ! -f "config/.env" ]; then
    cp config/.env.example config/.env
    log_info "Created config/.env from template"
    log_warn "IMPORTANT: Edit config/.env and add your API keys!"
    echo ""
    echo "Required API keys:"
    echo "  - PEXELS_API_KEY (FREE): https://www.pexels.com/api/"
    echo "  - GEMINI_API_KEY (FREE): https://makersuite.google.com/app/apikey"
    echo ""
else
    log_info "config/.env already exists"
fi

# Step 8: Create output directories
log_info "Creating output directories..."
mkdir -p output/videos output/audio output/subtitles
log_info "Directories created"

# Step 9: Show summary
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║            INSTALLATION COMPLETE! 🎉               ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "✅ Core dependencies installed"
echo "✅ Video engine ready"
echo "✅ TTS (Edge) ready"
echo "✅ Upload services ready"
echo "✅ FFmpeg installed"
echo ""
echo "⚠️  NEXT STEPS:"
echo ""
echo "1. Edit config/.env and add your API keys:"
echo "   nano config/.env"
echo ""
echo "2. Get FREE API keys:"
echo "   - Pexels: https://www.pexels.com/api/"
echo "   - Gemini: https://makersuite.google.com/app/apikey"
echo ""
echo "3. Test generate 1 video:"
echo "   source .venv/bin/activate"
echo "   python scripts/batch_generate.py --topics 1 --duration 30"
echo ""
echo "4. (Optional) Setup YouTube OAuth2 for auto-upload:"
echo "   See INSTALL.md for detailed instructions"
echo ""
echo "💡 TIPS FOR SLOW WIFI:"
echo "   - Dependencies are now cached in .venv/"
echo "   - Next installs will be faster"
echo "   - Use 'proxyon' if you're on Axis warnet"
echo ""
echo "🚀 Ready to create videos!"
echo ""