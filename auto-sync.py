#!/usr/bin/env python3
import subprocess
import os
from datetime import datetime

VAULT_DIR = os.path.expanduser("~/Downloads/estudos")
os.chdir(VAULT_DIR)

# Checa status
result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)

if result.stdout.strip():  # Se tem mudanças
    subprocess.run(["git", "add", "."])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["git", "commit", "-m", f"Auto-sync: {timestamp}"])
    subprocess.run(["git", "push", "origin", "main"])
    print(f"✓ Synced at {timestamp}")
else:
    print(f"No changes at {datetime.now().strftime('%H:%M:%S')}")
