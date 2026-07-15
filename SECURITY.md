# 🔒 SECURITY.md - Data Protection Guide

## ✅ What's Protected

### Files NEVER Committed (in .gitignore):
```
.env                    # API keys
config/.env             # Environment variables
client_secret.json      # OAuth credentials
youtube_token.pickle    # YouTube auth token
*.pem, *.key            # Private keys
storage/output/*.mp4    # Generated videos
logs/*.log              # Logs (may contain sensitive data)
```

### Config Files (Safe to Commit):
```
config/settings.toml    # Only empty placeholders
config/.env.example     # Template only (no real keys)
```

---

## 🚨 BEFORE YOU PUSH - CHECKLIST

### 1. Check for Leaked Secrets
```bash
# Scan for API keys
git grep -i "api_key\|apikey\|secret\|token" -- "*.toml" "*.py" "*.md"

# Should only show:
# - Empty strings: api_key = ""
# - Placeholders: "your_api_key_here"
# - Comments: # Get key from...
```

### 2. Verify .gitignore
```bash
# Make sure .gitignore is committed
git ls-files | grep gitignore

# Should show: .gitignore
```

### 3. Check Staged Files
```bash
# See what will be pushed
git status
git diff --cached --name-only
```

### 4. Scan Entire Repo
```bash
# Search for common secret patterns
grep -r "sk_live_\|ghp_\|xoxb-\|AIza" . --exclude-dir=.git 2>/dev/null

# Should return nothing
```

---

## 🔐 API KEY MANAGEMENT

### Where to Store Keys:
```
✅ ~/.config/fact-fusion/.env         (global, user-specific)
✅ config/.env                        (local, gitignored)
✅ Environment variables              (CI/CD, production)
✅ Secret managers (1Password, etc.)  (recommended for teams)
```

### Where NOT to Store Keys:
```
❌ config/settings.toml               (committed to repo)
❌ Code files (*.py, *.js, etc.)
❌ README.md or documentation
❌ GitHub Issues or PRs
❌ Screenshots
```

---

## 🛡️ GITHUB SECURITY FEATURES

### Enable These (After Push):
1. **Secret Scanning** → Settings → Security → Enable
2. **Dependabot Alerts** → Settings → Security → Enable
3. **Branch Protection** → Settings → Branches → Add rule:
   - Branch: `main`
   - Require pull request reviews
   - Require status checks

### Optional: Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: detect-private-key
      - id: detect-aws-credentials
      - id: no-commit-to-branch
        args: ['--branch', 'main']
EOF

# Install hooks
pre-commit install
```

---

## 🚨 IF YOU ACCIDENTALLY COMMIT SECRETS

### 1. IMMEDIATE ACTION
```bash
# Revoke the leaked key IMMEDIATELY
# Go to: API provider dashboard → Revoke key → Generate new one
```

### 2. Remove from Git History
```bash
# Install BFG Repo-Cleaner
# Download: https://rtyley.github.io/bfg-repo-cleaner/

# Remove secrets from history
java -jar bfg.jar --delete-files .env
java -jar bfg.jar --replace-text passwords.txt

# Force push (WARNING: rewrites history!)
git push --force
```

### 3. Notify Users
```markdown
# SECURITY NOTICE

If you cloned this repo before [DATE], you may have exposed API keys.
Please:
1. Delete your local clone
2. Re-clone: git clone [repo-url]
3. Generate new API keys
4. Update your .env file
```

---

## 📋 SAFE WORKFLOW FOR USERS

### 1. Clone Repo
```bash
git clone https://github.com/saya4421/fact-fusion-automation.git
cd fact-fusion-automation
```

### 2. Create .env from Template
```bash
cp config/.env.example config/.env
```

### 3. Edit .env with Real Keys
```bash
# Edit config/.env (NEVER commit this!)
nano config/.env

# Add your real API keys:
GEMINI_API_KEY=your_real_key_here
PEXELS_API_KEY=your_real_key_here
```

### 4. Run the Tool
```bash
python scripts/batch_generate.py --topics 10
```

---

## ✅ VERIFICATION

### Before Pushing, Run This:
```bash
#!/bin/bash
# save as: scripts/verify-security.sh

echo "🔍 Scanning for secrets..."

# Check for real API keys (not placeholders)
if grep -r "api_key.*[a-zA-Z0-9]\{20,\}" --include="*.toml" --include="*.py" --include="*.md" . 2>/dev/null | grep -v "your_\|example\|placeholder"; then
    echo "❌ Potential API keys found!"
    exit 1
fi

# Check .env is gitignored
if git ls-files | grep -q "^\.env$"; then
    echo "❌ .env is tracked by git!"
    exit 1
fi

echo "✅ Security check passed!"
```

### Make Executable & Run:
```bash
chmod +x scripts/verify-security.sh
./scripts/verify-security.sh
```

---

## 🎯 SUMMARY

| Check | Status |
|-------|--------|
| .gitignore comprehensive | ✅ |
| No real API keys in code | ✅ |
| .env in gitignore | ✅ |
| OAuth tokens protected | ✅ |
| Security documentation | ✅ |

**This repo is SAFE to push to GitHub!** 🚀

---

**Last Updated:** 2026-07-15
**Verified By:** Fact Fusion Security Team