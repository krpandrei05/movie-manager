#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import threading
from pathlib import Path

# Adaugam directoarele in path
BASE_DIR = Path(__file__).parent.absolute()
BACKEND_DIR = BASE_DIR / 'backend'
FRONTEND_DIR = BASE_DIR / 'frontend'

def run_backend():
    # Porneste backend-ul Flask pe portul 5000
    os.chdir(BACKEND_DIR)
    # Rulam app.py din backend
    return subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=str(BACKEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

def run_frontend():
    # Porneste frontend-ul Flask pe portul 5001
    os.chdir(FRONTEND_DIR)
    # Rulam app.py din frontend
    return subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=str(FRONTEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

if __name__ == '__main__':    
    processes = []
    
    try:
        # Pornim backend-ul
        print("Pornire backend API...")
        backend_process = run_backend()
        processes.append(('Backend', backend_process))
        time.sleep(2)  # Asteptam ca backend-ul sa porneasca
        
        # Pornim frontend-ul
        print("Pornire frontend web...")
        frontend_process = run_frontend()
        processes.append(('Frontend', frontend_process))
        time.sleep(2)  # Asteptam ca frontend-ul sa porneasca
        
        print()
        print("Ambele servere rulează!")
        print()
        print("Backend API:  http://localhost:5000")
        print("Frontend Web: http://localhost:5001")
        print()
        print("Deschide browser-ul la: http://localhost:5001")
        print()
        
        # Afisam output-ul proceselor
        def monitor_process(name, process):
            for line in iter(process.stdout.readline, ''):
                if line:
                    print(f"[{name}] {line.rstrip()}")
        
        threads = []
        for name, process in processes:
            thread = threading.Thread(target=monitor_process, args=(name, process), daemon=True)
            thread.start()
            threads.append(thread)
        
        # Asteptam ca procesele sa ruleze
        while all(p.poll() is None for _, p in processes):
            time.sleep(1)
            
    except KeyboardInterrupt:
        print()
        print("Oprire servere...")
        for name, process in processes:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        sys.exit(0)

