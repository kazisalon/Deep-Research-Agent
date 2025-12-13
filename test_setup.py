#!/usr/bin/env python3
"""
Quick Test Script - Verify your setup without running the full agent
"""

import sys
from pathlib import Path

print("🧪 Deep Research Agent - Configuration Test\n")
print("="*60)

# Test 1: Check .env file
print("\n1️⃣  Checking .env file...")
env_file = Path(".env")
if env_file.exists():
    print("   ✅ .env file exists")
    
    # Check if keys are set
    with open(".env", "r") as f:
        content = f.read()
        
    if "YOUR_" in content.upper():
        print("   ⚠️  WARNING: API keys not set (still using placeholders)")
        print("   → Edit .env and replace YOUR_TAVILY_KEY_HERE with your actual key")
    else:
        print("   ✅ API keys appear to be set")
else:
    print("   ❌ .env file not found")
    print("   → Copy .env.example to .env and add your keys")

# Test 2: Check Python version
print("\n2️⃣  Checking Python version...")
version_info = sys.version_info
version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
print(f"   Python {version_str}")

if version_info.major == 3 and version_info.minor >= 10:
    print("   ✅ Python version OK (3.10+)")
elif version_info.major == 3 and version_info.minor == 9:
    print("   ⚠️  Python 3.9 - Upgrade to 3.10+ recommended")
else:
    print("   ❌ Python 3.10+ required")

# Test 3: Check dependencies
print("\n3️⃣  Checking installed packages...")
required_packages = [
    "langgraph",
    "langchain",
    "langchain_google_genai",
    "langchain_community",
    "tavily",
    "pydantic",
    "pydantic_settings",
    "dotenv"
]

missing = []
for package in required_packages:
    try:
        if package == "tavily":
            __import__("tavily")
        elif package == "dotenv":
            __import__("dotenv")
        elif package == "pydantic_settings":
            __import__("pydantic_settings")
        else:
            __import__(package.replace("-", "_"))
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NOT INSTALLED")
        missing.append(package)

if missing:
    print(f"\n   ⚠️  Missing packages: {', '.join(missing)}")
    print("   → Run: pip install -r requirements.txt")

# Test 4: Check project structure
print("\n4️⃣  Checking project structure...")
required_files = [
    "main.py",
    "config/settings.py",
    "src/agent/graph.py",
    "src/agent/nodes.py",
    "src/tools/search.py"
]

all_exist = True
for file_path in required_files:
    if Path(file_path).exists():
        print(f"   ✅ {file_path}")
    else:
        print(f"   ❌ {file_path} - MISSING")
        all_exist = False

# Final summary
print("\n" + "="*60)
if env_file.exists() and version_info.minor >= 9 and not missing and all_exist:
    if "YOUR_" in content.upper():
        print("⚠️  ALMOST READY - Just add your API keys to .env")
        print("\nNext step:")
        print("1. Edit .env file")
        print("2. Add your Tavily and Google API keys")
        print("3. Run: python main.py")
    else:
        print("✅ ALL CHECKS PASSED - Ready to run!")
        print("\nRun: python main.py")
else:
    print("⚠️  SETUP INCOMPLETE - See errors above")
print("="*60 + "\n")
