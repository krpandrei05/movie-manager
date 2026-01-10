"""
View handlers pentru friends și recommendations
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sys
import os

# Importăm din backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

from models.database import get_db_connection

# Importăm validators din frontend
FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FRONTEND_DIR)
from utils.validators import validate_username, validate_movie_title

friend_bp = Blueprint('friend', __name__)

def require_auth():
    """Verifică dacă utilizatorul este autentificat"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.show_login'))
    return None

@friend_bp.route('/friends')
def show_friends():
    """Afișează pagina de prieteni"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    
    # Obținem lista de prieteni
    conn = get_db_connection()
    friends_data = conn.execute('''
        SELECT DISTINCT u.username 
        FROM users u
        INNER JOIN friends f ON (f.friend_id = u.id AND f.user_id = ?) OR (f.user_id = u.id AND f.friend_id = ?)
        WHERE u.id != ?
    ''', (user_id, user_id, user_id)).fetchall()
    conn.close()
    
    friends = [friend['username'] for friend in friends_data]
    
    return render_template('friends.html', friends=friends)

@friend_bp.route('/friends/add', methods=['POST'])
def add_friend():
    """Adaugă un prieten"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    friend_username = request.form.get('friend_username', '').strip()
    
    # Validare
    valid, message = validate_username(friend_username)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('friend.show_friends'))
    
    conn = get_db_connection()
    
    # Căutăm utilizatorul prieten
    friend_user = conn.execute('SELECT id FROM users WHERE username = ?', (friend_username,)).fetchone()
    
    if not friend_user:
        conn.close()
        flash('User not found', 'error')
        return redirect(url_for('friend.show_friends'))
    
    friend_id = friend_user['id']
    
    # Verificăm dacă nu încearcă să se adauge pe sine
    if user_id == friend_id:
        conn.close()
        flash('You cannot add yourself', 'error')
        return redirect(url_for('friend.show_friends'))
    
    # Verificăm dacă prietenia există deja
    existing = conn.execute('''
        SELECT id FROM friends 
        WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
    ''', (user_id, friend_id, friend_id, user_id)).fetchone()
    
    if existing:
        conn.close()
        flash('Friendship already exists', 'error')
        return redirect(url_for('friend.show_friends'))
    
    # Adăugăm prietenia (bidirecțională)
    try:
        conn.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (user_id, friend_id))
        conn.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (friend_id, user_id))
        conn.commit()
        conn.close()
        flash('Friend added successfully!', 'success')
    except Exception as e:
        conn.close()
        flash('Error adding friend', 'error')
    
    return redirect(url_for('friend.show_friends'))

@friend_bp.route('/friends/<username>')
def show_friend_profile(username):
    """Afișează profilul unui prieten"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    
    # Verificăm dacă prietenia există
    conn = get_db_connection()
    friend_user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    
    if not friend_user:
        conn.close()
        flash('User not found', 'error')
        return redirect(url_for('friend.show_friends'))
    
    friend_id = friend_user['id']
    
    # Verificăm prietenia
    friendship = conn.execute('''
        SELECT id FROM friends 
        WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
    ''', (user_id, friend_id, friend_id, user_id)).fetchone()
    
    if not friendship:
        conn.close()
        flash('You are not friends with this user', 'error')
        return redirect(url_for('friend.show_friends'))
    
    # Obținem filmele prietenului
    movies_data = conn.execute(
        'SELECT id, title, status, rating FROM movies WHERE user_id = ? ORDER BY status, title',
        (friend_id,)
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
    
    return render_template('friend_profile.html', friend_username=username, movies=movies)

@friend_bp.route('/friends/<username>/recommend', methods=['POST'])
def recommend_movie(username):
    """Recomandă un film unui prieten"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    movie_title = request.form.get('movie_title', '').strip()
    movie_validated = request.form.get('movie_validated', '0')
    
    # Validare strictă: verificăm dacă filmul a fost selectat din dropdown
    if movie_validated != '1':
        flash('Please select a movie from the dropdown list.', 'error')
        return redirect(url_for('friend.show_friend_profile', username=username))
    
    # Validare titlu
    valid, message = validate_movie_title(movie_title)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('friend.show_friend_profile', username=username))
    
    conn = get_db_connection()
    
    # Verificăm prietenia
    friend_user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    if not friend_user:
        conn.close()
        flash('User not found', 'error')
        return redirect(url_for('friend.show_friends'))
    
    friend_id = friend_user['id']
    
    friendship = conn.execute('''
        SELECT id FROM friends 
        WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
    ''', (user_id, friend_id, friend_id, user_id)).fetchone()
    
    if not friendship:
        conn.close()
        flash('You are not friends with this user', 'error')
        return redirect(url_for('friend.show_friends'))
    
    # Adăugăm recomandarea
    try:
        conn.execute(
            'INSERT INTO recommendations (from_user_id, to_user_id, movie_title) VALUES (?, ?, ?)',
            (user_id, friend_id, movie_title)
        )
        conn.commit()
        conn.close()
        flash('Recommendation sent successfully!', 'success')
    except Exception as e:
        conn.close()
        flash('Error sending recommendation', 'error')
    
    return redirect(url_for('friend.show_friend_profile', username=username))

@friend_bp.route('/recommendations')
def show_recommendations():
    """Afișează recomandările primite"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    
    # Obținem recomandările
    conn = get_db_connection()
    recommendations_data = conn.execute('''
        SELECT r.id, r.movie_title, u.username as from_username
        FROM recommendations r
        INNER JOIN users u ON r.from_user_id = u.id
        WHERE r.to_user_id = ?
        ORDER BY r.id DESC
    ''', (user_id,)).fetchall()
    conn.close()
    
    recommendations = [
        {
            'id': rec['id'],
            'movie_title': rec['movie_title'],
            'from_username': rec['from_username']
        }
        for rec in recommendations_data
    ]
    
    return render_template('recommendations.html', recommendations=recommendations)

@friend_bp.route('/recommendations/<int:recommendation_id>/delete', methods=['POST'])
def delete_recommendation(recommendation_id):
    """Șterge o recomandare"""
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    
    # Verificăm că recomandarea aparține utilizatorului
    rec = conn.execute(
        'SELECT id FROM recommendations WHERE id = ? AND to_user_id = ?',
        (recommendation_id, user_id)
    ).fetchone()
    
    if not rec:
        conn.close()
        flash('Recommendation not found', 'error')
        return redirect(url_for('friend.show_recommendations'))
    
    # Ștergem recomandarea
    conn.execute(
        'DELETE FROM recommendations WHERE id = ? AND to_user_id = ?',
        (recommendation_id, user_id)
    )
    conn.commit()
    conn.close()
    
    flash('Recommendation deleted successfully!', 'success')
    return redirect(url_for('friend.show_recommendations'))
