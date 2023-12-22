/* 
# ------------------------ #
| Pagination - List Movies |
# ------------------------ #
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
    let links = document.getElementsByClassName('linkMovie');

    // Function to update active link
    function updateActiveLinkMovie() {
        Array.from(links).forEach(link => link.classList.remove('active'));
        links[currentValue - 1].classList.add('active');
    }

    function activeLinkMovie(event) {
        let page = parseInt(event.currentTarget.getAttribute('data-value'));

        // Check if the page number is valid and exists
        if (!page || page < 1 || page > links.length) {
            console.error('Invalid page number:', page);
            return; // Do nothing if the page number is invalid
        }

        currentValue = page;
        updateActiveLinkMovie();
        window.location.href = '/movies/P' + page; // Redirect to the new page
    }

    // Attach event listeners to pagination links
    Array.from(links).forEach(link => {
        link.addEventListener('click', activeLinkMovie);
    });

    function backBtnMovie() {
        if (currentValue > 1) {
            currentValue--;
            updateActiveLinkMovie();
            window.location.href = '/movies/P' + currentValue; // Redirect to the new page
        }
    }
    
    function nextBtnMovie() {
        if (currentValue < links.length) {
            currentValue++;
            updateActiveLinkMovie();
            window.location.href = '/movies/P' + currentValue; // Redirect to the new page
        }
    }

    // Attach event listeners to buttons
    document.getElementById('btn1Movie').addEventListener('click', backBtnMovie);
    document.getElementById('btn2Movie').addEventListener('click', nextBtnMovie);

    // Update the active link initially
    updateActiveLinkMovie();
});

/* 
# ------------------------ #
| Pagination - List Actors |
# ------------------------ #
*/

document.addEventListener('DOMContentLoaded', (event) => {
    // Function to determine the initial page based on the URL
    function determineInitialPage() {
        let currentPath = window.location.pathname;
        let match = currentPath.match(/\/actors\/P(\d+)/);
        return match ? parseInt(match[1], 10) : 1;
    }

    // Global variables
    let currentValue = determineInitialPage();
    let links = document.getElementsByClassName('linkActor');

    // Function to update active link
    function updateActiveLinkActor() {
        Array.from(links).forEach(link => link.classList.remove('active'));
        links[currentValue - 1].classList.add('active');
    }

    function activeLinkActor(event) {
        let page = parseInt(event.currentTarget.getAttribute('data-value'));

        // Check if the page number is valid and exists
        if (!page || page < 1 || page > links.length) {
            console.error('Invalid page number:', page);
            return; // Do nothing if the page number is invalid
        }

        currentValue = page;
        updateActiveLinkActor();
        window.location.href = '/actors/P' + page; // Redirect to the new page
    }

    // Attach event listeners to pagination links
    Array.from(links).forEach(link => {
        link.addEventListener('click', activeLinkActor);
    });

    function backBtnActor() {
        if (currentValue > 1) {
            currentValue--;
            updateActiveLinkActor();
            window.location.href = '/actors/P' + currentValue; // Redirect to the new page
        }
    }
    
    function nextBtnActor() {
        if (currentValue < links.length) {
            currentValue++;
            updateActiveLinkActor();
            window.location.href = '/actors/P' + currentValue; // Redirect to the new page
        }
    }

    // Attach event listeners to buttons
    document.getElementById('btn1Actor').addEventListener('click', backBtnActor);
    document.getElementById('btn2Actor').addEventListener('click', nextBtnActor);

    // Update the active link initially
    updateActiveLinkActor();
});

/* 
# ------------------------------ #
| Search Bar - Performing Search |
# ------------------------------ #
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

/* 
# ---------------------------- #
| Search Bar - Styling Effects |
# ---------------------------- #
*/

const searchBar = document.querySelector('.navigation .search-bar');
let typingTimer;
const doneTypingInterval = 500; // 0.5 seconds

// Expand the search bar on focus
document.getElementById('search-input').addEventListener('focus', () => {
    searchBar.style.width = '400px';
});

// Contract the search bar on blur and remove inline style if not hovering
document.getElementById('search-input').addEventListener('blur', () => {
    if (!searchBar.matches(':hover')) {
        searchBar.style.width = '30px';
    }
    setTimeout(() => { // Delay to check hover state after blur
        if (!searchBar.matches(':hover')) {
            searchBar.style.removeProperty('width');
        }
    }, 100);
});

// Handling typing
document.getElementById('search-input').addEventListener('keyup', () => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

document.getElementById('search-input').addEventListener('keydown', () => {
    clearTimeout(typingTimer);
});

function doneTyping() {
    if (!searchBar.matches(':hover')) {
        searchBar.style.width = '30px';
    }
}

// Remove inline style on mouseleave to enable hover effect in CSS
searchBar.addEventListener('mouseleave', () => {
    if (!searchBar.querySelector('input').matches(':focus')) {
        searchBar.style.removeProperty('width');
    }
});
