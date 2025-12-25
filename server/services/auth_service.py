"""
Modul pentru logica de business pentru autentificare
Contine functiile pentru inregistrare si login
"""
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models.database import get_db_connection

# Functie pentru procesarea inregistrarii unui utilizator nou
def proceseaza_inregistrare():
    """
    Proceseaza cererea de inregistrare a unui utilizator nou
    Returns:
        JSON response cu mesaj de succes sau eroare
    """
    # Preluam datele din cerere
    date = request.get_json()
    
    # Verificam daca datele au fost trimise
    if not date:
        return jsonify({"message": "Missing data"}), 400
    
    nume = date.get('username')
    parola = date.get('password')
    
    # Verificam daca username si password au fost completate
    if not nume or not parola:
        return jsonify({"message": "Username and password are required"}), 400
    
    # Verificam daca valorile nu sunt goale dupa eliminarea spatiilor
    if not nume.strip() or not parola.strip():
        return jsonify({"message": "Username and password cannot be empty"}), 400
    
    conn = get_db_connection()
    try:
        # Criptam parola inainte de a o salva in baza de date
        parola_criptata = generate_password_hash(parola)
        
        # Introducem datele in tabelul users
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (nume, parola_criptata))
        conn.commit()
        return jsonify({"message": "User created"}), 201
    except sqlite3.IntegrityError:
        # Returnam eroare daca numele exista deja
        return jsonify({"message": "Username already exists"}), 400
    except Exception:
        # Returnam eroare pentru alte probleme
        return jsonify({"message": "Registration error"}), 400
    finally:
        # Inchidem conexiunea la baza de date
        conn.close()

# Functie pentru procesarea autentificarii unui utilizator
def proceseaza_login():
    """
    Proceseaza cererea de autentificare a unui utilizator
    Returns:
        JSON response cu token sau mesaj de eroare
    """
    # Preluam datele din cerere
    date = request.get_json()
    
    # Verificam daca datele au fost trimise
    if not date:
        return jsonify({"message": "Missing data"}), 400
    
    nume = date.get('username')
    parola = date.get('password')
    
    # Verificam daca username si password au fost completate
    if not nume or not parola:
        return jsonify({"message": "Username and password are required"}), 400
    
    conn = get_db_connection()
    
    # Cautam utilizatorul in baza de date doar dupa username
    user = conn.execute('SELECT * FROM users WHERE username = ?', (nume,)).fetchone()
    conn.close()
    
    # Verificam daca utilizatorul exista
    if user:
        # Verificam daca parola introdusa corespunde cu parola criptata din baza de date
        if check_password_hash(user['password'], parola):
            # Generam un token simplu pentru testare
            return jsonify({"token": "token_secret_pentru_" + nume}), 200
    
    # Returnam eroare daca username ul sau parola sunt invalide
    return jsonify({"message": "Incorrect username or password"}), 401

