# 🚀 PUSH TO GITHUB - MANUAL INSTRCTIONS

Repo udah dibuat lokal di: `~/Projects/fact-fusion-automation/`

## OPTION 1: HTTPS (Recommended)

```bash
cd ~/Projects/fact-fusion-automation

# Add remote (if not already added)
git remote add origin https://github.com/saya4421/fact-fusion-automation.git

# Push ke GitHub
git push -u origin main

# Masukkan GitHub username & token
# Token: https://github.com/settings/tokens (scope: repo)
```

---

## OPTION 2: SSH (If you have SSH key setup)

```bash
cd ~/Projects/fact-fusion-automation

# Remove HTTPS remote
git remote remove origin

# Add SSH remote
git remote add origin git@github.com:saya4421/fact-fusion-automation.git

# Push ke GitHub
git push -u origin main
```

---

## OPTION 3: GitHub CLI (Easiest!)

```bash
# Install gh CLI (if not installed)
sudo dnf install -y gh

# Login
gh auth login

# Create repo & push
cd ~/Projects/fact-fusion-automation
gh repo create fact-fusion-automation --public --source=. --push
```

---

## ✅ AFTER PUSH:

1. Go to: https://github.com/saya4421/fact-fusion-automation
2. Verify all files uploaded
3. README.md should render beautifully
4. Share repo link!

---

## 📋 NEXT STEPS (Development):

### Phase 1: Copy Core from MoneyPrinter
```bash
# Copy video generation engine
cp -r ~/Projects/MoneyPrinterTurbo/app/services/video.py ~/Projects/fact-fusion-automation/app/services/
cp -r ~/Projects/MoneyPrinterTurbo/app/models/ ~/Projects/fact-fusion-automation/app/
```

### Phase 2: Integrate Piper TTS from Viral-Faceless
```bash
# Copy Piper service
cp -r ~/Projects/Viral-Faceless-Shorts-Generator/piper/ ~/Projects/fact-fusion-automation/services/
```

### Phase 3: Add Google Trends Scraper
```bash
# Copy trends scraper
cp -r ~/Projects/Viral-Faceless-Shorts-Generator/trendscraper/ ~/Projects/fact-fusion-automation/services/
```

### Phase 4: YouTube Upload Integration
```bash
# OAuth already configured at ~/.config/google/
# Just implement upload service
```

---

**Repo Blueprint DONE! Tinggal push & develop!** 🚀