from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sys
import os

# Importam din backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

from models.database import get_db_connection

# Importam validators din frontend
FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FRONTEND_DIR)
from utils.validators import validate_movie_title, validate_rating

dashboard_bp = Blueprint('dashboard', __name__)

# Verifica daca utilizatorul este autentificat
def require_auth():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.show_login'))
    return None

@dashboard_bp.route('/dashboard')
# Afiseaza dashboard-ul cu filmele utilizatorului
def show_dashboard():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    username = session.get('username', 'User')
    
    # Obtinem filmele din baza de date
    conn = get_db_connection()
    movies_data = conn.execute(
        'SELECT id, title, status, rating FROM movies WHERE user_id = ?',
        (user_id,)
    ).fetchall()
    conn.close()
    
    # Organizam filmele pe liste
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
    
    # Obtinem lista de prieteni pentru sidebar
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
# Adauga un film nou
def add_movie():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    title = request.form.get('title', '').strip()
    status = request.form.get('status', 'To Watch')
    movie_validated = request.form.get('movie_validated', '0')
    
    # Validare stricta: verificam daca filmul a fost selectat din dropdown
    if movie_validated != '1':
        flash('Please select a movie from the dropdown list.', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Validare titlu
    valid, message = validate_movie_title(title)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Verificam statusul
    if status not in ['To Watch', 'Watching', 'Completed']:
        status = 'To Watch'
    
    # Verificam daca filmul exista deja pentru acest utilizator
    conn = get_db_connection()
    existing_movie = conn.execute(
        'SELECT id FROM movies WHERE user_id = ? AND title = ?',
        (user_id, title)
    ).fetchone()
    
    if existing_movie:
        conn.close()
        flash('This movie already exists in your list!', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Adaugam filmul in baza de date
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
# Muta un film intre liste
def move_movie(movie_id):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    new_status = request.form.get('new_list', '').strip()
    
    if new_status not in ['To Watch', 'Watching', 'Completed']:
        flash('Invalid status', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    conn = get_db_connection()
    # Verificam ca filmul apartine utilizatorului
    movie = conn.execute(
        'SELECT id FROM movies WHERE id = ? AND user_id = ?',
        (movie_id, user_id)
    ).fetchone()
    
    if not movie:
        conn.close()
        flash('Movie not found', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Actualizam statusul
    conn.execute(
        'UPDATE movies SET status = ? WHERE id = ? AND user_id = ?',
        (new_status, movie_id, user_id)
    )
    conn.commit()
    conn.close()
    
    flash(f'Movie moved to {new_status} successfully!', 'success')
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/<int:movie_id>/rate', methods=['POST'])
# Noteaza un film
def rate_movie(movie_id):
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
    # Verificam ca filmul apartine utilizatorului
    movie = conn.execute(
        'SELECT id FROM movies WHERE id = ? AND user_id = ?',
        (movie_id, user_id)
    ).fetchone()
    
    if not movie:
        conn.close()
        flash('Movie not found', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Actualizam rating-ul
    conn.execute(
        'UPDATE movies SET rating = ? WHERE id = ? AND user_id = ?',
        (rating, movie_id, user_id)
    )
    conn.commit()
    conn.close()
    
    flash(f'Movie rated {rating}/10!', 'success')
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/<int:movie_id>/delete', methods=['POST'])
# Sterge un film
def delete_movie(movie_id):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    # Verificam ca filmul apartine utilizatorului
    movie = conn.execute(
        'SELECT id FROM movies WHERE id = ? AND user_id = ?',
        (movie_id, user_id)
    ).fetchone()
    
    if not movie:
        conn.close()
        flash('Movie not found', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Stergem filmul
    conn.execute(
        'DELETE FROM movies WHERE id = ? AND user_id = ?',
        (movie_id, user_id)
    )
    conn.commit()
    conn.close()
    
    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('dashboard.show_dashboard'))
