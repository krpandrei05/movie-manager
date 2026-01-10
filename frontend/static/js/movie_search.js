// url pentru cautare filme
const MOVIE_SEARCH_URL = 'http://localhost:5000/api/search-movies';

// variabile pentru debounce la cautare
let searchTimeout = null;
let currentSearchResults = [];

// variabile pentru a salva filmele selectate
let selectedMovieDashboard = null; // filmul selectat din dashboard
let selectedMovieRecommend = null; // filmul selectat pentru recomandare

// Cauta filme cu debounce
function searchMovies(searchTerm) {
    // anulam timeout-ul anterior daca exista
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    // daca campul este gol, ascundem rezultatele si resetam filmul selectat
    if (!searchTerm || searchTerm.trim().length < 2) {
        hideSearchResults();
        selectedMovieDashboard = null;
        return;
    }
    
    // asteptam 300ms inainte de a face request-ul
    searchTimeout = setTimeout(async () => {
        try {
            // facem request catre backend pentru cautare
            const response = await fetch(`${MOVIE_SEARCH_URL}?s=${encodeURIComponent(searchTerm.trim())}`);
            const data = await response.json();
            
            // verificam daca cautarea a reusit
            if (data.Response === 'True' && data.Search) {
                // salvam rezultatele
                currentSearchResults = data.Search;
                // afisam rezultatele in dropdown
                displaySearchResults(currentSearchResults, 'movie-search-results');
            } else {
                // daca nu sunt rezultate, afisam mesaj
                const resultsDiv = document.getElementById('movie-search-results');
                if (resultsDiv) {
                    resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
                    resultsDiv.classList.add('show');
                }
            }
        } catch (error) {
            // in caz de eroare, afisam mesaj
            const resultsDiv = document.getElementById('movie-search-results');
            if (resultsDiv) {
                resultsDiv.innerHTML = '<div class="movie-search-error">Error searching movies</div>';
                resultsDiv.classList.add('show');
            }
        }
    }, 300);
}

// Cauta filme pentru recomandare cu debounce
function searchMoviesRecommend(searchTerm) {
    // anulam timeout-ul anterior daca exista
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    // daca campul este gol, ascundem rezultatele si resetam filmul selectat
    if (!searchTerm || searchTerm.trim().length < 2) {
        hideSearchResultsRecommend();
        selectedMovieRecommend = null;
        return;
    }
    
    // asteptam 300ms inainte de a face request-ul
    searchTimeout = setTimeout(async () => {
        try {
            // facem request catre backend pentru cautare
            const response = await fetch(`${MOVIE_SEARCH_URL}?s=${encodeURIComponent(searchTerm.trim())}`);
            const data = await response.json();
            
            // verificam daca cautarea a reusit
            if (data.Response === 'True' && data.Search) {
                // salvam rezultatele
                currentSearchResults = data.Search;
                // afisam rezultatele in dropdown
                displaySearchResults(currentSearchResults, 'movie-search-results-recommend');
            } else {
                // daca nu sunt rezultate, afisam mesaj
                const resultsDiv = document.getElementById('movie-search-results-recommend');
                if (resultsDiv) {
                    resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
                    resultsDiv.classList.add('show');
                }
            }
        } catch (error) {
            // in caz de eroare, afisam mesaj
            const resultsDiv = document.getElementById('movie-search-results-recommend');
            if (resultsDiv) {
                resultsDiv.innerHTML = '<div class="movie-search-error">Error searching movies</div>';
                resultsDiv.classList.add('show');
            }
        }
    }, 300);
}

// Afiseaza rezultatele cautarii in dropdown
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
    
    // cream html-ul pentru fiecare rezultat
    resultsDiv.innerHTML = results.map((movie, index) => {
        // escapam caracterele speciale pentru siguranta
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
    
    // afisam dropdown-ul
    resultsDiv.classList.add('show');
}

// Selecteaza un film din lista si completeaza input-ul
function selectMovie(movieTitle, containerId) {
    // cautam filmul selectat in rezultatele curente
    const selectedMovie = currentSearchResults.find(movie => movie.Title === movieTitle);
    
    // determinam care input trebuie completat si salvam filmul selectat
    if (containerId === 'movie-search-results') {
        // completam input-ul din dashboard
        const input = document.getElementById('movie-title');
        if (input) {
            input.value = movieTitle;
            selectedMovieDashboard = selectedMovie;
            // setam campul hidden pentru validare
            const hiddenInput = document.getElementById('movie-validated');
            if (hiddenInput) {
                hiddenInput.value = '1';
            }
        }
    } else if (containerId === 'movie-search-results-recommend') {
        // completam input-ul pentru recomandare
        const input = document.getElementById('recommend-movie-title');
        if (input) {
            input.value = movieTitle;
            selectedMovieRecommend = selectedMovie;
            // setam campul hidden pentru validare
            const hiddenInput = document.getElementById('recommend-movie-validated');
            if (hiddenInput) {
                hiddenInput.value = '1';
            }
        }
    }
    
    // ascundem dropdown-ul
    hideSearchResults();
    hideSearchResultsRecommend();
}

// Afiseaza dropdown-ul de rezultate pentru dashboard
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

// Ascunde dropdown-ul de rezultate pentru dashboard
function hideSearchResults() {
    // folosim un mic delay pentru a permite click-ul pe item
    setTimeout(() => {
        const resultsDiv = document.getElementById('movie-search-results');
        if (resultsDiv) {
            resultsDiv.classList.remove('show');
        }
    }, 200);
}

// Afiseaza dropdown-ul de rezultate pentru recomandare
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

// Ascunde dropdown-ul de rezultate pentru recomandare
function hideSearchResultsRecommend() {
    // folosim un mic delay pentru a permite click-ul pe item
    setTimeout(() => {
        const resultsDiv = document.getElementById('movie-search-results-recommend');
        if (resultsDiv) {
            resultsDiv.classList.remove('show');
        }
    }, 200);
}