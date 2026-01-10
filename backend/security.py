"""
Modul pentru gestionarea securitatii: token-uri si verificare autentificare
"""
from models.database import get_db_connection

def verifica_token(text_header):
    """
    Verifica daca token-ul de autentificare este valid
    Args:
        text_header: Token-ul din header-ul Authorization
    Returns:
        id-ul utilizatorului daca token-ul este valid, None altfel
    """
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

