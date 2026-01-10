"""
Utilitare pentru validare input
Conține funcții de validare pentru username, password, etc.
"""

def validate_username(username):
    """
    Validează un username
    Returns: (valid: bool, message: str)
    """
    if not username or not username.strip():
        return False, 'Username is required'
    
    if len(username.strip()) < 3:
        return False, 'Username must be at least 3 characters'
    
    return True, ''

def validate_password(password):
    """
    Validează o parolă
    Returns: (valid: bool, message: str)
    """
    if not password or not password.strip():
        return False, 'Password is required'
    
    if len(password.strip()) < 3:
        return False, 'Password must be at least 3 characters'
    
    return True, ''

def validate_movie_title(title):
    """
    Validează un titlu de film
    Returns: (valid: bool, message: str)
    """
    if not title or not title.strip():
        return False, 'Movie title is required'
    
    return True, ''

def validate_rating(rating):
    """
    Validează un rating (1-10)
    Returns: (valid: bool, message: str)
    """
    try:
        rating_value = int(rating)
        if rating_value < 1 or rating_value > 10:
            return False, 'Rating must be between 1 and 10'
        return True, ''
    except (ValueError, TypeError):
        return False, 'Rating must be a number'

