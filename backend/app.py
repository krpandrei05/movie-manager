"""
Backend API - Flask app pentru API REST (JSON responses)
Nu servește HTML, doar JSON pentru frontend
"""
from flask import Flask, jsonify, request
from models.database import init_db
from routes.auth_routes import auth_bp
from routes.movie_routes import movie_bp
from routes.friend_routes import friend_bp
from services.external_api import search_movies

# Initializam aplicatia Flask pentru API
app = Flask(__name__)

# CORS headers manual (pentru a nu necesita flask-cors)
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

# Inregistram blueprint-urile pentru API routes
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(movie_bp, url_prefix='/api')
app.register_blueprint(friend_bp, url_prefix='/api')

# Ruta pentru cautarea filmelor (API extern)
@app.route('/api/search-movies', methods=['GET'])
def search_movies_route():
    """
    Endpoint pentru cautarea filmelor folosind API-ul extern (TVMaze)
    """
    return search_movies()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint pentru verificarea stării API-ului"""
    return jsonify({'status': 'ok'}), 200

# Pornim aplicatia
if __name__ == '__main__':
    # Initializam baza de date la pornirea serverului
    init_db()
    # Pornim serverul Flask pe portul 5000
    app.run(debug=True, port=5000)
