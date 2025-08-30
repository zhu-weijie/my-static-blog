(function() {
    // This function delays the execution of a function until after a certain time has passed
    // without that function being called again.
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function displaySearchResults(results, store) {
        const searchResults = document.getElementById('results-container');
        if (results.length) {
            let resultList = '';
            for (const result of results) {
                const item = store.find(doc => doc.url === result.ref);
                if (item) {
                    resultList += `<li><a href="${item.url}">${item.title}</a></li>`;
                }
            }
            searchResults.innerHTML = resultList;
        } else {
            searchResults.innerHTML = '<li>No results found.</li>';
        }
    }

    const searchInput = document.getElementById('search-input');
    let idx;
    let postStore;

    fetch('/search-index.json')
        .then(response => response.json())
        .then(data => {
            postStore = data;
            idx = lunr(function () {
                this.ref('url');
                this.field('title', { boost: 10 });
                this.field('content');
                data.forEach(doc => this.add(doc));
            });
            searchInput.disabled = false;
            searchInput.placeholder = "Enter search term...";
            searchInput.focus();
        })
        .catch(error => {
            console.error("Failed to load search index:", error);
            searchInput.placeholder = "Search is unavailable.";
        });

    function performSearch() {
        if (!idx) return;

        const query = searchInput.value;
        const resultsContainer = document.getElementById('results-container');

        if (query.length < 3) {
            resultsContainer.innerHTML = '';
            return;
        }
        
        try {
            const results = idx.search(query);
            displaySearchResults(results, postStore);
        } catch (error) {
            console.error("Search error:", error);
        }
    }

    // We wait 300ms after the user stops typing before searching.
    searchInput.addEventListener('keyup', debounce(performSearch, 300));

})();
