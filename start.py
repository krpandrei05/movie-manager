#!/usr/bin/env python3
"""
Script pentru pornirea simultană a backend-ului și frontend-ului
Rulează ambele servere Flask în thread-uri separate
"""
import os
import sys
import threading
import time
from pathlib import Path

# Adăugăm directoarele în path
BASE_DIR = Path(__file__).parent.absolute()
BACKEND_DIR = BASE_DIR / 'backend'
FRONTEND_DIR = BASE_DIR / 'frontend'

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(FRONTEND_DIR))

def run_backend():
    """Pornește backend-ul Flask pe portul 5000"""
    os.chdir(BACKEND_DIR)
    from app import app
    from models.database import init_db
    
    print("🔧 Inițializare baza de date...")
    init_db()
    print("✅ Baza de date inițializată")
    
    print("🚀 Pornire backend API pe http://localhost:5000")
    app.run(debug=True, port=5000, use_reloader=False)

def run_frontend():
    """Pornește frontend-ul Flask pe portul 5001"""
    # Așteptăm puțin pentru ca backend-ul să pornească
    time.sleep(2)
    
    os.chdir(FRONTEND_DIR)
    from app import app
    
    print("🌐 Pornire frontend web pe http://localhost:5001")
    app.run(debug=True, port=5001, use_reloader=False)

if __name__ == '__main__':
    print("=" * 60)
    print("🎬 Movie Manager - Pornire servere")
    print("=" * 60)
    print()
    
    # Creăm thread-uri pentru ambele servere
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    
    # Pornim thread-urile
    backend_thread.start()
    frontend_thread.start()
    
    print()
    print("✅ Ambele servere rulează!")
    print()
    print("📡 Backend API:  http://localhost:5000")
    print("🌐 Frontend Web: http://localhost:5001")
    print()
    print("💡 Deschide browser-ul la: http://localhost:5001")
    print()
    print("⚠️  Apasă Ctrl+C pentru a opri serverele")
    print("=" * 60)
    print()
    
    try:
        # Așteptăm ca thread-urile să ruleze
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print("🛑 Oprire servere...")
        print("✅ Serverele au fost oprite")
        sys.exit(0)

