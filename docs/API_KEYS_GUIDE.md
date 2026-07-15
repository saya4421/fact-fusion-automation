# 🔑 API Keys Setup Guide

Quick guide untuk mendapatkan semua API keys yang dibutuhkan.

---

## ✅ REQUIRED (WAJIB)

### 1. **Pexels API** (FREE - Unlimited)
**Untuk:** Stock footage/video clips

**Cara Dapatkan:**
1. Buka https://www.pexels.com/api/
2. Click "Sign Up" (gratis)
3. Login dengan Google/email
4. Go to API section
5. Copy API key

**Time:** 3 menit  
**Cost:** FREE  
**Limit:** Unlimited untuk personal use

**Add to `.env`:**
```env
PEXELS_API_KEY="your_pexels_api_key_here"
```

---

### 2. **Gemini API** (FREE Tier)
**Untuk:** AI script generation

**Cara Dapatkan:**
1. Buka https://makersuite.google.com/app/apikey
2. Login dengan Google account
3. Click "Create API Key"
4. Copy key

**Time:** 2 menit  
**Cost:** FREE (60 requests/minute)  
**Limit:** Cukup untuk 100+ videos/hari

**Add to `.env`:**
```env
GEMINI_API_KEY="your_gemini_api_key_here"
GEMINI_MODEL="gemini-1.5-flash"
```

---

## ⚠️ OPTIONAL (TAMBAHAN)

### 3. **Edge TTS** (FREE - No API Key!)
**Untuk:** Text-to-Speech (fallback Piper)

**Setup:** Tidak perlu API key!  
Sudah included di `requirements.txt`

**Add to `.env`:**
```env
TTS_PROVIDER="edge"
EDGE_VOICE="en-US-GuyNeural"
```

---

### 4. **Piper TTS** (FREE - Offline)
**Untuk:** Text-to-Speech (best quality, offline)

**Setup:** Run Docker container
```bash
docker-compose up -d piper
```

**Add to `.env`:**
```env
TTS_PROVIDER="piper"
PIPER_VOICE="en_US-lessac-medium"
PIPER_LANGUAGE="en"
```

---

### 5. **YouTube OAuth2** (FREE)
**Untuk:** Auto-upload ke YouTube

**Cara Setup:**
1. Buka https://console.cloud.google.com/
2. Create new project
3. Enable "YouTube Data API v3"
4. Go to Credentials → Create OAuth2 Client ID
5. Download `client_secret.json`
6. Run auth flow (lihat `INSTALL.md`)

**Time:** 10 menit  
**Cost:** FREE  
**Limit:** 10,000 units/day (cukup untuk 500+ uploads)

**Add to `.env`:**
```env
YOUTUBE_CLIENT_SECRET="path/to/client_secret.json"
YOUTUBE_TOKEN="path/to/token.pickle"
```

---

### 6. **TikTok API** (FREE - Developer)
**Untuk:** Auto-upload ke TikTok

**Cara Setup:**
1. Buka https://developers.tiktok.com/
2. Register as developer
3. Create app
4. Get API credentials

**Time:** 15 menit  
**Cost:** FREE  
**Note:** Approval required (bisa pakai manual upload sambil tunggu)

---

### 7. **Instagram Graph API** (FREE)
**Untuk:** Auto-upload ke Reels

**Cara Setup:**
1. Buka https://developers.facebook.com/
2. Create app
3. Add Instagram Graph API
4. Get access token

**Time:** 15 menit  
**Cost:** FREE  
**Note:** Butuh Instagram Business account

---

## 📋 QUICK START (5 MENIT!)

**Minimal untuk mulai:**
```bash
# 1. Dapatkan Pexels API key (3 min)
# 2. Dapatkan Gemini API key (2 min)

# 3. Copy template
cp config/.env.example config/.env

# 4. Edit .env
nano config/.env

# 5. Paste API keys
PEXELS_API_KEY="pe_xxxxxxxxxxxxxxxxxxxxx"
GEMINI_API_KEY="xxxxxxxxxxxxxxxxxxxxx"

# 6. Save & test
python scripts/batch_generate.py --topics 1 --duration 30
```

**That's it!** 🎉

---

## 🆓 SEMUA FREE?

**YES!** Semua API yang required adalah FREE:

| API | Cost | Limit |
|-----|------|-------|
| Pexels | FREE | Unlimited |
| Gemini | FREE | 60 req/min |
| Edge TTS | FREE | Unlimited |
| Piper TTS | FREE | Offline |
| YouTube | FREE | 500+ uploads/day |

**Total Cost: $0** 💰

---

## 💡 TIPS

1. **Jangan commit `.env` ke GitHub!** (udah di `.gitignore`)
2. **Backup API keys** di password manager
3. **Rotate keys** setiap 3-6 bulan untuk security
4. **Monitor usage** di dashboard masing-masing provider

---

## 🆘 TROUBLESHOOTING

### "Invalid API key"
- Check ada typo di `.env`
- Pastikan no quotes di sekitar key
- Restart script setelah edit `.env`

### "Rate limit exceeded"
- Tunggu beberapa menit
- Upgrade ke paid tier (optional)
- Reduce batch size

### "Service unavailable"
- Check internet connection
- Check proxy setting (kalo di warnet)
- Restart Docker services

---

## 📞 SUPPORT

Masalah setup API keys?  
Buka issue di GitHub atau baca `INSTALL.md` untuk detailed guide.