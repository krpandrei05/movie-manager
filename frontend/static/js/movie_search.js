/**
 * JavaScript minim pentru autocomplete căutare filme
 * Folosește TVMaze API prin backend-ul Python
 */

// URL pentru căutare filme (backend API)
const MOVIE_SEARCH_URL = 'http://localhost:5000/api/search-movies';

// Variabile pentru debounce la căutare
let searchTimeout = null;
let currentSearchResults = [];

// Variabile pentru a salva filmele selectate (pentru validare)
let selectedMovieDashboard = null; // Filmul selectat din dashboard
let selectedMovieRecommend = null; // Filmul selectat pentru recomandare

/**
 * Caută filme pe TVMaze API (cu debounce)
 * @param {string} searchTerm - Termenul de căutare
 */
function searchMovies(searchTerm) {
    // Anulăm timeout-ul anterior dacă există
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    // Dacă câmpul este gol, ascundem rezultatele și resetăm filmul selectat
    if (!searchTerm || searchTerm.trim().length < 2) {
        hideSearchResults();
        selectedMovieDashboard = null;
        return;
    }
    
    // Așteptăm 300ms înainte de a face request-ul (debounce)
    searchTimeout = setTimeout(async () => {
        try {
            // Facem request către endpoint-ul nostru de proxy pentru căutare
            const response = await fetch(`${MOVIE_SEARCH_URL}?s=${encodeURIComponent(searchTerm.trim())}`);
            const data = await response.json();
            
            // Verificăm dacă căutarea a reușit
            if (data.Response === 'True' && data.Search) {
                // Salvăm rezultatele
                currentSearchResults = data.Search;
                // Afișăm rezultatele în dropdown
                displaySearchResults(currentSearchResults, 'movie-search-results');
            } else {
                // Dacă nu sunt rezultate, afișăm mesaj
                const resultsDiv = document.getElementById('movie-search-results');
                if (resultsDiv) {
                    resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
                    resultsDiv.classList.add('show');
                }
            }
        } catch (error) {
            // În caz de eroare, afișăm mesaj
            const resultsDiv = document.getElementById('movie-search-results');
            if (resultsDiv) {
                resultsDiv.innerHTML = '<div class="movie-search-error">Error searching movies</div>';
                resultsDiv.classList.add('show');
            }
        }
    }, 300);
}

/**
 * Caută filme pentru recomandare (cu debounce)
 * @param {string} searchTerm - Termenul de căutare
 */
function searchMoviesRecommend(searchTerm) {
    // Anulăm timeout-ul anterior dacă există
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    // Dacă câmpul este gol, ascundem rezultatele și resetăm filmul selectat
    if (!searchTerm || searchTerm.trim().length < 2) {
        hideSearchResultsRecommend();
        selectedMovieRecommend = null;
        return;
    }
    
    // Așteptăm 300ms înainte de a face request-ul (debounce)
    searchTimeout = setTimeout(async () => {
        try {
            // Facem request către endpoint-ul nostru de proxy pentru căutare
            const response = await fetch(`${MOVIE_SEARCH_URL}?s=${encodeURIComponent(searchTerm.trim())}`);
            const data = await response.json();
            
            // Verificăm dacă căutarea a reușit
            if (data.Response === 'True' && data.Search) {
                // Salvăm rezultatele
                currentSearchResults = data.Search;
                // Afișăm rezultatele în dropdown
                displaySearchResults(currentSearchResults, 'movie-search-results-recommend');
            } else {
                // Dacă nu sunt rezultate, afișăm mesaj
                const resultsDiv = document.getElementById('movie-search-results-recommend');
                if (resultsDiv) {
                    resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
                    resultsDiv.classList.add('show');
                }
            }
        } catch (error) {
            // În caz de eroare, afișăm mesaj
            const resultsDiv = document.getElementById('movie-search-results-recommend');
            if (resultsDiv) {
                resultsDiv.innerHTML = '<div class="movie-search-error">Error searching movies</div>';
                resultsDiv.classList.add('show');
            }
        }
    }, 300);
}

/**
 * Afișează rezultatele căutării
 * @param {Array} results - Array cu rezultatele căutării
 * @param {string} containerId - ID-ul containerului pentru rezultate
 */
function displaySearchResults(results, containerId) {
    const resultsDiv = document.getElementById(containerId);
    
    if (!resultsDiv) {
        return;
    }
    
    if (!results || results.length === 0) {
        resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
        resultsDiv.classList.add('show');
        return;
    }
    
    // Cream HTML-ul pentru fiecare rezultat
    resultsDiv.innerHTML = results.map((movie, index) => {
        // Escapăm caracterele speciale pentru siguranță (pentru onclick)
        const titleEscaped = movie.Title.replace(/'/g, "\\'").replace(/"/g, '&quot;');
        const titleHtml = movie.Title.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const yearHtml = (movie.Year || 'N/A').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const typeHtml = (movie.Type || 'show').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return `
            <div class="movie-search-item" onclick="selectMovie('${titleEscaped}', '${containerId}')">
                <div class="movie-title">${titleHtml}</div>
                <div class="movie-year">${yearHtml}</div>
                <div class="movie-type">${typeHtml}</div>
            </div>
        `;
    }).join('');
    
    // Afișăm dropdown-ul
    resultsDiv.classList.add('show');
}

/**
 * Selectează un film din lista de rezultate
 * @param {string} movieTitle - Titlul filmului selectat
 * @param {string} containerId - ID-ul containerului
 */
function selectMovie(movieTitle, containerId) {
    // Căutăm filmul selectat în rezultatele curente pentru validare
    const selectedMovie = currentSearchResults.find(movie => movie.Title === movieTitle);
    
    // Determinăm care input trebuie completat și salvăm filmul selectat
    if (containerId === 'movie-search-results') {
        // Completăm input-ul din dashboard
        const input = document.getElementById('movie-title');
        if (input) {
            input.value = movieTitle;
            selectedMovieDashboard = selectedMovie;
        }
    } else if (containerId === 'movie-search-results-recommend') {
        // Completăm input-ul pentru recomandare
        const input = document.getElementById('recommend-movie-title');
        if (input) {
            input.value = movieTitle;
            selectedMovieRecommend = selectedMovie;
        }
    }
    
    // Ascundem dropdown-ul
    hideSearchResults();
    hideSearchResultsRecommend();
}

/**
 * Afișează dropdown-ul de rezultate (dashboard)
 */
function showSearchResults() {
    const input = document.getElementById('movie-title');
    if (input) {
        const searchTerm = input.value;
        if (searchTerm && searchTerm.trim().length >= 2 && currentSearchResults.length > 0) {
            const resultsDiv = document.getElementById('movie-search-results');
            if (resultsDiv) {
                resultsDiv.classList.add('show');
            }
        }
    }
}

/**
 * Ascunde dropdown-ul de rezultate (dashboard)
 */
function hideSearchResults() {
    // Folosim un mic delay pentru a permite click-ul pe item
    setTimeout(() => {
        const resultsDiv = document.getElementById('movie-search-results');
        if (resultsDiv) {
            resultsDiv.classList.remove('show');
        }
    }, 200);
}

/**
 * Afișează dropdown-ul de rezultate (recomandare)
 */
function showSearchResultsRecommend() {
    const input = document.getElementById('recommend-movie-title');
    if (input) {
        const searchTerm = input.value;
        if (searchTerm && searchTerm.trim().length >= 2 && currentSearchResults.length > 0) {
            const resultsDiv = document.getElementById('movie-search-results-recommend');
            if (resultsDiv) {
                resultsDiv.classList.add('show');
            }
        }
    }
}

/**
 * Ascunde dropdown-ul de rezultate (recomandare)
 */
function hideSearchResultsRecommend() {
    // Folosim un mic delay pentru a permite click-ul pe item
    setTimeout(() => {
        const resultsDiv = document.getElementById('movie-search-results-recommend');
        if (resultsDiv) {
            resultsDiv.classList.remove('show');
        }
    }, 200);
}

