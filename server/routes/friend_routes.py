"""
Modul pentru rutele legate de prieteni (/friends, /friends/<username>/movies, /recommendations)
"""
from flask import Blueprint, request, jsonify
import sqlite3
from models.database import get_db_connection
from security import verifica_token

# Cream un Blueprint pentru rutele de prieteni
friend_bp = Blueprint('friends', __name__)

# Ruta pentru obtinerea listei de prieteni
@friend_bp.route('/friends', methods=['GET'])
def get_friends():
    """
    Endpoint pentru obtinerea listei de prieteni ai utilizatorului curent
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    conn = get_db_connection()
    
    # Preluam toti prietenii utilizatorului (relatie bidirectionala)
    # Cautam atat prietenii unde user_id = id_user, cat si unde friend_id = id_user
    prieteni = conn.execute('''
        SELECT DISTINCT u.username 
        FROM users u
        INNER JOIN friends f ON (f.friend_id = u.id AND f.user_id = ?) OR (f.user_id = u.id AND f.friend_id = ?)
        WHERE u.id != ?
    ''', (id_user, id_user, id_user)).fetchall()
    
    conn.close()
    
    # Organizam prietenii intr-o lista
    lista_prieteni = [prieten['username'] for prieten in prieteni]
    
    return jsonify(lista_prieteni), 200

# Ruta pentru adaugarea unui prieten
@friend_bp.route('/friends/add', methods=['POST'])
def add_friend():
    """
    Endpoint pentru adaugarea unui prieten nou
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    # Preluam datele din cerere
    date = request.get_json()
    
    # Verificam daca datele au fost trimise
    if not date:
        return jsonify({'message': 'Date lipsa'}), 400
    
    nume_prieten = date.get('friend_username')
    
    # Verificam daca numele prietenului a fost completat
    if not nume_prieten or not nume_prieten.strip():
        return jsonify({'message': 'Numele prietenului este obligatoriu'}), 400
    
    conn = get_db_connection()
    
    # Cautam utilizatorul prieten in baza de date
    prieten = conn.execute('SELECT id FROM users WHERE username = ?', (nume_prieten,)).fetchone()
    
    if not prieten:
        conn.close()
        return jsonify({'message': 'Utilizator negasit'}), 404
    
    id_prieten = prieten['id']
    
    # Verificam daca nu incearca sa se adauge pe sine
    if id_user == id_prieten:
        conn.close()
        return jsonify({'message': 'Nu te poti adauga pe tine insuti'}), 400
    
    # Verificam daca prietenia exista deja
    prietenie_existenta = conn.execute('SELECT id FROM friends WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)', 
                                      (id_user, id_prieten, id_prieten, id_user)).fetchone()
    
    if prietenie_existenta:
        conn.close()
        return jsonify({'message': 'Prietenia exista deja'}), 400
    
    try:
        # Adaugam prietenia (bidirectionala)
        conn.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (id_user, id_prieten))
        conn.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (id_prieten, id_user))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Prieten adaugat'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'message': 'Prietenia exista deja'}), 400
    except Exception:
        conn.close()
        return jsonify({'message': 'Eroare la adaugarea prietenului'}), 400

# Ruta pentru vizualizarea filmelor unui prieten
@friend_bp.route('/friends/<friend_username>/movies', methods=['GET'])
def get_friend_movies(friend_username):
    """
    Endpoint pentru obtinerea filmelor unui prieten (toate listele: To Watch, Watching, Completed)
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    conn = get_db_connection()
    
    # Cautam utilizatorul prieten in baza de date
    prieten = conn.execute('SELECT id FROM users WHERE username = ?', (friend_username,)).fetchone()
    
    if not prieten:
        conn.close()
        return jsonify({'message': 'Utilizator negasit'}), 404
    
    id_prieten = prieten['id']
    
    # Verificam daca exista prietenia
    prietenie = conn.execute('SELECT id FROM friends WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)', 
                            (id_user, id_prieten, id_prieten, id_user)).fetchone()
    
    if not prietenie:
        conn.close()
        return jsonify({'message': 'Nu sunteti prieteni'}), 403
    
    # Preluam toate filmele prietenului, grupate pe status
    date_filme = conn.execute('SELECT id, title, status, rating FROM movies WHERE user_id = ? ORDER BY status, title', 
                              (id_prieten,)).fetchall()
    conn.close()
    
    # Organizam filmele pe liste (To Watch, Watching, Completed)
    filme = {
        'To Watch': [],
        'Watching': [],
        'Completed': []
    }
    
    for rand in date_filme:
        status = rand['status']
        if status in filme:
            filme[status].append({
                'id': rand['id'],
                'title': rand['title'],
                'rating': rand['rating'] if rand['rating'] else '-'
            })
    
    return jsonify(filme), 200

# Ruta pentru recomandarea unui film unui prieten
@friend_bp.route('/friends/recommend', methods=['POST'])
def recommend_movie():
    """
    Endpoint pentru recomandarea unui film unui prieten
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    # Preluam datele din cerere
    date = request.get_json()
    
    # Verificam daca datele au fost trimise
    if not date:
        return jsonify({'message': 'Date lipsa'}), 400
    
    nume_prieten = date.get('friend_username')
    titlu_film = date.get('movie_title')
    
    # Verificam daca toate datele au fost completate
    if not nume_prieten or not nume_prieten.strip():
        return jsonify({'message': 'Numele prietenului este obligatoriu'}), 400
    
    if not titlu_film or not titlu_film.strip():
        return jsonify({'message': 'Titlul filmului este obligatoriu'}), 400
    
    conn = get_db_connection()
    
    # Cautam utilizatorul prieten in baza de date
    prieten = conn.execute('SELECT id FROM users WHERE username = ?', (nume_prieten,)).fetchone()
    
    if not prieten:
        conn.close()
        return jsonify({'message': 'Utilizator negasit'}), 404
    
    id_prieten = prieten['id']
    
    # Verificam daca exista prietenia
    prietenie = conn.execute('SELECT id FROM friends WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)', 
                            (id_user, id_prieten, id_prieten, id_user)).fetchone()
    
    if not prietenie:
        conn.close()
        return jsonify({'message': 'Nu sunteti prieteni'}), 403
    
    try:
        # Adaugam recomandarea in baza de date
        conn.execute('INSERT INTO recommendations (from_user_id, to_user_id, movie_title) VALUES (?, ?, ?)', 
                    (id_user, id_prieten, titlu_film))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Recomandare trimisa'}), 201
    except Exception:
        conn.close()
        return jsonify({'message': 'Eroare la trimiterea recomandarii'}), 400

# Ruta pentru obtinerea recomandarilor primite
@friend_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """
    Endpoint pentru obtinerea recomandarilor primite de utilizatorul curent
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    conn = get_db_connection()
    
    # Preluam toate recomandarile primite de utilizator (inclusiv ID-ul pentru stergere)
    recomandari = conn.execute('''
        SELECT r.id, r.movie_title, u.username as from_username
        FROM recommendations r
        INNER JOIN users u ON r.from_user_id = u.id
        WHERE r.to_user_id = ?
        ORDER BY r.id DESC
    ''', (id_user,)).fetchall()
    
    conn.close()
    
    # Organizam recomandarile intr-o lista
    lista_recomandari = []
    for recomandare in recomandari:
        lista_recomandari.append({
            'id': recomandare['id'],
            'movie_title': recomandare['movie_title'],
            'from_username': recomandare['from_username']
        })
    
    return jsonify(lista_recomandari), 200

# Ruta pentru stergerea unei recomandari primite
@friend_bp.route('/recommendations/<int:recommendation_id>', methods=['DELETE'])
def delete_recommendation(recommendation_id):
    """
    Endpoint pentru stergerea unei recomandari primite
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    conn = get_db_connection()
    
    # Verificam daca recomandarea exista si apartine utilizatorului curent
    recomandare = conn.execute('SELECT id FROM recommendations WHERE id = ? AND to_user_id = ?', 
                               (recommendation_id, id_user)).fetchone()
    
    if not recomandare:
        conn.close()
        return jsonify({'message': 'Recomandare negasita'}), 404
    
    # Stergem recomandarea
    conn.execute('DELETE FROM recommendations WHERE id = ? AND to_user_id = ?', 
                (recommendation_id, id_user))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Recomandare stearsa'}), 200

