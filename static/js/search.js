(function() {
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

    function displaySearchResults(results, store, query) {
        const searchResults = document.getElementById('results-container');
        if (results.length) {
            let resultList = '';
            const highlightRegex = new RegExp(`(${query})`, 'gi');

            for (const result of results) {
                const item = store.find(doc => doc.url === result.ref);
                if (item) {
                    let snippet = '';
                    const matchMetadata = result.matchData.metadata;
                    for (const term in matchMetadata) {
                        if (matchMetadata[term].content) {
                            const position = matchMetadata[term].content.position[0][0];
                            const snippetStart = Math.max(position - 50, 0);
                            const snippetEnd = Math.min(position + 100, item.content.length);
                            snippet = '...' + item.content.substring(snippetStart, snippetEnd) + '...';
                            break;
                        }
                    }
                    
                    const highlightedTitle = item.title.replace(highlightRegex, '<mark>$1</mark>');
                    const highlightedSnippet = snippet.replace(highlightRegex, '<mark>$1</mark>');

                    resultList += `
                        <li>
                            <a href="${item.url}">${highlightedTitle}</a>
                            <p>${highlightedSnippet}</p>
                        </li>`;
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
                this.metadataWhitelist = ['position'];
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
            displaySearchResults(results, postStore, query);
        } catch (error) {
            console.error("Search error:", error);
        }
    }

    searchInput.addEventListener('keyup', debounce(performSearch, 300));

})();
