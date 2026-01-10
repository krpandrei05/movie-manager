"""
Modul pentru interogarea API-urilor externe (TVMaze pentru cautare filme)
"""
import urllib.request
import urllib.parse
import json
from flask import request, jsonify

# Functie pentru cautarea filmelor, serialelor si show-urilor TV pe TVMaze API
def search_movies():
    """
    Cauta filme, seriale si show-uri TV folosind TVMaze API (gratuit, fara cheie)
    Returns:
        JSON response cu rezultatele cautarii sau mesaj de eroare
    """
    # Preluam termenul de cautare din query string
    search_term = request.args.get('s', '')
    
    # Verificam daca termenul de cautare a fost trimis
    if not search_term or not search_term.strip():
        return jsonify({'Response': 'False', 'Error': 'Search term required'}), 400
    
    try:
        # Facem request catre TVMaze API (gratuit, fara cheie necesara)
        # TVMaze API returneaza filme, seriale, show-uri TV, etc.
        search_params = urllib.parse.urlencode({
            'q': search_term.strip()
        })
        tvmaze_url = f'http://api.tvmaze.com/search/shows?{search_params}'
        
        # Facem request-ul HTTP
        with urllib.request.urlopen(tvmaze_url, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        # Transformam rezultatul TVMaze in format compatibil cu codul existent
        # TVMaze returneaza o lista de obiecte cu 'show' in interior
        formatted_results = {
            'Response': 'True',
            'Search': []
        }
        
        # Extragem informatiile relevante din fiecare rezultat
        for item in data:
            show = item.get('show', {})
            formatted_results['Search'].append({
                'Title': show.get('name', 'Unknown'),
                'Year': show.get('premiered', '')[:4] if show.get('premiered') else 'N/A',
                'Type': show.get('type', 'show'),
                'imdbID': str(show.get('id', '')),
                'Poster': show.get('image', {}).get('medium', '') if show.get('image') else ''
            })
        
        # Returnam rezultatul formatat
        return jsonify(formatted_results), 200
    except Exception as e:
        # In caz de eroare, returnam mesaj de eroare
        return jsonify({'Response': 'False', 'Error': 'Error searching movies'}), 500

