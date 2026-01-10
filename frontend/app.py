"""
Frontend - Flask app pentru interfață web (HTML templates)
Servește pagini HTML și gestionează interacțiunile utilizatorului
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sys

# Adăugăm backend-ul în path pentru import
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

# Importăm din backend pentru a apela API-ul
from models.database import get_db_connection
from security import verifica_token
from services.external_api import search_movies as search_movies_api

# Initializam aplicatia Flask pentru frontend
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'movie_manager_secret_key_change_in_production'  # Pentru sessions

# Importăm view handlers
from views import auth_views, dashboard_views, friend_views

# Inregistram blueprint-urile pentru views
app.register_blueprint(auth_views.auth_bp)
app.register_blueprint(dashboard_views.dashboard_bp)
app.register_blueprint(friend_views.friend_bp)

# Ruta root - redirect la login sau dashboard
@app.route('/')
def index():
    """Redirect la login sau dashboard în funcție de autentificare"""
    if 'user_id' in session:
        return redirect(url_for('dashboard.show_dashboard'))
    return redirect(url_for('auth.show_login'))

# Ruta pentru căutare filme (AJAX endpoint pentru autocomplete - opțional, pentru viitor)
# Pentru moment, căutarea se face direct prin form submission

# Pornim aplicatia
if __name__ == '__main__':
    # Pornim serverul Flask pe portul 5001 (backend rulează pe 5000)
    app.run(debug=True, port=5001)

