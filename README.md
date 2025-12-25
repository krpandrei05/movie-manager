# Movie Manager

Aplicatie web pentru gestionarea filmelor, serialelor si show-urilor TV. Utilizatorii pot crea liste de filme, adauga prieteni, recomanda filme si vedea ce filme au prietenii lor.

## Functionalitati

### Autentificare
- **Inregistrare**: Utilizatorii pot crea un cont nou cu username si parola
- **Login**: Utilizatorii se pot autentifica cu username si parola
- **Securitate**: Parolele sunt criptate in baza de date folosind hash-uri

### Gestionare filme
- **Adaugare filme**: Utilizatorii pot adauga filme in trei liste:
  - **To Watch**: Filme pe care vrea sa le vada
  - **Watching**: Filme pe care le urmareste in prezent
  - **Completed**: Filme pe care le-a terminat de vazut
- **Mutare intre liste**: Utilizatorii pot muta filme intre cele trei liste
- **Notare filme**: Pentru filmele din lista "Completed", utilizatorii pot da o nota de la 1 la 10
- **Stergere filme**: Utilizatorii pot sterge filme din liste
- **Cautare filme**: Integrare cu TVMaze API pentru cautarea filmelor, serialelor si show-urilor TV (gratuit, fara cheie API)

### Prieteni
- **Adaugare prieteni**: Utilizatorii pot adauga alti utilizatori ca prieteni
- **Vizualizare lista prieteni**: Utilizatorii pot vedea lista cu toti prietenii lor
- **Vizualizare filme prieteni**: Utilizatorii pot vedea toate listele de filme ale prietenilor (To Watch, Watching, Completed)
- **Recomandare filme**: Utilizatorii pot recomanda filme prietenilor lor

### Recomandari
- **Vizualizare recomandari**: Utilizatorii pot vedea toate recomandarile primite de la prieteni
- **Stergere recomandari**: Utilizatorii pot sterge recomandarile primite

## Structura proiectului

```
movie-manager/
├── server/                    # Folderul principal al serverului
│   ├── app.py                 # Punctul de intrare al aplicatiei Flask
│   │                          # Initializeaza aplicatia, gestioneaza CORS, inregistreaza blueprint-urile
│   │
│   ├── routes/                # Folder pentru rutele aplicatiei
│   │   ├── auth_routes.py     # Rutele pentru autentificare (/login, /register)
│   │   ├── movie_routes.py    # Rutele pentru filme (/movies, /movies/<id>/move, /movies/<id>/rate, /user/username)
│   │   └── friend_routes.py   # Rutele pentru prieteni (/friends, /friends/<username>/movies, /recommendations)
│   │
│   ├── models/                # Folder pentru gestionarea bazei de date
│   │   └── database.py        # Functii pentru conexiune la baza de date si initializarea tabelelor
│   │
│   ├── services/              # Folder pentru logica de business
│   │   ├── auth_service.py    # Logica pentru inregistrare si login (criptare parole, verificare date)
│   │   └── external_api.py    # Logica pentru interogarea TVMaze API (cautare filme)
│   │
│   ├── security.py            # Functii pentru verificarea token-urilor de autentificare
│   │
│   ├── instance/              # Folder pentru baza de date
│   │   └── production.db      # Baza de date SQLite cu toate datele
│   │
│   ├── static/                # Fisiere statice (CSS, JavaScript, imagini)
│   │   ├── css/
│   │   │   └── style.css      # Stilurile pentru interfata web (tema dark, animatii, layout)
│   │   ├── js/
│   │   │   └── app.js         # Logica frontend (apeluri API, manipulare DOM, notificari)
│   │   └── images/
│   │       └── logo.png       # Logo-ul aplicatiei
│   │
│   └── templates/             # Template-uri HTML
│       └── index.html         # Pagina principala HTML (login, register, dashboard, pagini)
│
└── requirements.txt           # Biblioteci Python necesare (Flask, Werkzeug)
```

## Ce face fiecare fisier

### app.py
Punctul de intrare al aplicatiei. Initializeaza aplicatia Flask, gestioneaza header-ele CORS pentru comunicarea frontend-backend, inregistreaza toate blueprint-urile (rutele) si porneste serverul.

### routes/auth_routes.py
Contine rutele pentru autentificare:
- `/register` - pentru crearea unui cont nou
- `/login` - pentru autentificarea unui utilizator

### routes/movie_routes.py
Contine rutele pentru gestionarea filmelor:
- `GET /movies` - obtine toate filmele utilizatorului grupate pe liste
- `POST /movies` - adauga un film nou
- `PUT /movies/<id>/move` - muta un film intre liste
- `PUT /movies/<id>/rate` - noteaza un film (1-10)
- `DELETE /movies/<id>` - sterge un film
- `GET /user/username` - obtine username-ul utilizatorului curent

### routes/friend_routes.py
Contine rutele pentru prieteni si recomandari:
- `GET /friends` - obtine lista de prieteni
- `POST /friends/add` - adauga un prieten nou
- `GET /friends/<username>/movies` - obtine filmele unui prieten (toate listele)
- `POST /friends/recommend` - recomanda un film unui prieten
- `GET /recommendations` - obtine recomandarile primite
- `DELETE /recommendations/<id>` - sterge o recomandare primita

### models/database.py
Contine functiile pentru gestionarea bazei de date:
- `get_db_connection()` - deschide o conexiune la baza de date SQLite
- `init_db()` - creeaza toate tabelele necesare (users, movies, friends, recommendations)

### services/auth_service.py
Contine logica de business pentru autentificare:
- `proceseaza_inregistrare()` - proceseaza cererea de inregistrare (verifica datele, cripteaza parola, salveaza in baza de date)
- `proceseaza_login()` - proceseaza cererea de login (verifica username si parola, returneaza token)

### services/external_api.py
Contine logica pentru interogarea API-ului extern:
- `search_movies()` - cauta filme, seriale si show-uri TV folosind TVMaze API (gratuit, fara cheie)

### security.py
Contine functiile pentru securitate:
- `verifica_token()` - verifica daca un token de autentificare este valid si returneaza id-ul utilizatorului

### static/css/style.css
Contine toate stilurile pentru interfata web: tema dark, animatii, layout-uri pentru pagini, butoane, liste, notificari.

### static/js/app.js
Contine toata logica frontend: apeluri catre API-ul backend, manipulare DOM pentru afisarea datelor, gestionarea notificarilor, validari, cautare filme cu autocomplete.

### templates/index.html
Pagina principala HTML care contine: formularul de login, formularul de register, dashboard-ul cu listele de filme, pagina de prieteni, pagina de recomandari, pagina de profil prieten.

## Utilizatori de test

Pentru testare, exista urmatorii utilizatori deja creati in baza de date:

- **Username**: `test`
  - **Parola**: `test123`

- **Username**: `test1`
  - **Parola**: `test123`

- **Username**: `test2`
  - **Parola**: `test123`

Poti folosi acesti utilizatori pentru a testa functionalitatile de prieteni si recomandari (adauga-i ca prieteni, recomanda-le filme, etc.).

## Cum se porneste aplicatia

1. Instaleaza dependentele:
```bash
pip install -r requirements.txt
```

2. Porneste serverul:
```bash
python3 server/app.py
```

3. Deschide browserul la adresa:
```
http://127.0.0.1:5000
```

## API extern folosit

Aplicatia foloseste **TVMaze API** pentru cautarea filmelor, serialelor si show-urilor TV.

- **Nume API**: TVMaze
- **URL**: `http://api.tvmaze.com/search/shows`
- **Gratuit**: Da, nu necesita cheie API
- **Functionalitate**: Cauta filme, seriale si show-uri TV pe baza unui termen de cautare
- **Endpoint in aplicatie**: `/api/search-movies`

API-ul este accesat prin intermediul serverului (proxy) pentru a evita problemele de CORS si pentru a transforma raspunsul in formatul necesar aplicatiei.

## Tehnologii folosite

- **Backend**: Flask (Python)
- **Baza de date**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **API extern**: TVMaze (pentru cautare filme, seriale, show-uri TV)
- **Securitate**: Werkzeug (pentru criptare parole)
