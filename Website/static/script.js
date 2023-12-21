/* 
# ---------- #
| Pagination |
# ---------- #
*/

document.addEventListener('DOMContentLoaded', (event) => {
    // Function to determine the initial page based on the URL
    function determineInitialPage() {
        let currentPath = window.location.pathname;
        let match = currentPath.match(/\/movies\/P(\d+)/);
        return match ? parseInt(match[1], 10) : 1;
    }

    // Global variables
    let currentValue = determineInitialPage();
    let links = document.getElementsByClassName('link');

    // Function to update active link
    function updateActiveLink() {
        Array.from(links).forEach(link => link.classList.remove('active'));
        links[currentValue - 1].classList.add('active');
    }

    function activeLink(event) {
        let page = parseInt(event.currentTarget.getAttribute('data-value'));

        // Check if the page number is valid and exists
        if (!page || page < 1 || page > links.length) {
            console.error('Invalid page number:', page);
            return; // Do nothing if the page number is invalid
        }

        currentValue = page;
        updateActiveLink();
        window.location.href = '/movies/P' + page; // Redirect to the new page
    }

    // Attach event listeners to pagination links
    Array.from(links).forEach(link => {
        link.addEventListener('click', activeLink);
    });

    function backBtn() {
        if (currentValue > 1) {
            currentValue--;
            updateActiveLink();
            window.location.href = '/movies/P' + currentValue; // Redirect to the new page
        }
    }
    
    function nextBtn() {
        if (currentValue < links.length) {
            currentValue++;
            updateActiveLink();
            window.location.href = '/movies/P' + currentValue; // Redirect to the new page
        }
    }

    // Attach event listeners to buttons
    document.getElementById('btn1').addEventListener('click', backBtn);
    document.getElementById('btn2').addEventListener('click', nextBtn);

    // Update the active link initially
    updateActiveLink();
});

/* 
# ------ #
| Search |
# ------ #
*/

function handleKeyPress(event) {
    // Check if the pressed key is Enter (key code 13)
    if (event.keyCode === 13) {
      // Prevent the default form submission
      event.preventDefault();
      // Call the performSearch function
      performSearch();
    }
}

function performSearch() {
    // Get the value entered in the search bar
    var searchTerm = document.getElementById('search-input').value;

    // Check if the search term is not empty
    if (searchTerm.trim() !== '') {
      // Construct the new URL based on the search term
      var newURL = '/search/' + encodeURIComponent(searchTerm);

      // Redirect to the new URL
      window.location.href = newURL;
    }
}