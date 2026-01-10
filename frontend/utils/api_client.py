import requests
import os

# URL-ul backend API
API_URL = os.getenv('BACKEND_API_URL', 'http://localhost:5000/api')

# Client pentru apelarea backend API
class APIClient:
    
    def __init__(self, token=None):
        self.token = token
        self.base_url = API_URL
    
    # Returneaza header-ele pentru request-uri
    def _get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = self.token
        return headers
    
    # Auth methods
    # Login utilizator
    def login(self, username, password):
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
    
    # Inregistrare utilizator nou
    def register(self, username, password):
        response = requests.post(
            f'{self.base_url}/register',
            json={'username': username, 'password': password},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 201, data
    
    # Obtine username-ul utilizatorului curent
    def get_username(self):
        response = requests.get(
            f'{self.base_url}/user/username',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        return False, {}
    
    # Movie methods
    # Obtine toate filmele utilizatorului
    def get_movies(self):
        response = requests.get(
            f'{self.base_url}/movies',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        return False, {}
    
    # Adauga un film nou
    def add_movie(self, title, status='To Watch'):
        response = requests.post(
            f'{self.base_url}/movies',
            json={'title': title, 'status': status},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 201, data
    
    # Muta un film intre liste
    def move_movie(self, movie_id, new_list):
        response = requests.put(
            f'{self.base_url}/movies/{movie_id}/move',
            json={'new_list': new_list},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 200, data
    
    # Noteaza un film
    def rate_movie(self, movie_id, rating):
        response = requests.put(
            f'{self.base_url}/movies/{movie_id}/rate',
            json={'rating': str(rating)},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 200, data
    
    # Sterge un film
    def delete_movie(self, movie_id):
        response = requests.delete(
            f'{self.base_url}/movies/{movie_id}',
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 200, data
    
    # Friend methods
    # Obtine lista de prieteni
    def get_friends(self):
        response = requests.get(
            f'{self.base_url}/friends',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        return False, []
    
    # Adauga un prieten
    def add_friend(self, friend_username):
        response = requests.post(
            f'{self.base_url}/friends/add',
            json={'friend_username': friend_username},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 201, data
    
    # Obtine filmele unui prieten
    def get_friend_movies(self, friend_username):
        response = requests.get(
            f'{self.base_url}/friends/{friend_username}/movies',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        data = response.json() if response.content else {}
        return False, data
    
    # Recommendation methods
    # Obtine recomandarile primite
    def get_recommendations(self):
        response = requests.get(
            f'{self.base_url}/recommendations',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        return False, []
    
    # Trimite o recomandare
    def recommend_movie(self, friend_username, movie_title):
        response = requests.post(
            f'{self.base_url}/friends/recommend',
            json={'friend_username': friend_username, 'movie_title': movie_title},
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 201, data
    
    # Sterge o recomandare
    def delete_recommendation(self, recommendation_id):
        response = requests.delete(
            f'{self.base_url}/recommendations/{recommendation_id}',
            headers=self._get_headers()
        )
        data = response.json() if response.content else {}
        return response.status_code == 200, data

