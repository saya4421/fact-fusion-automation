# 📦 Installation Guide

## Quick Start

### 1. Clone Repo
```bash
git clone https://github.com/saya4421/fact-fusion-automation.git
cd fact-fusion-automation
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** Installation may take 5-10 minutes depending on your internet connection.

### 4. Setup Configuration
```bash
cp config/.env.example config/.env
nano config/.env
```

Edit with your API keys:
- `GEMINI_API_KEY` - Get from https://aistudio.google.com/app/apikey (FREE)
- `PPEXELS_API_KEY` - Get from https://www.pexels.com/api/ (FREE)

### 5. Test Installation
```bash
python scripts/verify_security.py
```

If all checks pass, you're ready to go! 🚀

---

## Optional Dependencies

### Piper TTS (FREE, offline)
```bash
# Commented out in requirements.txt due to complex dependencies
# Install manually if needed:
pip install piper-tts
```

### Aeneas (Subtitle alignment)
```bash
# Commented out in requirements.txt
# Install manually if needed:
pip install aeneas
# Requires: numpy, ffmpeg, espeak
```

---

## Troubleshooting

### Issue: numpy error when installing aeneas
**Solution:** Install numpy first:
```bash
pip install numpy
pip install aeneas
```

### Issue: ffmpeg not found
**Solution:** Install ffmpeg:
```bash
# Linux
sudo dnf install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Issue: Slow installation
**Solution:** Use a faster PyPI mirror:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## Next Steps

After installation:
1. Read [README.md](README.md) for features overview
2. Read [SECURITY.md](SECURITY.md) for security best practices
3. Run your first batch: `python scripts/batch_generate.py --topics 5`

Happy automating! 🎉