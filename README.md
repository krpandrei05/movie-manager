# Movie Manager

Aplicație web pentru gestionarea filmelor, serialelor și show-urilor TV. Utilizatorii pot crea liste de filme, adăuga prieteni, recomanda filme și vedea ce filme au prietenii lor.

## 📋 Cuprins

- [Funcționalități](#funcționalități)
- [Tehnologii](#tehnologii)
- [Structura Proiectului](#structura-proiectului)
- [Instalare](#instalare)
- [Rulare](#rulare)
- [Arhitectură](#arhitectură)
- [API Endpoints](#api-endpoints)
- [Frontend Views](#frontend-views)
- [Baza de Date](#baza-de-date)
- [Securitate](#securitate)
- [API Extern](#api-extern)

---

## 🎯 Funcționalități

### Autentificare
- **Înregistrare**: Utilizatorii pot crea un cont nou cu username și parolă
- **Login**: Utilizatorii se pot autentifica cu username și parolă
  - **Enter key**: Apăsarea tastei Enter în câmpul de parolă trimite automat formularul
- **Securitate**: Parolele sunt criptate în baza de date folosind hash-uri (Werkzeug)
- **Sessions**: Gestionare sesiuni pentru autentificare persistentă

### Gestionare Filme
- **Adăugare filme**: Utilizatorii pot adăuga filme în trei liste:
  - **To Watch**: Filme pe care vrea să le vadă
  - **Watching**: Filme pe care le urmărește în prezent
  - **Completed**: Filme pe care le-a terminat de văzut
- **Mutare între liste**: Utilizatorii pot muta filme între cele trei liste
- **Notare filme**: Pentru filmele din lista "Completed", utilizatorii pot da o notă de la 1 la 10
- **Ștergere filme**: Utilizatorii pot șterge filme din liste
- **Căutare filme**: Integrare cu TVMaze API pentru căutarea filmelor, serialelor și show-urilor TV (gratuit, fără cheie API)
- **Autocomplete**: Căutare în timp real cu dropdown de rezultate
- **Validare strictă**: Filmele pot fi adăugate doar dacă sunt selectate din dropdown-ul de rezultate (validare Python)

### Prieteni
- **Adăugare prieteni**: Utilizatorii pot adăuga alți utilizatori ca prieteni
  - **Layout vertical**: Search bar-ul și butonul "Add Friend" sunt așezate unul sub altul, centrate
- **Vizualizare listă prieteni**: Utilizatorii pot vedea lista cu toți prietenii lor
- **Vizualizare filme prieteni**: Utilizatorii pot vedea toate listele de filme ale prietenilor (To Watch, Watching, Completed)
- **Recomandare filme**: Utilizatorii pot recomanda filme prietenilor lor
  - **Autocomplete**: Aceeași funcționalitate de căutare ca în "My Movies"
  - **Validare strictă**: Filmele pot fi recomandate doar dacă sunt selectate din dropdown
  - **Layout vertical**: "Recommend a Movie" → Search Box → Button (așezate vertical)

### Recomandări
- **Vizualizare recomandări**: Utilizatorii pot vedea toate recomandările primite de la prieteni
- **Ștergere recomandări**: Utilizatorii pot șterge recomandările primite
  - **Dialog de confirmare**: Dialog custom cu mesaje specifice pentru fiecare acțiune

---

## 🛠 Tehnologii

### Backend
- **Flask 3.0.0**: Framework web Python pentru API REST
- **SQLite**: Baza de date pentru stocare persistentă
- **Werkzeug 3.0.1**: Utilitare pentru securitate (criptare parole)

### Frontend
- **Flask (Server-Side Rendering)**: Generare HTML dinamic cu Jinja2 templates
- **HTML5/CSS3**: Structură și stilizare (tema dark)
- **JavaScript (minim)**: Autocomplete pentru căutare filme (interacțiuni în timp real)
- **Jinja2**: Template engine pentru generare HTML dinamic

### API Extern
- **TVMaze API**: API gratuit pentru căutare filme, seriale și show-uri TV (fără cheie API necesară)

---

## 📁 Structura Proiectului

```
movie-manager/
├── backend/                    # Backend API (REST JSON)
│   ├── app.py                  # Punctul de intrare al API-ului
│   ├── models/                 # Modele de date
│   │   └── database.py         # Gestionare baza de date SQLite
│   ├── routes/                 # Rute API
│   │   ├── auth_routes.py      # Rute autentificare (/api/register, /api/login)
│   │   ├── movie_routes.py     # Rute filme (/api/movies, /api/movies/<id>/move, etc.)
│   │   └── friend_routes.py    # Rute prieteni și recomandări
│   ├── services/               # Logica de business
│   │   ├── auth_service.py     # Logica autentificare (criptare, validare)
│   │   └── external_api.py     # Integrare TVMaze API
│   ├── security.py             # Verificare token-uri
│   └── instance/               # Baza de date SQLite
│       └── production.db
│
├── frontend/                   # Frontend web (HTML templates)
│   ├── app.py                  # Punctul de intrare al frontend-ului
│   ├── views/                  # View handlers (logica pentru pagini)
│   │   ├── auth_views.py       # Views pentru login/register
│   │   ├── dashboard_views.py  # Views pentru dashboard (My Movies)
│   │   └── friend_views.py     # Views pentru prieteni și recomandări
│   ├── templates/              # Template-uri HTML (Jinja2)
│   │   ├── base.html           # Template de bază
│   │   ├── login.html          # Pagină login
│   │   ├── register.html       # Pagină înregistrare
│   │   ├── dashboard.html      # Dashboard (My Movies)
│   │   ├── friends.html        # Pagină prieteni
│   │   ├── recommendations.html # Pagină recomandări
│   │   └── friend_profile.html # Profil prieten
│   ├── static/                 # Fișiere statice
│   │   ├── css/
│   │   │   └── style.css       # Stiluri (tema dark)
│   │   ├── js/
│   │   │   └── movie_search.js  # JavaScript pentru autocomplete
│   │   └── images/
│   │       └── logo.png        # Logo aplicație
│   └── utils/                  # Utilitare
│       ├── validators.py       # Validări input
│       └── api_client.py       # Client pentru API (opțional)
│
└── requirements.txt            # Dependențe Python
```

**Statistici:**
- **20 fișiere Python** (backend + frontend)
- **7 template-uri HTML** (Jinja2)
- **3 fișiere statice** (CSS, JS, imagini)

---

## 🚀 Instalare

### Cerințe
- Python 3.8 sau mai nou
- pip (package manager Python)

### Pași

1. **Clonează sau descarcă proiectul**

2. **Instalează dependențele:**
```bash
pip install -r requirements.txt
```

Dependențe instalate:
- `Flask==3.0.0` - Framework web
- `Werkzeug==3.0.1` - Securitate (criptare parole)
- `requests==2.31.0` - Client HTTP (pentru comunicare frontend-backend, opțional)

---

## ▶️ Rulare

Aplicația necesită **două servere Flask** care rulează simultan:
- **Backend** (port 5000): API REST pentru date
- **Frontend** (port 5001): Interfață web HTML

### Opțiunea 1: Script automat (Recomandat)

Folosește scriptul `start.py` pentru a porni ambele servere simultan:

```bash
cd movie-manager
python3 start.py
```

**Avantaje:**
- Pornește automat ambele servere
- Inițializează baza de date
- Afișează informații clare despre serverele pornite
- O singură comandă pentru tot

**Output:**
```
🎬 Movie Manager - Pornire servere
📡 Backend API:  http://localhost:5000
🌐 Frontend Web: http://localhost:5001
💡 Deschide browser-ul la: http://localhost:5001
```

**Oprire:** Apasă `Ctrl+C` pentru a opri ambele servere.

### Opțiunea 2: Pornire manuală (două terminale)

#### Terminal 1 - Backend API
```bash
cd movie-manager
python3 backend/app.py
```

Backend-ul va rula pe: `http://localhost:5000`

**Funcții:**
- Inițializează baza de date SQLite la pornire
- Servește API REST endpoints (JSON responses)
- Gestionează CORS pentru comunicare cu frontend-ul

#### Terminal 2 - Frontend Web
```bash
cd movie-manager
python3 frontend/app.py
```

Frontend-ul va rula pe: `http://localhost:5001`

**Funcții:**
- Servește pagini HTML (templates Jinja2)
- Gestionează sessions pentru autentificare
- Procesează form submissions
- Renderizează interfața utilizatorului

### Accesare Aplicație

Deschide browser-ul la: **http://localhost:5001**

**Notă:** Asigură-te că ambele servere rulează simultan!

---

## 🏗 Arhitectură

### Separare Backend/Frontend

Proiectul folosește o arhitectură **separată** cu două aplicații Flask:

#### Backend (`backend/`)
- **Rol**: API REST care returnează JSON
- **Port**: 5000
- **Funcții**:
  - Gestionare baza de date
  - Logica de business
  - Securitate (autentificare, validare)
  - Integrare API extern (TVMaze)
- **Endpoints**: `/api/*` (toate rutele au prefix `/api`)

#### Frontend (`frontend/`)
- **Rol**: Interfață web cu server-side rendering
- **Port**: 5001
- **Funcții**:
  - Generare HTML dinamic (Jinja2 templates)
  - Gestionare sessions
  - Procesare form submissions
  - Interacțiuni utilizator
- **Routes**: `/`, `/login`, `/register`, `/dashboard`, `/friends`, etc.

### Comunicare Backend ↔ Frontend

Frontend-ul comunică cu backend-ul în două moduri:

1. **Direct Import** (pentru logica de business):
   ```python
   # frontend/app.py
   from models.database import get_db_connection
   from services.auth_service import proceseaza_login
   ```

2. **HTTP Requests** (pentru API REST, opțional):
   ```python
   # frontend/utils/api_client.py
   import requests
   response = requests.get('http://localhost:5000/api/movies')
   ```

**Notă:** În implementarea actuală, frontend-ul folosește **direct import** pentru eficiență, dar backend-ul expune și API REST pentru flexibilitate.

---

## 🔌 API Endpoints

### Autentificare

#### `POST /api/register`
Înregistrare utilizator nou.

**Request:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response (201):**
```json
{
  "message": "Account created successfully"
}
```

#### `POST /api/login`
Autentificare utilizator.

**Request:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "token": "token_secret_pentru_testuser",
  "message": "Login successful"
}
```

### Filme

#### `GET /api/movies`
Obține toate filmele utilizatorului curent (grupate pe liste).

**Headers:**
```
Authorization: token_secret_pentru_username
```

**Response (200):**
```json
{
  "To Watch": [
    {"id": 1, "title": "The Matrix", "rating": "-"}
  ],
  "Watching": [],
  "Completed": [
    {"id": 2, "title": "Inception", "rating": "9"}
  ]
}
```

#### `POST /api/movies`
Adaugă un film nou.

**Headers:**
```
Authorization: token_secret_pentru_username
```

**Request:**
```json
{
  "title": "The Matrix",
  "status": "To Watch"
}
```

**Response (201):**
```json
{
  "message": "Movie added successfully",
  "movie_id": 1
}
```

#### `PUT /api/movies/<id>/move`
Mută un film între liste.

**Request:**
```json
{
  "new_status": "Watching"
}
```

#### `PUT /api/movies/<id>/rate`
Notează un film (1-10).

**Request:**
```json
{
  "rating": 9
}
```

#### `DELETE /api/movies/<id>`
Șterge un film.

### Prieteni

#### `GET /api/friends`
Obține lista de prieteni.

#### `POST /api/friends/add`
Adaugă un prieten.

**Request:**
```json
{
  "friend_username": "frienduser"
}
```

#### `GET /api/friends/<username>/movies`
Obține filmele unui prieten.

#### `POST /api/friends/recommend`
Recomandă un film unui prieten.

**Request:**
```json
{
  "friend_username": "frienduser",
  "movie_title": "The Matrix"
}
```

### Recomandări

#### `GET /api/recommendations`
Obține recomandările primite.

#### `DELETE /api/recommendations/<id>`
Șterge o recomandare.

### Căutare

#### `GET /api/search-movies?s=<search_term>`
Caută filme folosind TVMaze API.

**Response:**
```json
{
  "Response": "True",
  "Search": [
    {
      "Title": "The Matrix",
      "Year": "1999",
      "Type": "movie",
      "imdbID": "0133093"
    }
  ]
}
```

---

## 🖥 Frontend Views

### Autentificare

#### `GET /login`
Afișează pagina de login.

#### `POST /login`
Procesează login-ul utilizatorului.

#### `GET /register`
Afișează pagina de înregistrare.

#### `POST /register`
Procesează înregistrarea utilizatorului.

#### `GET /logout`
Deconectează utilizatorul (șterge session).

### Dashboard

#### `GET /dashboard`
Afișează dashboard-ul cu filmele utilizatorului (3 liste: To Watch, Watching, Completed).

#### `POST /movies/add`
Adaugă un film nou.

#### `POST /movies/<id>/move`
Mută un film între liste.

#### `POST /movies/<id>/rate`
Notează un film.

#### `POST /movies/<id>/delete`
Șterge un film.

### Prieteni

#### `GET /friends`
Afișează lista de prieteni.

#### `POST /friends/add`
Adaugă un prieten.

#### `GET /friends/<username>/movies`
Afișează profilul unui prieten cu filmele lui.

#### `POST /friends/recommend`
Recomandă un film unui prieten.

### Recomandări

#### `GET /recommendations`
Afișează recomandările primite.

#### `POST /recommendations/<id>/delete`
Șterge o recomandare.

---

## 💾 Baza de Date

Aplicația folosește **SQLite** pentru stocare persistentă.

### Schema Bazei de Date

#### Tabel `users`
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT  -- Hash criptat cu Werkzeug
);
```

#### Tabel `movies`
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    status TEXT,  -- 'To Watch', 'Watching', 'Completed'
    rating TEXT   -- '1' - '10' sau '-'
);
```

#### Tabel `friends`
```sql
CREATE TABLE friends (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    friend_id INTEGER,
    UNIQUE(user_id, friend_id)  -- Relație bidirecțională
);
```

#### Tabel `recommendations`
```sql
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY,
    from_user_id INTEGER,
    to_user_id INTEGER,
    movie_title TEXT
);
```

### Locație Baza de Date

Baza de date este stocată în: `backend/instance/production.db`

**Notă:** Baza de date este creată automat la prima rulare a backend-ului.

---

## 🔒 Securitate

### Criptare Parole

Parolele sunt criptate folosind **Werkzeug** (hash-uri securizate):

```python
from werkzeug.security import generate_password_hash, check_password_hash

# La înregistrare
password_hash = generate_password_hash(password)

# La login
is_valid = check_password_hash(stored_hash, password)
```

### Autentificare

Aplicația folosește două mecanisme de autentificare:

1. **Backend API**: Token-uri simple (format: `token_secret_pentru_<username>`)
   - Token-ul este verificat în `security.py`
   - Trimis în header `Authorization`

2. **Frontend Web**: Flask Sessions
   - Session-ul stochează `user_id` și `username`
   - Gestionat automat de Flask
   - Expiră la închiderea browser-ului

### Validare Input

Validări sunt implementate în:
- **Backend**: `backend/services/auth_service.py`
- **Frontend**: `frontend/utils/validators.py`

Validări:
- Username: minim 3 caractere, alfanumeric
- Password: minim 6 caractere
- Movie title: minim 1 caracter
- Rating: între 1 și 10

### Validare Strictă Filme

Aplicația implementează **validare strictă** pentru adăugarea și recomandarea filmelor:

- **Câmp hidden**: `movie_validated` indică dacă filmul a fost selectat din dropdown
- **Validare Python**: Backend-ul verifică `movie_validated == '1'` înainte de a permite adăugarea
- **Notificări**: Dacă filmul nu este selectat din dropdown, se afișează un flash message de eroare
- **Fără popup-uri**: Toate notificările sunt afișate pe site (fără `alert()` browser)

**Implementare:**
- JavaScript setează `movie_validated = '1'` când utilizatorul selectează un film din dropdown
- Python verifică acest câmp în `dashboard_views.py` și `friend_views.py`
- Dacă validarea eșuează, se returnează un flash message și se face redirect

### Validare Strictă Filme

Aplicația implementează **validare strictă** pentru adăugarea și recomandarea filmelor:

- **Câmp hidden**: `movie_validated` indică dacă filmul a fost selectat din dropdown
- **Validare Python**: Backend-ul verifică `movie_validated == '1'` înainte de a permite adăugarea
- **Notificări**: Dacă filmul nu este selectat din dropdown, se afișează un flash message de eroare
- **Fără popup-uri**: Toate notificările sunt afișate pe site (fără `alert()` browser)

**Implementare:**
- JavaScript setează `movie_validated = '1'` când utilizatorul selectează un film din dropdown
- Python verifică acest câmp în `dashboard_views.py` și `friend_views.py`
- Dacă validarea eșuează, se returnează un flash message și se face redirect

---

## 🌐 API Extern

### TVMaze API

Aplicația integrează **TVMaze API** pentru căutare filme, seriale și show-uri TV.

- **URL**: `http://api.tvmaze.com/search/shows`
- **Gratuit**: Da, nu necesită cheie API
- **Endpoint local**: `/api/search-movies?s=<search_term>`

**Exemplu request:**
```
GET http://localhost:5000/api/search-movies?s=matrix
```

**Exemplu response:**
```json
{
  "Response": "True",
  "Search": [
    {
      "Title": "The Matrix",
      "Year": "1999",
      "Type": "movie",
      "imdbID": "0133093",
      "Poster": "https://..."
    }
  ]
}
```

**Implementare:**
- Backend: `backend/services/external_api.py`
- Frontend: `frontend/static/js/movie_search.js` (autocomplete JavaScript)

---

## 🎨 Interfață Utilizator

### Tema Dark

Aplicația folosește o temă dark modernă:
- Fundal: `#0a0a0a` (negru)
- Containere: `#171717`, `#252525` (gri închis)
- Text: `#d3d3d3`, `#ffffff` (gri deschis, alb)
- Accente: Tranziții și animații smooth

### Componente UI

- **Sidebar**: Navigare între pagini (My Movies, Friends, Recommendations)
- **Dropdown Autocomplete**: Căutare filme cu rezultate în timp real
- **Flash Messages**: Notificări pentru acțiuni (success, error)
- **Confirm Dialog**: Dialog de confirmare pentru ștergere
- **Movie Lists**: Trei coloane pentru To Watch, Watching, Completed

### JavaScript Minim

JavaScript este folosit doar pentru:
- **Autocomplete search**: Căutare în timp real cu debounce (300ms)
- **Dropdown interactions**: Click handlers pentru selectare filme
- **Scroll management**: Gestionare scroll în dropdown-uri
- **Enter key**: Detectare Enter key în formularul de login
- **Dialog custom**: Funcționalitate pentru dialog-ul de confirmare custom

**Fișier**: `frontend/static/js/movie_search.js` (~250 linii)

**Notă**: Aplicația **nu folosește** `alert()` sau `confirm()` nativ JavaScript. Toate notificările și confirmările sunt implementate folosind componente custom care se potrivesc cu design-ul aplicației.

---

## 📝 Note Tehnice

### De ce două servere Flask?

1. **Separare responsabilități**: Backend (API) vs Frontend (UI)
2. **Scalabilitate**: Backend-ul poate servi și alte clienți (mobile, etc.)
3. **Flexibilitate**: Frontend-ul poate fi înlocuit cu alt framework
4. **Testare**: Poți testa API-ul independent de UI

### De ce Server-Side Rendering?

1. **100% Python**: Majoritatea logicii în Python (cerință proiect)
2. **SEO friendly**: HTML generat pe server
3. **Securitate**: Validări pe server
4. **Simplitate**: Fără complexitate SPA (Single Page Application)

### De ce JavaScript minim?

JavaScript este folosit doar pentru interacțiuni în timp real imposibile în Python:
- **Autocomplete**: Detectare `oninput` (fiecare tastă)
- **Scroll events**: Detectare scroll în dropdown
- **Click handlers**: Selectare din dropdown

**Alternativa Python**: Ar necesita refresh la fiecare interacțiune (experiență slabă).

---

## 🐛 Troubleshooting

### Backend nu pornește
- Verifică dacă portul 5000 este liber
- Verifică dacă Python 3.8+ este instalat
- Verifică dacă dependențele sunt instalate: `pip install -r requirements.txt`

### Frontend nu pornește
- Verifică dacă portul 5001 este liber
- Verifică dacă backend-ul rulează (frontend-ul depinde de backend)
- Verifică dacă toate importurile funcționează

### Autocomplete nu funcționează
- Verifică dacă backend-ul rulează pe port 5000
- Verifică consola browser-ului pentru erori JavaScript
- Verifică dacă `movie_search.js` este încărcat corect

### Baza de date nu se creează
- Verifică permisiuni de scriere în `backend/instance/`
- Verifică dacă backend-ul pornește corect (vezi logs)

---

## 📚 Resurse

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [TVMaze API](https://www.tvmaze.com/api)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security)

---

## 👤 Autor

Proiect realizat pentru cursul de Inteligentă Artificială, Universitatea Politehnica București.

---

## 📄 Licență

Acest proiect este realizat în scop educațional.

