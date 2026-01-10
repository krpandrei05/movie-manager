# Valideaza un username
def validate_username(username):
    if not username or not username.strip():
        return False, 'Username is required'
    
    if len(username.strip()) < 3:
        return False, 'Username must be at least 3 characters'
    
    return True, ''

# Valideaza o parola
def validate_password(password):
    if not password or not password.strip():
        return False, 'Password is required'
    
    if len(password.strip()) < 3:
        return False, 'Password must be at least 3 characters'
    
    return True, ''

# Valideaza un titlu de film
def validate_movie_title(title):
    if not title or not title.strip():
        return False, 'Movie title is required'
    
    return True, ''

# Valideaza un rating (1-10)
def validate_rating(rating):
    try:
        rating_value = int(rating)
        if rating_value < 1 or rating_value > 10:
            return False, 'Rating must be between 1 and 10'
        return True, ''
    except (ValueError, TypeError):
        return False, 'Rating must be a number'
