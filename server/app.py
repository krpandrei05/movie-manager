from flask import Flask, request, jsonify, render_template
import sqlite3
from auth import proceseaza_inregistrare, proceseaza_login

# Initializam aplicatia Flask cu directoarele pentru template-uri si fisiere statice
app = Flask(__name__, template_folder='templates', static_folder='static')

# Decorator pentru adaugarea header-elor CORS la toate raspunsurile
# Acest decorator permite comunicarea intre frontend si backend
@app.after_request
def after_request(response):
    # Permitem request-uri de la orice origine (pentru development)
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    # Specificam metodele HTTP permise
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    
    # Specificam header-ele permise in request-uri
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    return response

# Handler pentru request-urile OPTIONS (preflight CORS)
# Browserul trimite acest request inainte de request-urile POST/PUT/DELETE
@app.before_request
def handle_preflight():
    # Verificam daca este un request OPTIONS (preflight)
    if request.method == "OPTIONS":
        # Returnam raspuns gol cu header-ele CORS necesare
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

# Functie pentru deschiderea conexiunii la baza de date
def get_db_connection():
    # Cream fisierul bazei de date local
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crearea tabelelor la pornirea serverului
def init_db():
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

def verifica_token(text_header):
    # Deocamdata, verificam doar daca token ul este valid
    if not text_header:
        return None
    
    # Luam numele utilizatorului din token
    nume_user = text_header.replace('token_secret_pentru_', '')
    baza = get_db_connection()
    
    # Cautam utilizatorul in baza de date
    utilizator = baza.execute('SELECT id FROM users WHERE username = ?', (nume_user,)).fetchone()
    baza.close()
    
    # Daca utilizatorul exista, returnam id ul acestuia
    if utilizator:
        return utilizator['id']
    
    # Altfel, returnam None
    return None

# Ruta root pentru afisarea paginii principale web
@app.route('/', methods=['GET'])
def index():
    # Returnam pagina HTML principala
    return render_template('index.html')

# Ruta pentru crearea unui cont nou
@app.route('/register', methods=['POST'])
def register():
    # Apelam functia de procesare a inregistrarii din modulul auth
    return proceseaza_inregistrare()

# Ruta pentru autentificare
@app.route('/login', methods=['POST'])
def login():
    # Apelam functia de procesare a login-ului din modulul auth
    return proceseaza_login()

# Ruta pentru obtinerea filmelor
@app.route('/movies', methods=['GET'])
def get_movies():
    # Verificam token ul de autentificare
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    
    # Daca token ul nu este valid, returnam eroare
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    baza = get_db_connection()
    
    # Preluam filmele utilizatorului
    date_filme = baza.execute('SELECT id, title, status FROM movies WHERE user_id = ?', (id_user,)).fetchall()
    baza.close()
    
    # Organizam filmele in liste pe status
    liste = {'To Watch': [], 'Watching': [], 'Completed': []}
    for rand in date_filme:
        # Verificam daca statusul este valid inainte de a adauga filmul
        status_film = rand['status']
        if status_film in liste:
            liste[status_film].append({'id': rand['id'], 'title': rand['title']})

    return jsonify(liste), 200

# Ruta pentru adaugarea unui film nou
@app.route('/movies', methods=['POST'])
def add_movie():
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
@app.route('/movies/<int:id_film>/move', methods=['PUT'])
def move_movie(id_film):
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
@app.route('/movies/<int:id_film>/rate', methods=['PUT'])
def rate_movie(id_film):
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
@app.route('/movies/<int:id_film>', methods=['DELETE'])
def delete_movie(id_film):
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

# Ruta pentru adaugarea unui prieten
@app.route('/friends/add', methods=['POST'])
def add_friend():
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
@app.route('/friends/<friend_username>/movies', methods=['GET'])
def get_friend_movies(friend_username):
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
    
    # Preluam doar filmele finalizate ale prietenului
    date_filme = conn.execute('SELECT id, title, rating FROM movies WHERE user_id = ? AND status = ?', 
                              (id_prieten, 'Completed')).fetchall()
    conn.close()
    
    # Organizam filmele intr o lista
    filme = []
    for rand in date_filme:
        filme.append({
            'id': rand['id'],
            'title': rand['title'],
            'rating': rand['rating']
        })
    
    return jsonify(filme), 200

# Ruta pentru recomandarea unui film unui prieten
@app.route('/friends/recommend', methods=['POST'])
def recommend_movie():
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)