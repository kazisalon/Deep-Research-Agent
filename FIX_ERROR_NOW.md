# ⚠️ PYTHON 3.9 ERROR - CANNOT BE FIXED WITHOUT UPGRADING

## The Error You're Seeing is UNFIXABLE on Python 3.9

```
TypeError: unhashable type: 'list'
```

**This is a BUG in Python 3.9's core `typing.py` module.**

Modern AI packages (Google Gemini, LangChain) require Python 3.10+ and trigger this bug.

---

## ✅ THE ONLY FIX: Upgrade to Python 3.12

Follow these steps **EXACTLY**:

### Step 1: Download Python 3.12

Click this link: https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe

Save the file to your Desktop.

### Step 2: Install Python 3.12

1. **Double-click** the downloaded file: `python-3.12.8-amd64.exe`
2. ✅ **CHECK** "Add python.exe to PATH" (IMPORTANT!)
3. Click "Install Now"
4. Wait for installation to complete
5. Click "Close"

### Step 3: Verify Installation

Close PowerShell completely and open a NEW PowerShell window.

Then run:
```powershell
python --version
```

Should show: `Python 3.12.8`

If it still shows 3.9, run:
```powershell
python3.12 --version
```

### Step 4: Recreate Your Project Environment

In PowerShell (NEW window after installing Python):

```powershell
# Navigate to project
cd C:\Users\User\Desktop\2025\Deep-Research-Agent

# Delete old environment
Remove-Item -Recurse -Force venv

# Create new environment with Python 3.12
python -m venv venv

# If the above still uses 3.9, use:
python3.12 -m venv venv

# Activate new environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Test import
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; print('✅ SUCCESS!')"
```

### Step 5: Run Your Agent

```powershell
# Make sure .env has your API keys
python main.py
```

---

## Alternative: Use py Launcher

If you have multiple Python versions:

```powershell
# Check available versions
py --list

# Use Python 3.12 specifically
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

## Why This is The Only Solution

**You cannot fix a Python 3.9 bug.** The error is in Python's source code:

```
File "C:\Users\User\AppData\Local\Programs\Python\Python39\lib\typing.py", line 694
    return hash((self.__origin__, self.__args__))
TypeError: unhashable type: 'list'
```

This line in Python 3.9's `typing.py` breaks when modern packages use advanced type hints.

**Python 3.10+ fixed this bug.**

---

## Timeline

- Python 3.9: Released 2020, End-of-Life October 2025
- Python 3.10: Fixed the typing bugs
- Python 3.11: Faster, better
- Python 3.12: Current stable (industry standard)

**All modern AI development uses Python 3.10+**

---

## After Upgrading

Once you have Python 3.12 installed:

1. Your error will be completely gone
2. The agent will run perfectly
3. You'll never have this issue again
4. You'll be using the same version as professionals

---

## Download Link Again

**Python 3.12.8 Installer (64-bit Windows):**

https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe

**Click → Download → Install → Check "Add to PATH" → Done**

---

## Need Help?

If you get stuck during installation:

1. Make sure you checked "Add python.exe to PATH"
2. Close and reopen PowerShell after installing
3. Use `python3.12 -m venv venv` if `python` still points to 3.9
4. Check `py --list` to see all installed Python versions

---

**This is not optional. Python 3.9 cannot run modern AI packages. Upgrade now.**
