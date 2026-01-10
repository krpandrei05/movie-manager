"""
Modul pentru gestionarea bazei de date SQLite
Contine functiile pentru conexiune si initializarea tabelelor
"""
import sqlite3
import os

# Calea catre baza de date (in folderul instance)
# Calculam calea relativa la directorul server
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'production.db')

# Functie pentru deschiderea conexiunii la baza de date
def get_db_connection():
    """
    Deschide o conexiune la baza de date SQLite
    Returneaza: conexiunea la baza de date configurata cu row_factory
    """
    # Cream directorul instance daca nu exista
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Cream fisierul bazei de date local
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Crearea tabelelor la pornirea serverului
def init_db():
    """
    Initializeaza baza de date creand toate tabelele necesare
    """
    conn = get_db_connection()
    
    # Cream tabelele users si movies daca nu exista deja
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, status TEXT, rating TEXT)')
    
    # Cream tabelul pentru prieteni (relatie bidirectionala)
    conn.execute('CREATE TABLE IF NOT EXISTS friends (id INTEGER PRIMARY KEY, user_id INTEGER, friend_id INTEGER, UNIQUE(user_id, friend_id))')
    
    # Cream tabelul pentru recomandari
    conn.execute('CREATE TABLE IF NOT EXISTS recommendations (id INTEGER PRIMARY KEY, from_user_id INTEGER, to_user_id INTEGER, movie_title TEXT)')
    
    conn.commit()
    conn.close()

