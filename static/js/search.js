(function() {
    function displaySearchResults(results, store) {
        const searchResults = document.getElementById('results-container');
        if (results.length) {
            let resultList = '';
            // The ref from Lunr is the "url" we specified
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

    // Fetch the search index and initialize Lunr
    fetch('/search-index.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            postStore = data;
            idx = lunr(function () {
                this.ref('url');
                this.field('title', { boost: 10 });
                this.field('content');
                
                data.forEach(doc => {
                    this.add(doc);
                }, this);
            });

            // --- FIX: Enable the input now that the index is ready ---
            searchInput.disabled = false;
            searchInput.placeholder = "Enter search term...";
            searchInput.focus(); // Automatically focus the input for the user
        })
        .catch(error => {
            console.error("Failed to load search index:", error);
            searchInput.placeholder = "Search is unavailable.";
        });

    searchInput.addEventListener('keyup', function () {
        // Don't search if the index isn't ready yet
        if (!idx) {
            return;
        }

        const query = this.value;
        const resultsContainer = document.getElementById('results-container');

        // Clear results if the query is too short
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
    });
})();
