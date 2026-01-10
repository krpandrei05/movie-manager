"""
View handlers pentru dashboard (My Movies)
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sys
import os

# Importăm din backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

from models.database import get_db_connection
from security import verifica_token

# Importăm validators din frontend
FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FRONTEND_DIR)
from utils.validators import validate_movie_title, validate_rating

dashboard_bp = Blueprint('dashboard', __name__)

def require_auth():
    """Verifică dacă utilizatorul este autentificat"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.show_login'))
    return None

@dashboard_bp.route('/dashboard')
def show_dashboard():
    """Afișează dashboard-ul cu filmele utilizatorului"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    username = session.get('username', 'User')
    
    # Obținem filmele din baza de date
    conn = get_db_connection()
    movies_data = conn.execute(
        'SELECT id, title, status, rating FROM movies WHERE user_id = ?',
        (user_id,)
    ).fetchall()
    conn.close()
    
    # Organizăm filmele pe liste
    movies = {'To Watch': [], 'Watching': [], 'Completed': []}
    for row in movies_data:
        status = row['status']
        if status in movies:
            rating = row['rating'] if row['rating'] and row['rating'] != '-' else None
            movies[status].append({
                'id': row['id'],
                'title': row['title'],
                'rating': rating
            })
    
    # Obținem lista de prieteni pentru sidebar
    conn = get_db_connection()
    friends_data = conn.execute('''
        SELECT DISTINCT u.username 
        FROM users u
        INNER JOIN friends f ON (f.friend_id = u.id AND f.user_id = ?) OR (f.user_id = u.id AND f.friend_id = ?)
        WHERE u.id != ?
    ''', (user_id, user_id, user_id)).fetchall()
    conn.close()
    
    friends = [friend['username'] for friend in friends_data]
    
    return render_template('dashboard.html', 
                         movies=movies, 
                         username=username,
                         friends=friends)

@dashboard_bp.route('/movies/add', methods=['POST'])
def add_movie():
    """Adaugă un film nou"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    title = request.form.get('title', '').strip()
    status = request.form.get('status', 'To Watch')
    
    # Validare
    valid, message = validate_movie_title(title)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Verificăm statusul
    if status not in ['To Watch', 'Watching', 'Completed']:
        status = 'To Watch'
    
    # Adăugăm filmul în baza de date
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO movies (user_id, title, status, rating) VALUES (?, ?, ?, ?)',
            (user_id, title, status, '-')
        )
        conn.commit()
        conn.close()
        flash('Movie added successfully!', 'success')
    except Exception as e:
        conn.close()
        flash('Error adding movie', 'error')
    
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/<int:movie_id>/move', methods=['POST'])
def move_movie(movie_id):
    """Mută un film între liste"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    new_status = request.form.get('new_list', '').strip()
    
    if new_status not in ['To Watch', 'Watching', 'Completed']:
        flash('Invalid status', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    conn = get_db_connection()
    # Verificăm că filmul aparține utilizatorului
    movie = conn.execute(
        'SELECT id FROM movies WHERE id = ? AND user_id = ?',
        (movie_id, user_id)
    ).fetchone()
    
    if not movie:
        conn.close()
        flash('Movie not found', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Actualizăm statusul
    conn.execute(
        'UPDATE movies SET status = ? WHERE id = ? AND user_id = ?',
        (new_status, movie_id, user_id)
    )
    conn.commit()
    conn.close()
    
    flash(f'Movie moved to {new_status} successfully!', 'success')
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/<int:movie_id>/rate', methods=['POST'])
def rate_movie(movie_id):
    """Notează un film"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    rating = request.form.get('rating', '').strip()
    
    # Validare
    valid, message = validate_rating(rating)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    conn = get_db_connection()
    # Verificăm că filmul aparține utilizatorului
    movie = conn.execute(
        'SELECT id FROM movies WHERE id = ? AND user_id = ?',
        (movie_id, user_id)
    ).fetchone()
    
    if not movie:
        conn.close()
        flash('Movie not found', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Actualizăm rating-ul
    conn.execute(
        'UPDATE movies SET rating = ? WHERE id = ? AND user_id = ?',
        (rating, movie_id, user_id)
    )
    conn.commit()
    conn.close()
    
    flash(f'Movie rated {rating}/10!', 'success')
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    """Șterge un film"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    # Verificăm că filmul aparține utilizatorului
    movie = conn.execute(
        'SELECT id FROM movies WHERE id = ? AND user_id = ?',
        (movie_id, user_id)
    ).fetchone()
    
    if not movie:
        conn.close()
        flash('Movie not found', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Ștergem filmul
    conn.execute(
        'DELETE FROM movies WHERE id = ? AND user_id = ?',
        (movie_id, user_id)
    )
    conn.commit()
    conn.close()
    
    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('dashboard.show_dashboard'))
