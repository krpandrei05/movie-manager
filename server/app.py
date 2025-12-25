"""
Punctul de intrare al aplicatiei Flask
Initializeaza aplicatia si inregistreaza toate blueprint-urile
"""
from flask import Flask, render_template, jsonify, request
from models.database import init_db
from routes.auth_routes import auth_bp
from routes.movie_routes import movie_bp
from routes.friend_routes import friend_bp
from services.external_api import search_movies

# Initializam aplicatia Flask cu directoarele pentru template-uri si fisiere statice
app = Flask(__name__, template_folder='templates', static_folder='static')

# Decorator pentru adaugarea header-elor CORS la toate raspunsurile
# Acest decorator permite comunicarea intre frontend si backend
@app.after_request
def after_request(response):
    """
    Adauga header-ele CORS la toate raspunsurile pentru a permite comunicarea frontend-backend
    """
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
    """
    Gestioneaza request-urile OPTIONS (preflight CORS)
    """
    # Verificam daca este un request OPTIONS (preflight)
    if request.method == "OPTIONS":
        # Returnam raspuns gol cu header-ele CORS necesare
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

# Ruta root pentru afisarea paginii principale web
@app.route('/', methods=['GET'])
def index():
    """
    Endpoint pentru afisarea paginii principale HTML
    """
    # Returnam pagina HTML principala
    return render_template('index.html')

# Ruta pentru cautarea filmelor (API extern)
@app.route('/api/search-movies', methods=['GET'])
def search_movies_route():
    """
    Endpoint pentru cautarea filmelor folosind API-ul extern (TVMaze)
    """
    return search_movies()

# Inregistram blueprint-urile pentru rutele aplicatiei
app.register_blueprint(auth_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(friend_bp)

# Pornim aplicatia
if __name__ == '__main__':
    # Initializam baza de date la pornirea serverului
    init_db()
    # Pornim serverul Flask in modul debug pe portul 5000
    app.run(debug=True, port=5000)
