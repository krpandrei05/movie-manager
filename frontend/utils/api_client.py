"""
Client Python pentru comunicarea cu backend API
Folosește requests pentru a apela endpoint-urile backend
"""
import requests
import os

# URL-ul backend API
API_URL = os.getenv('BACKEND_API_URL', 'http://localhost:5000/api')

class APIClient:
    """Client pentru apelarea backend API"""
    
    def __init__(self, token=None):
        self.token = token
        self.base_url = API_URL
    
    def _get_headers(self):
        """Returnează header-ele pentru request-uri"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = self.token
        return headers
    
    # Auth methods
    def login(self, username, password):
        """Login utilizator"""
        response = requests.post(
            f'{self.base_url}/login',
            json={'username': username, 'password': password},
            headers=self._get_headers()
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('token')
            return True, data
        return False, response.json() if response.content else {'message': 'Login failed'}
    
    def register(self, username, password):
        """Înregistrare utilizator nou"""
        response = requests.post(
            f'{self.base_url}/register',
            json={'username': username, 'password': password},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 201, data
    
    def get_username(self):
        """Obține username-ul utilizatorului curent"""
        response = requests.get(
            f'{self.base_url}/user/username',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        return False, {}
    
    # Movie methods
    def get_movies(self):
        """Obține toate filmele utilizatorului"""
        response = requests.get(
            f'{self.base_url}/movies',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        return False, {}
    
    def add_movie(self, title, status='To Watch'):
        """Adaugă un film nou"""
        response = requests.post(
            f'{self.base_url}/movies',
            json={'title': title, 'status': status},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 201, data
    
    def move_movie(self, movie_id, new_list):
        """Mută un film între liste"""
        response = requests.put(
            f'{self.base_url}/movies/{movie_id}/move',
            json={'new_list': new_list},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 200, data
    
    def rate_movie(self, movie_id, rating):
        """Notează un film"""
        response = requests.put(
            f'{self.base_url}/movies/{movie_id}/rate',
            json={'rating': str(rating)},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 200, data
    
    def delete_movie(self, movie_id):
        """Șterge un film"""
        response = requests.delete(
            f'{self.base_url}/movies/{movie_id}',
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 200, data
    
    # Friend methods
    def get_friends(self):
        """Obține lista de prieteni"""
        response = requests.get(
            f'{self.base_url}/friends',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        return False, []
    
    def add_friend(self, friend_username):
        """Adaugă un prieten"""
        response = requests.post(
            f'{self.base_url}/friends/add',
            json={'friend_username': friend_username},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 201, data
    
    def get_friend_movies(self, friend_username):
        """Obține filmele unui prieten"""
        response = requests.get(
            f'{self.base_url}/friends/{friend_username}/movies',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        data = response.json() if response.content else {}
        return False, data
    
    # Recommendation methods
    def get_recommendations(self):
        """Obține recomandările primite"""
        response = requests.get(
            f'{self.base_url}/recommendations',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        return False, []
    
    def recommend_movie(self, friend_username, movie_title):
        """Trimite o recomandare"""
        response = requests.post(
            f'{self.base_url}/friends/recommend',
            json={'friend_username': friend_username, 'movie_title': movie_title},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 201, data
    
    def delete_recommendation(self, recommendation_id):
        """Șterge o recomandare"""
        response = requests.delete(
            f'{self.base_url}/recommendations/{recommendation_id}',
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 200, data

