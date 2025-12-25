// Variabila globala pentru salvarea token-ului de autentificare
let token = null;

// Adresa serverului backend
const API_URL = 'http://localhost:5000';

// URL pentru cautarea filmelor, serialelor si show-urilor TV (folosim endpoint-ul nostru de proxy catre TVMaze API)
// TVMaze API este complet gratuit si nu necesita cheie API
const MOVIE_SEARCH_URL = `${API_URL}/api/search-movies`;

// Variabile pentru debounce la cautare
let searchTimeout = null;
let currentSearchResults = [];

// Variabile pentru a salva filmele selectate (pentru validare)
let selectedMovieDashboard = null; // Filmul selectat din dashboard
let selectedMovieRecommend = null; // Filmul selectat pentru recomandare

// Variabila pentru a salva callback-ul de confirmare
let confirmCallback = null;

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

// Functie pentru afisarea confirmarii personalizate pe site
function showConfirm(message, onConfirm) {
    // Salvam callback-ul de confirmare
    confirmCallback = onConfirm;
    
    // Setam mesajul de confirmare
    document.getElementById('confirm-message').textContent = message;
    
    // Afisam dialog-ul de confirmare
    document.getElementById('confirm-dialog').classList.add('show');
}

// Functie pentru ascunderea confirmarii
function hideConfirm() {
    document.getElementById('confirm-dialog').classList.remove('show');
    confirmCallback = null;
}

// Event listeners pentru butoanele de confirmare
document.addEventListener('DOMContentLoaded', function() {
    // Butonul "Yes"
    document.getElementById('confirm-yes').addEventListener('click', function() {
        if (confirmCallback) {
            confirmCallback();
        }
        hideConfirm();
    });
    
    // Butonul "No"
    document.getElementById('confirm-no').addEventListener('click', function() {
        hideConfirm();
    });
    
    // Inchidere la click pe background
    document.getElementById('confirm-dialog').addEventListener('click', function(e) {
        if (e.target === this) {
            hideConfirm();
        }
    });
});

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
    document.getElementById('dashboard').style.display = 'flex';

    // Afisam pagina Dashboard
    showPage('dashboard');

    // Incarcam username-ul utilizatorului
    loadUsername();

    // Incarcam filmele utilizatorului
    loadMovies();

    // Incarcam lista de prieteni
    loadFriends();
}

// Functie pentru incarcarea username-ului utilizatorului
async function loadUsername() {
    try {
        // Cerem username-ul de la server
        const response = await fetch(`${API_URL}/user/username`, {
            headers: {'Authorization': token}
        });
        
        // Verificam daca cererea a reusit
        if (response.status === 200) {
            // Preluam datele
            const data = await response.json();
            
            // Afisam username-ul in header
            document.getElementById('username-display').textContent = data.username;
        }
    } catch (error) {
        // Afisam eroare in consola daca apare o problema
        console.error('Eroare la incarcarea username-ului');
    }
}

// Functie pentru incarcarea listei de prieteni
async function loadFriends() {
    try {
        // Cerem lista de prieteni de la server
        const response = await fetch(`${API_URL}/friends`, {
            headers: {'Authorization': token}
        });
        
        // Verificam daca cererea a reusit
        if (response.status === 200) {
            // Preluam lista de prieteni
            const friends = await response.json();
            
            // Afisam prietenii in interfata
            displayFriends(friends);
        }
    } catch (error) {
        // Afisam eroare in consola daca apare o problema
        console.error('Eroare la incarcarea prietenilor');
    }
}

// Functie pentru afisarea prietenilor in interfata (pentru sidebar)
function displayFriends(friends) {
    // Preluam containerul pentru lista de prieteni
    const friendsList = document.getElementById('friends-list');
    
    // Verificam daca exista prieteni
    if (friends.length === 0) {
        // Afisam mesaj daca nu exista prieteni
        friendsList.innerHTML = '<p style="color: #888; text-align: center; padding: 20px;">No friends yet. Add some!</p>';
        return;
    }
    
    // Cream elementele HTML pentru fiecare prieten cu click handler
    friendsList.innerHTML = friends.map(friend => 
        `<div class="friend-item" onclick="showFriendProfile('${friend}')">${friend}</div>`
    ).join('');
}

// Functie pentru afisarea prietenilor in pagina Friends
function displayFriendsPage(friends) {
    // Preluam containerul pentru lista de prieteni din pagina
    const friendsList = document.getElementById('friends-list-page');
    
    // Verificam daca exista prieteni
    if (friends.length === 0) {
        // Afisam mesaj daca nu exista prieteni
        friendsList.innerHTML = '<p style="color: #888; text-align: center; padding: 20px;">No friends yet. Add some!</p>';
        return;
    }
    
    // Cream elementele HTML pentru fiecare prieten cu click handler
    friendsList.innerHTML = friends.map(friend => 
        `<div class="friend-card" onclick="showFriendProfile('${friend}')">${friend}</div>`
    ).join('');
}

// Functie pentru adaugarea unui prieten nou
async function addFriend() {
    // Preluam username-ul prietenului din campul de input
    const friendUsername = document.getElementById('friend-username').value;
    
    // Verificam daca username-ul nu este gol
    if (!friendUsername || !friendUsername.trim()) {
        showNotification('Please enter a username', 'error');
        return;
    }
    
    try {
        // Trimitem cererea de adaugare prieten la server
        const response = await fetch(`${API_URL}/friends/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({friend_username: friendUsername.trim()})
        });
        
        // Verificam daca adaugarea a reusit
        if (response.status === 201) {
            // Golim campul de input
            document.getElementById('friend-username').value = '';
            
            // Afisam notificare de succes
            showNotification('Friend added successfully!', 'success');
            
            // Reincarcam lista de prieteni
            loadFriends();
        } else {
            // Preluam mesajul de eroare de la server
            const data = await response.json();
            showNotification(data.message || 'Error adding friend', 'error');
        }
    } catch (error) {
        // Afisam eroare daca apare o problema
        showNotification('Connection error', 'error');
    }
}

// Functie pentru navigare intre pagini
function showPage(pageName) {
    // Ascundem toate paginile
    const pages = ['dashboard', 'friends', 'recommendations', 'friend-profile'];
    pages.forEach(page => {
        const pageElement = document.getElementById(`page-${page}`);
        if (pageElement) {
            pageElement.style.display = 'none';
        }
    });
    
    // Afisam pagina selectata
    const selectedPage = document.getElementById(`page-${pageName}`);
    if (selectedPage) {
        selectedPage.style.display = 'block';
    }
    
    // Actualizam meniul lateral
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-page') === pageName) {
            item.classList.add('active');
        }
    });
    
    // Incarcam datele pentru pagina selectata
    if (pageName === 'friends') {
        loadFriendsPage();
    } else if (pageName === 'recommendations') {
        loadRecommendations();
    }
}

// Functie pentru afisarea profilului unui prieten
function showFriendProfile(friendUsername) {
    // Ascundem toate paginile
    const pages = ['dashboard', 'movies', 'friends', 'recommendations', 'friend-profile'];
    pages.forEach(page => {
        const pageElement = document.getElementById(`page-${page}`);
        if (pageElement) {
            pageElement.style.display = 'none';
        }
    });
    
    // Afisam pagina de profil prieten
    document.getElementById('page-friend-profile').style.display = 'block';
    
    // Actualizam numele prietenului in header
    document.getElementById('friend-profile-name').textContent = `${friendUsername}'s Profile`;
    
    // Salvam username-ul prietenului pentru recomandari
    window.currentFriendUsername = friendUsername;
    
    // Incarcam filmele prietenului
    loadFriendMovies(friendUsername);
}

// Functie pentru incarcarea prietenilor in pagina Friends
async function loadFriendsPage() {
    try {
        const response = await fetch(`${API_URL}/friends`, {
            headers: {'Authorization': token}
        });
        
        if (response.status === 200) {
            const friends = await response.json();
            displayFriendsPage(friends);
        }
    } catch (error) {
        console.error('Eroare la incarcarea prietenilor');
    }
}

// Functie pentru adaugarea unui prieten din pagina Friends
async function addFriendFromPage() {
    const friendUsername = document.getElementById('friend-username-page').value;
    
    if (!friendUsername || !friendUsername.trim()) {
        showNotification('Please enter a username', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/friends/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({friend_username: friendUsername.trim()})
        });
        
        if (response.status === 201) {
            document.getElementById('friend-username-page').value = '';
            showNotification('Friend added successfully!', 'success');
            loadFriendsPage();
            loadFriends(); // Reincarcam si in sidebar
        } else {
            const data = await response.json();
            showNotification(data.message || 'Error adding friend', 'error');
        }
    } catch (error) {
        showNotification('Connection error', 'error');
    }
}

// Functie pentru incarcarea filmelor unui prieten
async function loadFriendMovies(friendUsername) {
    try {
        const response = await fetch(`${API_URL}/friends/${friendUsername}/movies`, {
            headers: {'Authorization': token}
        });
        
        if (response.status === 200) {
            const movies = await response.json();
            displayFriendMovies(movies);
        } else {
            const data = await response.json();
            showNotification(data.message || 'Error loading friend movies', 'error');
        }
    } catch (error) {
        showNotification('Connection error', 'error');
    }
}

// Functie pentru afisarea filmelor unui prieten (toate listele)
function displayFriendMovies(movies) {
    // Afisam lista "To Watch"
    const toWatchList = document.getElementById('friend-to-watch-list');
    if (movies['To Watch'] && movies['To Watch'].length > 0) {
        toWatchList.innerHTML = movies['To Watch'].map(movie => `
            <div class="friend-movie-item">
                <span>${movie.title}</span>
            </div>
        `).join('');
    } else {
        toWatchList.innerHTML = '<p style="color: #888; text-align: center; padding: 10px; font-size: 0.9em;">No movies in this list.</p>';
    }
    
    // Afisam lista "Watching"
    const watchingList = document.getElementById('friend-watching-list');
    if (movies['Watching'] && movies['Watching'].length > 0) {
        watchingList.innerHTML = movies['Watching'].map(movie => `
            <div class="friend-movie-item">
                <span>${movie.title}</span>
            </div>
        `).join('');
    } else {
        watchingList.innerHTML = '<p style="color: #888; text-align: center; padding: 10px; font-size: 0.9em;">No movies in this list.</p>';
    }
    
    // Afisam lista "Completed"
    const completedList = document.getElementById('friend-completed-list');
    if (movies['Completed'] && movies['Completed'].length > 0) {
        completedList.innerHTML = movies['Completed'].map(movie => `
            <div class="friend-movie-item">
                <span>${movie.title}</span>
                ${movie.rating && movie.rating !== '-' ? `<span class="friend-movie-rating">(${movie.rating}/10)</span>` : ''}
            </div>
        `).join('');
    } else {
        completedList.innerHTML = '<p style="color: #888; text-align: center; padding: 10px; font-size: 0.9em;">No movies in this list.</p>';
    }
}

// Functie pentru recomandarea unui film unui prieten
async function recommendMovie() {
    const movieTitle = document.getElementById('recommend-movie-title').value;
    const friendUsername = window.currentFriendUsername;
    
    if (!movieTitle || !movieTitle.trim()) {
        showNotification('Please enter a movie title', 'error');
        return;
    }
    
    // Verificam daca filmul a fost selectat din lista de rezultate (validare)
    if (!selectedMovieRecommend) {
        showNotification('Please select a movie from the search results', 'error');
        return;
    }
    
    // Verificam daca titlul din input corespunde cu filmul selectat
    if (movieTitle.trim() !== selectedMovieRecommend.Title) {
        showNotification('Please select a movie from the search results', 'error');
        return;
    }
    
    if (!friendUsername) {
        showNotification('Friend not selected', 'error');
        return;
    }
    
    // Ascundem rezultatele cautarii
    hideSearchResultsRecommend();
    
    try {
        const response = await fetch(`${API_URL}/friends/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({
                friend_username: friendUsername,
                movie_title: movieTitle.trim()
            })
        });
        
        if (response.status === 201) {
            document.getElementById('recommend-movie-title').value = '';
            
            // Resetam filmul selectat
            selectedMovieRecommend = null;
            
            showNotification('Recommendation sent successfully!', 'success');
        } else {
            const data = await response.json();
            showNotification(data.message || 'Error sending recommendation', 'error');
        }
    } catch (error) {
        showNotification('Connection error', 'error');
    }
}

// Functie pentru incarcarea recomandarilor primite
async function loadRecommendations() {
    try {
        const response = await fetch(`${API_URL}/recommendations`, {
            headers: {'Authorization': token}
        });
        
        if (response.status === 200) {
            const recommendations = await response.json();
            displayRecommendations(recommendations);
        }
    } catch (error) {
        console.error('Eroare la incarcarea recomandarilor');
    }
}

// Functie pentru afisarea recomandarilor
function displayRecommendations(recommendations) {
    const recommendationsList = document.getElementById('recommendations-list');
    
    if (recommendations.length === 0) {
        recommendationsList.innerHTML = '<p style="color: #888; text-align: center; padding: 20px;">No recommendations yet.</p>';
        return;
    }
    
    recommendationsList.innerHTML = recommendations.map(rec => `
        <div class="recommendation-card">
            <button class="recommendation-delete-btn" onclick="deleteRecommendation(${rec.id})" title="Delete recommendation">
                <span class="delete-icon">×</span>
            </button>
            <h4>${rec.movie_title}</h4>
            <div class="recommendation-from">Recommended by: ${rec.from_username}</div>
        </div>
    `).join('');
}

// Functie pentru stergerea unei recomandari
async function deleteRecommendation(recommendationId) {
    // Afisam confirmare personalizata pe site
    showConfirm('Are you sure you want to delete this recommendation?', async function() {
        try {
            // Trimitem cererea de stergere recomandare la server
            const response = await fetch(`${API_URL}/recommendations/${recommendationId}`, {
                method: 'DELETE',
                headers: {'Authorization': token}
            });
            
            // Verificam daca stergerea a reusit
            if (response.status === 200) {
                // Afisam notificare de succes pe site
                showNotification('Recommendation deleted successfully!', 'success');
                
                // Reincarcam lista de recomandari
                loadRecommendations();
            } else {
                // Preluam mesajul de eroare de la server si il afisam pe site
                const data = await response.json();
                showNotification(data.message || 'Error deleting recommendation', 'error');
            }
        } catch (error) {
            // Afisam eroare pe site daca apare o problema
            showNotification('Connection error. Please try again.', 'error');
        }
    });
}

// Functie pentru toggle sidebar (retract/expand meniu)
function toggleSidebar() {
    // Preluam elementul sidebar
    const sidebar = document.querySelector('.sidebar');
    
    // Toggle clasa collapsed
    sidebar.classList.toggle('collapsed');
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

// Functie pentru cautarea filmelor pe TVMaze API (cu debounce)
function searchMovies(searchTerm) {
    // Anulam timeout-ul anterior daca exista
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    // Daca campul este gol, ascundem rezultatele si resetam filmul selectat
    if (!searchTerm || searchTerm.trim().length < 2) {
        hideSearchResults();
        selectedMovieDashboard = null; // Resetam filmul selectat cand se modifica input-ul
        return;
    }
    
    // Asteptam 300ms inainte de a face request-ul (debounce)
    searchTimeout = setTimeout(async () => {
        try {
            // Facem request catre endpoint-ul nostru de proxy pentru cautare
            const response = await fetch(`${MOVIE_SEARCH_URL}?s=${encodeURIComponent(searchTerm.trim())}`);
            const data = await response.json();
            
            // Verificam daca cautarea a reusit
            if (data.Response === 'True' && data.Search) {
                // Salvam rezultatele
                currentSearchResults = data.Search;
                // Afisam rezultatele in dropdown
                displaySearchResults(currentSearchResults, 'movie-search-results');
            } else {
                // Daca nu sunt rezultate, afisam mesaj
                const resultsDiv = document.getElementById('movie-search-results');
                resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
                resultsDiv.classList.add('show');
            }
        } catch (error) {
            // In caz de eroare, afisam mesaj
            const resultsDiv = document.getElementById('movie-search-results');
            resultsDiv.innerHTML = '<div class="movie-search-error">Error searching movies</div>';
            resultsDiv.classList.add('show');
        }
    }, 300);
}

// Functie pentru afisarea rezultatelor cautarii
function displaySearchResults(results, containerId) {
    const resultsDiv = document.getElementById(containerId);
    
    if (!results || results.length === 0) {
        resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
        resultsDiv.classList.add('show');
        return;
    }
    
    // Cream HTML-ul pentru fiecare rezultat
    resultsDiv.innerHTML = results.map((movie, index) => `
        <div class="movie-search-item" onclick="selectMovie('${movie.Title}', '${containerId}')">
            <div class="movie-title">${movie.Title}</div>
            <div class="movie-year">${movie.Year}</div>
            <div class="movie-type">${movie.Type}</div>
        </div>
    `).join('');
    
    // Afisam dropdown-ul
    resultsDiv.classList.add('show');
}

// Functie pentru selectarea unui film din lista de rezultate
function selectMovie(movieTitle, containerId) {
    // Cautam filmul selectat in rezultatele curente pentru validare
    const selectedMovie = currentSearchResults.find(movie => movie.Title === movieTitle);
    
    // Determinam care input trebuie completat si salvam filmul selectat
    if (containerId === 'movie-search-results') {
        // Completam input-ul din dashboard
        document.getElementById('movie-title').value = movieTitle;
        // Salvam filmul selectat pentru validare
        selectedMovieDashboard = selectedMovie;
    } else if (containerId === 'movie-search-results-recommend') {
        // Completam input-ul pentru recomandare
        document.getElementById('recommend-movie-title').value = movieTitle;
        // Salvam filmul selectat pentru validare
        selectedMovieRecommend = selectedMovie;
    }
    
    // Ascundem dropdown-ul
    hideSearchResults();
    hideSearchResultsRecommend();
}

// Functie pentru afisarea dropdown-ului de rezultate (dashboard)
function showSearchResults() {
    const searchTerm = document.getElementById('movie-title').value;
    if (searchTerm && searchTerm.trim().length >= 2 && currentSearchResults.length > 0) {
        const resultsDiv = document.getElementById('movie-search-results');
        resultsDiv.classList.add('show');
    }
}

// Functie pentru ascunderea dropdown-ului de rezultate (dashboard)
function hideSearchResults() {
    // Folosim un mic delay pentru a permite click-ul pe item
    setTimeout(() => {
        const resultsDiv = document.getElementById('movie-search-results');
        if (resultsDiv) {
            resultsDiv.classList.remove('show');
        }
    }, 200);
}

// Functie pentru cautarea filmelor pentru recomandare (cu debounce)
function searchMoviesRecommend(searchTerm) {
    // Anulam timeout-ul anterior daca exista
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    // Daca campul este gol, ascundem rezultatele si resetam filmul selectat
    if (!searchTerm || searchTerm.trim().length < 2) {
        hideSearchResultsRecommend();
        selectedMovieRecommend = null; // Resetam filmul selectat cand se modifica input-ul
        return;
    }
    
    // Asteptam 300ms inainte de a face request-ul (debounce)
    searchTimeout = setTimeout(async () => {
        try {
            // Facem request catre endpoint-ul nostru de proxy pentru cautare
            const response = await fetch(`${MOVIE_SEARCH_URL}?s=${encodeURIComponent(searchTerm.trim())}`);
            const data = await response.json();
            
            // Verificam daca cautarea a reusit
            if (data.Response === 'True' && data.Search) {
                // Salvam rezultatele
                currentSearchResults = data.Search;
                // Afisam rezultatele in dropdown
                displaySearchResults(currentSearchResults, 'movie-search-results-recommend');
            } else {
                // Daca nu sunt rezultate, afisam mesaj
                const resultsDiv = document.getElementById('movie-search-results-recommend');
                resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
                resultsDiv.classList.add('show');
            }
        } catch (error) {
            // In caz de eroare, afisam mesaj
            const resultsDiv = document.getElementById('movie-search-results-recommend');
            resultsDiv.innerHTML = '<div class="movie-search-error">Error searching movies</div>';
            resultsDiv.classList.add('show');
        }
    }, 300);
}

// Functie pentru afisarea dropdown-ului de rezultate (recomandare)
function showSearchResultsRecommend() {
    const searchTerm = document.getElementById('recommend-movie-title').value;
    if (searchTerm && searchTerm.trim().length >= 2 && currentSearchResults.length > 0) {
        const resultsDiv = document.getElementById('movie-search-results-recommend');
        resultsDiv.classList.add('show');
    }
}

// Functie pentru ascunderea dropdown-ului de rezultate (recomandare)
function hideSearchResultsRecommend() {
    // Folosim un mic delay pentru a permite click-ul pe item
    setTimeout(() => {
        const resultsDiv = document.getElementById('movie-search-results-recommend');
        if (resultsDiv) {
            resultsDiv.classList.remove('show');
        }
    }, 200);
}

// Functie pentru adaugarea unui film nou
async function addMovie() {
    // Preluam titlul filmului din campul de input
    const title = document.getElementById('movie-title').value;
    
    // Verificam daca titlul nu este gol
    if (!title || !title.trim()) {
        showNotification('Please enter a movie title', 'error');
        return;
    }
    
    // Verificam daca filmul a fost selectat din lista de rezultate (validare)
    if (!selectedMovieDashboard) {
        showNotification('Please select a movie from the search results', 'error');
        return;
    }
    
    // Verificam daca titlul din input corespunde cu filmul selectat
    if (title.trim() !== selectedMovieDashboard.Title) {
        showNotification('Please select a movie from the search results', 'error');
        return;
    }
    
    // Ascundem rezultatele cautarii
    hideSearchResults();
    
    try {
        // Trimitem cererea de adaugare film la server
        const response = await fetch(`${API_URL}/movies`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({title: title.trim()})
        });
        
        // Verificam daca adaugarea a reusit
        if (response.status === 201) {
            // Golim campul de input
            document.getElementById('movie-title').value = '';
            
            // Resetam filmul selectat
            selectedMovieDashboard = null;
            
            // Afisam notificare de succes
            showNotification('Movie added successfully!', 'success');

            // Reincarcam lista de filme
            loadMovies();
        } else {
            showNotification('Error adding movie', 'error');
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
    // Mapam statusurile la texte mai scurte si clare pentru butoane
    const statusLabels = {
        'To Watch': 'Watch',
        'Watching': 'Watching',
        'Completed': 'Done'
    };
    
    let actionButtons = '';
    
    // Generam butoanele in functie de statusul curent
    if (currentStatus === 'To Watch') {
        // Pentru "To Watch": butoane pentru Watching, Completed si Delete
        actionButtons = `
            <button class="move-btn move-btn-watching" onclick="moveMovie(${movie.id}, 'Watching')" title="Move to Watching">
                <span class="btn-text">Watching</span>
            </button>
            <button class="move-btn move-btn-completed" onclick="moveMovie(${movie.id}, 'Completed')" title="Move to Completed">
                <span class="btn-text">Completed</span>
            </button>
            <button class="delete-btn" onclick="deleteMovie(${movie.id})" title="Delete movie">
                <span class="btn-icon">🗑</span>
                <span class="btn-text">Delete</span>
            </button>
        `;
    } else if (currentStatus === 'Watching') {
        // Pentru "Watching": butoane pentru Completed si Delete
        actionButtons = `
            <button class="move-btn move-btn-completed" onclick="moveMovie(${movie.id}, 'Completed')" title="Move to Completed">
                <span class="btn-text">Completed</span>
            </button>
            <button class="delete-btn" onclick="deleteMovie(${movie.id})" title="Delete movie">
                <span class="btn-icon">🗑</span>
                <span class="btn-text">Delete</span>
            </button>
        `;
    } else if (currentStatus === 'Completed') {
        // Pentru "Completed": dropdown pentru rating (1-10) si Delete
        const currentRating = movie.rating && movie.rating !== '-' ? movie.rating : '';
        actionButtons = `
            <div class="rating-container">
                <select class="rating-select" id="rating-${movie.id}" onchange="rateMovie(${movie.id}, this.value)" title="Rate this movie">
                    <option value="">Rate (1-10)</option>
                    ${[1,2,3,4,5,6,7,8,9,10].map(r => 
                        `<option value="${r}" ${currentRating == r ? 'selected' : ''}>${r}</option>`
                    ).join('')}
                </select>
            </div>
            <button class="delete-btn" onclick="deleteMovie(${movie.id})" title="Delete movie">
                <span class="btn-icon">🗑</span>
                <span class="btn-text">Delete</span>
            </button>
        `;
    }
    
    // Returnam HTML-ul pentru un film cu butoane in functie de status
    return `
        <div class="movie-item">
            <span class="movie-title-text">${movie.title}${currentStatus === 'Completed' && movie.rating && movie.rating !== '-' ? ` <span class="movie-rating-display">(${movie.rating}/10)</span>` : ''}</span>
            <div class="movie-actions">
                ${actionButtons}
            </div>
        </div>
    `;
}

// Functie pentru notarea unui film (rating 1-10)
async function rateMovie(id, rating) {
    // Verificam daca rating-ul este valid
    if (!rating || rating === '') {
        return; // Daca nu este selectat nimic, nu facem nimic
    }
    
    const ratingValue = parseInt(rating);
    
    // Verificam daca rating-ul este intre 1 si 10
    if (ratingValue < 1 || ratingValue > 10) {
        showNotification('Rating must be between 1 and 10', 'error');
        return;
    }
    
    try {
        // Trimitem cererea de notare film la server
        const response = await fetch(`${API_URL}/movies/${id}/rate`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({rating: ratingValue.toString()})
        });
        
        // Verificam daca notarea a reusit
        if (response.status === 200) {
            // Afisam notificare de succes pe site
            showNotification(`Movie rated ${ratingValue}/10!`, 'success');
            
            // Reincarcam lista de filme pentru a actualiza rating-ul afisat
            loadMovies();
        } else {
            // Preluam mesajul de eroare de la server si il afisam pe site
            const data = await response.json();
            showNotification(data.message || 'Error rating movie', 'error');
        }
    } catch (error) {
        // Afisam eroare pe site daca apare o problema
        showNotification('Connection error. Please try again.', 'error');
    }
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
            // Afisam notificare de succes pe site
            showNotification(`Movie moved to ${newStatus} successfully!`, 'success');
            
            // Reincarcam lista de filme
            loadMovies();
        } else {
            // Preluam mesajul de eroare de la server si il afisam pe site
            const data = await response.json();
            showNotification(data.message || 'Error moving movie', 'error');
        }
    } catch (error) {
        // Afisam eroare pe site daca apare o problema
        showNotification('Connection error. Please try again.', 'error');
    }
}

// Functie pentru stergerea unui film
async function deleteMovie(id) {
    // Afisam confirmare personalizata pe site
    showConfirm('Are you sure you want to delete this movie?', async function() {
        try {
            // Trimitem cererea de stergere film la server
            const response = await fetch(`${API_URL}/movies/${id}`, {
                method: 'DELETE',
                headers: {'Authorization': token}
            });
            
            // Verificam daca stergerea a reusit
            if (response.status === 200) {
                // Afisam notificare de succes pe site
                showNotification('Movie deleted successfully!', 'success');
                
                // Reincarcam lista de filme
                loadMovies();
            } else {
                // Preluam mesajul de eroare de la server si il afisam pe site
                const data = await response.json();
                showNotification(data.message || 'Error deleting movie', 'error');
            }
        } catch (error) {
            // Afisam eroare pe site daca apare o problema
            showNotification('Connection error. Please try again.', 'error');
        }
    });
}