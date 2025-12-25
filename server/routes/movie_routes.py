"""
Modul pentru rutele legate de filme (/movies, /movies/<id>)
"""
from flask import Blueprint, request, jsonify
from models.database import get_db_connection
from security import verifica_token

# Cream un Blueprint pentru rutele de filme
movie_bp = Blueprint('movies', __name__)

# Ruta pentru obtinerea filmelor
@movie_bp.route('/movies', methods=['GET'])
def get_movies():
    """
    Endpoint pentru obtinerea tuturor filmelor utilizatorului curent
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    
    # Daca token ul nu este valid, returnam eroare
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    baza = get_db_connection()
    
    # Preluam filmele utilizatorului (inclusiv rating-ul)
    date_filme = baza.execute('SELECT id, title, status, rating FROM movies WHERE user_id = ?', (id_user,)).fetchall()
    baza.close()
    
    # Organizam filmele in liste pe status
    liste = {'To Watch': [], 'Watching': [], 'Completed': []}
    for rand in date_filme:
        # Verificam daca statusul este valid inainte de a adauga filmul
        status_film = rand['status']
        if status_film in liste:
            # Adaugam filmul cu rating-ul sau '-' daca nu exista
            rating = rand['rating'] if rand['rating'] else '-'
            liste[status_film].append({
                'id': rand['id'], 
                'title': rand['title'],
                'rating': rating
            })

    return jsonify(liste), 200

# Ruta pentru adaugarea unui film nou
@movie_bp.route('/movies', methods=['POST'])
def add_movie():
    """
    Endpoint pentru adaugarea unui film nou in lista utilizatorului
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
    
    titlu = date.get('title')
    
    # Verificam daca titlul a fost completat
    if not titlu or not titlu.strip():
        return jsonify({'message': 'Titlul este obligatoriu'}), 400
    
    # Preluam statusul dorit din cerere, sau folosim "To Watch" ca default
    status_ales = date.get('status')
    
    # Daca statusul nu este furnizat, setam "To Watch" ca default
    if not status_ales:
        status_ales = 'To Watch'
    
    # Verificam daca statusul este valid
    statusuri_valide = ['To Watch', 'Watching', 'Completed']
    if status_ales not in statusuri_valide:
        return jsonify({'message': 'Status invalid'}), 400
    
    baza = get_db_connection()
    
    # Introducem filmul in baza de date
    baza.execute('INSERT INTO movies (user_id, title, status, rating) VALUES (?, ?, ?, ?)', (id_user, titlu, status_ales, '-'))
    baza.commit()
    baza.close()
    
    return jsonify({'message': 'Film adaugat'}), 201

# Ruta pentru mutarea unui film intre liste
@movie_bp.route('/movies/<int:id_film>/move', methods=['PUT'])
def move_movie(id_film):
    """
    Endpoint pentru mutarea unui film intre liste (To Watch, Watching, Completed)
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    uid = verifica_token(token)
    if not uid:
        return jsonify({'message': 'Acces interzis'}), 401
    
    # Preluam noua lista din cerere
    date = request.get_json()
    
    # Verificam daca datele au fost trimise
    if not date:
        return jsonify({'message': 'Date lipsa'}), 400
    
    noua_lista = date.get('new_list')
    
    # Verificam daca noua lista este valida
    statusuri_valide = ['To Watch', 'Watching', 'Completed']
    if not noua_lista:
        return jsonify({'message': 'Status invalid'}), 400
    
    # Verificam daca este string gol sau nu este in lista de statusuri valide
    if not isinstance(noua_lista, str) or not noua_lista.strip() or noua_lista not in statusuri_valide:
        return jsonify({'message': 'Status invalid'}), 400
    
    conn = get_db_connection()
    
    # Verificam daca filmul exista si apartine utilizatorului
    film = conn.execute('SELECT id FROM movies WHERE id = ? AND user_id = ?', (id_film, uid)).fetchone()
    if not film:
        conn.close()
        return jsonify({'message': 'Film negasit'}), 404
    
    # Actualizam statusul filmului in baza de date
    conn.execute('UPDATE movies SET status = ? WHERE id = ? AND user_id = ?', (noua_lista, id_film, uid))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Film mutat'}), 200

# Ruta pentru notarea unui film
@movie_bp.route('/movies/<int:id_film>/rate', methods=['PUT'])
def rate_movie(id_film):
    """
    Endpoint pentru notarea unui film (1-10)
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    uid = verifica_token(token)
    if not uid:
        return jsonify({'message': 'Acces interzis'}), 401
    
    # Preluam nota din cerere
    date = request.get_json()
    
    # Verificam daca datele au fost trimise
    if not date:
        return jsonify({'message': 'Date lipsa'}), 400
    
    nota = date.get('rating')
    
    # Verificam daca nota a fost trimisa
    if nota is None:
        return jsonify({'message': 'Nota este obligatorie'}), 400
    
    conn = get_db_connection()
    
    # Verificam daca filmul exista si apartine utilizatorului
    film = conn.execute('SELECT id FROM movies WHERE id = ? AND user_id = ?', (id_film, uid)).fetchone()
    if not film:
        conn.close()
        return jsonify({'message': 'Film negasit'}), 404
    
    # Actualizam nota filmului in baza de date
    conn.execute('UPDATE movies SET rating = ? WHERE id = ? AND user_id = ?', (nota, id_film, uid))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Nota salvata'}), 200

# Ruta pentru stergerea unui film
@movie_bp.route('/movies/<int:id_film>', methods=['DELETE'])
def delete_movie(id_film):
    """
    Endpoint pentru stergerea unui film
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    uid = verifica_token(token)
    if not uid:
        return jsonify({'message': 'Acces interzis'}), 401
    
    conn = get_db_connection()
    
    # Verificam daca filmul exista si apartine utilizatorului
    film = conn.execute('SELECT id FROM movies WHERE id = ? AND user_id = ?', (id_film, uid)).fetchone()
    if not film:
        conn.close()
        return jsonify({'message': 'Film negasit'}), 404
    
    # Stergem filmul din baza de date
    conn.execute('DELETE FROM movies WHERE id = ? AND user_id = ?', (id_film, uid))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Film sters'}), 200

# Ruta pentru obtinerea username-ului utilizatorului curent
@movie_bp.route('/user/username', methods=['GET'])
def get_username():
    """
    Endpoint pentru obtinerea username-ului utilizatorului curent
    """
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    # Extragem username-ul din token
    nume_user = token.replace('token_secret_pentru_', '')
    
    return jsonify({'username': nume_user}), 200

