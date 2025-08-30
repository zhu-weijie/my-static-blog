(function() {
    function displaySearchResults(results, store) {
        const searchResults = document.getElementById('results-container');
        if (results.length) {
            let resultList = '';
            for (const n in results) {
                const item = store[results[n].ref];
                resultList += '<li><a href="' + item.url + '">' + item.title + '</a></li>';
            }
            searchResults.innerHTML = resultList;
        } else {
            searchResults.innerHTML = '<li>No results found.</li>';
        }
    }

    const searchInput = document.getElementById('search-input');

    // Fetch the search index and initialize Lunr
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
                
                data.forEach(function (doc) {
                    this.add(doc);
                }, this);
            });
        });

    searchInput.addEventListener('keyup', function () {
        const query = this.value;
        if (query.length < 3) {
            return;
        }
        const results = idx.search(query);
        displaySearchResults(results, postStore);
    });
})();
