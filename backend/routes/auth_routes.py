"""
Modul pentru rutele de autentificare (/login, /register)
"""
from flask import Blueprint
from services.auth_service import proceseaza_inregistrare, proceseaza_login

# Cream un Blueprint pentru rutele de autentificare (API)
auth_bp = Blueprint('auth', __name__)

# Ruta pentru crearea unui cont nou
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint pentru inregistrarea unui utilizator nou
    """
    # Apelam functia de procesare a inregistrarii din modulul auth_service
    return proceseaza_inregistrare()

# Ruta pentru autentificare
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint pentru autentificarea unui utilizator
    """
    # Apelam functia de procesare a login-ului din modulul auth_service
    return proceseaza_login()

