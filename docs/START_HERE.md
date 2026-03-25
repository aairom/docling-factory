# 🚀 Quick Start Guide

## The Right Way to Run the App

### ✅ Method 1: Use the Launch Script (Easiest)

```bash
./scripts/launch.sh
```

That's it! The script handles everything automatically.

### ✅ Method 2: Manual Start (If you prefer)

```bash
# Step 1: Activate virtual environment
source venv/bin/activate

# Step 2: Run the app
python app_enhanced.py
```

### ❌ Common Mistake

**DON'T** run the app like this:
```bash
python app_enhanced.py  # ❌ WRONG - Missing venv activation
```

This will cause the "EasyOCR not installed" error!

---

## First Time Setup

If this is your first time running the app:

```bash
# 1. Create virtual environment (if not exists)
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start OpenSearch (for RAG features)
docker-compose up -d opensearch

# 5. Start Ollama (for LLM)
ollama serve

# 6. Launch the app
./scripts/launch.sh
```

---

## Launch Options

```bash
# Run in background
./scripts/launch.sh --detached

# Use custom port
./scripts/launch.sh --port 8080

# Enable GPU acceleration
./scripts/launch.sh --gpu

# Create public share link
./scripts/launch.sh --share

# Combine options
./scripts/launch.sh --detached --port 8080 --gpu
```

---

## Stopping the App

```bash
# If running in foreground: Press Ctrl+C

# If running in background:
./scripts/stop.sh
```

---

## Checking Status

```bash
./scripts/status.sh
```

---

## Troubleshooting

If you see any errors, check:
1. **TROUBLESHOOTING.md** - Common issues and solutions
2. **logs/app.log** - Application logs
3. **docs/QUICKSTART.md** - Detailed setup guide

---

## Key Points to Remember

1. ✅ **Always activate venv** before running the app manually
2. ✅ **Use `./scripts/launch.sh`** for hassle-free startup
3. ✅ **Check logs** if something goes wrong: `tail -f logs/app.log`
4. ❌ **Never run** `python app_enhanced.py` without activating venv first

---

## Quick Reference

| Task | Command |
|------|---------|
| Start app | `./scripts/launch.sh` |
| Stop app | `./scripts/stop.sh` |
| Check status | `./scripts/status.sh` |
| View logs | `tail -f logs/app.log` |
| Activate venv | `source venv/bin/activate` |
| Start OpenSearch | `docker-compose up -d opensearch` |
| Start Ollama | `ollama serve` |

---

## Need Help?

- 📖 Read **TROUBLESHOOTING.md** for common issues
- 📚 Check **docs/QUICKSTART.md** for detailed instructions
- 🏗️ Review **docs/ARCHITECTURE.md** to understand the system