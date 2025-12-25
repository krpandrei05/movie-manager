// Variabila globala pentru salvarea token-ului de autentificare
let token = null;

// Adresa serverului backend
const API_URL = 'http://localhost:5000';

// Functie pentru afisarea notificarilor pe site
function showNotification(message, type) {
    // Preluam elementul de notificare
    const notification = document.getElementById('notification');

    // Setam mesajul
    notification.textContent = message;

    // Setam tipul de notificare (success sau error)
    notification.className = `notification ${type}`;
    
    // Ascundem notificarea dupa 3 secunde
    setTimeout(() => {notification.className = 'notification';}, 3000);
}

// Functie pentru gestionarea apasarii tastei Enter in formularul de login
function handleLoginEnter(event) {
    // Verificam daca tasta apasata este Enter
    if (event.key === 'Enter') {

        // Apelam functia de login
        login();
    }
}

// Functie pentru gestionarea apasarii tastei Enter in formularul de register
function handleRegisterEnter(event) {
    // Verificam daca tasta apasata este Enter
    if (event.key === 'Enter') {

        // Apelam functia de register
        register();
    }
}

// Functie pentru procesarea login-ului
async function login() {
    // Preluam valorile din campurile de input
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        // Trimitem cererea de autentificare la server
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        
        // Verificam daca autentificarea a reusit
        if (response.status === 200) {
            const data = await response.json();

            // Salvam token-ul pentru request-urile viitoare
            token = data.token;

            // Afisam dashboard-ul
            showDashboard();
        } else {
            // Afisam mesaj de eroare daca autentificarea a esuat
            showNotification('Invalid credentials', 'error');
        }
    } catch (error) {
        // Afisam eroare daca apare o problema la conectare
        showNotification('Connection error', 'error');
    }
}

// Functie pentru procesarea inregistrarii unui cont nou
async function register() {
    // Preluam valorile din campurile de input
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    
    try {
        // Trimitem cererea de inregistrare la server
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        
        // Verificam daca inregistrarea a reusit
        if (response.status === 201) {

            // Golim campurile de register
            document.getElementById('register-username').value = '';
            document.getElementById('register-password').value = '';

            // Afisam notificare de succes
            showNotification('Account created successfully! Please login.', 'success');

            // Revenim la formularul de login pentru a introduce datele manual
            showLogin();
        } else {
            // Preluam mesajul de eroare de la server
            const data = await response.json();
            showNotification(data.message || 'Account creation failed', 'error');
        }
    } catch (error) {
        // Afisam eroare daca apare o problema la conectare
        showNotification('Connection error', 'error');
    }
}

// Functie pentru afisarea formularului de login
function showLogin() {
    // Afisam formularul de login
    document.getElementById('login-form').style.display = 'block';

    // Ascundem formularul de inregistrare
    document.getElementById('register-form').style.display = 'none';
}

// Functie pentru afisarea formularului de inregistrare
function showRegister() {
    // Ascundem formularul de login
    document.getElementById('login-form').style.display = 'none';

    // Afisam formularul de inregistrare
    document.getElementById('register-form').style.display = 'block';
}

// Functie pentru afisarea dashboard-ului principal
function showDashboard() {
    // Ascundem containerul de autentificare
    document.getElementById('auth-container').style.display = 'none';

    // Afisam dashboard-ul
    document.getElementById('dashboard').style.display = 'block';

    // Incarcam filmele utilizatorului
    loadMovies();
}

// Functie pentru delogare
function logout() {
    // Stergem token-ul
    token = null;

    // Afisam din nou formularul de autentificare
    document.getElementById('auth-container').style.display = 'block';

    // Ascundem dashboard-ul
    document.getElementById('dashboard').style.display = 'none';
}

// Functie pentru adaugarea unui film nou
async function addMovie() {
    // Preluam titlul filmului din campul de input
    const title = document.getElementById('movie-title').value;
    
    // Verificam daca titlul nu este gol
    if (!title) return;
    
    try {
        // Trimitem cererea de adaugare film la server
        const response = await fetch(`${API_URL}/movies`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({title})
        });
        
        // Verificam daca adaugarea a reusit
        if (response.status === 201) {
            // Golim campul de input
            document.getElementById('movie-title').value = '';

            // Reincarcam lista de filme
            loadMovies();
        }
    } catch (error) {
        // Afisam eroare daca apare o problema
        showNotification('Error adding movie', 'error');
    }
}

// Functie pentru incarcarea filmelor de la server
async function loadMovies() {
    try {
        // Cerem lista de filme de la server
        const response = await fetch(`${API_URL}/movies`, {
            headers: {'Authorization': token}
        });
        
        // Verificam daca cererea a reusit
        if (response.status === 200) {
            // Preluam datele de filme
            const movies = await response.json();

            // Afisam filmele in interfata
            displayMovies(movies);
        }
    } catch (error) {
        // Afisam eroare in consola daca apare o problema
        console.error('Eroare la încărcarea filmelor');
    }
}

// Functie pentru afisarea filmelor in interfata
function displayMovies(movies) {
    // Afisam filmele din lista "To Watch"
    document.getElementById('to-watch-list').innerHTML = 
        movies['To Watch'].map(m => createMovieItem(m, 'To Watch')).join('');
    
    // Afisam filmele din lista "Watching"
    document.getElementById('watching-list').innerHTML = 
        movies['Watching'].map(m => createMovieItem(m, 'Watching')).join('');
    
    // Afisam filmele din lista "Completed"
    document.getElementById('completed-list').innerHTML = 
        movies['Completed'].map(m => createMovieItem(m, 'Completed')).join('');
}

// Functie pentru crearea elementului HTML al unui film
function createMovieItem(movie, currentStatus) {
    // Lista cu toate statusurile posibile
    const statuses = ['To Watch', 'Watching', 'Completed'];

    // Filtram statusurile pentru a exclude statusul curent
    const otherStatuses = statuses.filter(s => s !== currentStatus);
    
    // Returnam HTML-ul pentru un film cu butoane pentru mutare si stergere
    return `
        <div class="movie-item">
            <span>${movie.title}</span>
            <div>
                ${otherStatuses.map(status => 
                    `<button onclick="moveMovie(${movie.id}, '${status}')">→ ${status}</button>`
                ).join('')}
                <button onclick="deleteMovie(${movie.id})">Delete</button>
            </div>
        </div>
    `;
}

// Functie pentru mutarea unui film intre liste
async function moveMovie(id, newStatus) {
    try {
        // Trimitem cererea de mutare film la server
        const response = await fetch(`${API_URL}/movies/${id}/move`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({new_list: newStatus})
        });
        
        // Verificam daca mutarea a reusit
        if (response.status === 200) {
            // Reincarcam lista de filme
            loadMovies();
        }
    } catch (error) {
        // Afisam eroare daca apare o problema
        showNotification('Error moving movie', 'error');
    }
}

// Functie pentru stergerea unui film
async function deleteMovie(id) {
    // Cerem confirmare de la utilizator inainte de stergere
    // Folosim confirm() doar pentru stergere deoarece este o actiune critica
    if (!confirm('Are you sure you want to delete this movie?')) return;
    
    try {
        // Trimitem cererea de stergere film la server
        const response = await fetch(`${API_URL}/movies/${id}`, {
            method: 'DELETE',
            headers: {'Authorization': token}
        });
        
        // Verificam daca stergerea a reusit
        if (response.status === 200) {
            // Reincarcam lista de filme
            loadMovies();
        }
    } catch (error) {
        // Afisam eroare daca apare o problema
        showNotification('Error deleting movie', 'error');
    }
}