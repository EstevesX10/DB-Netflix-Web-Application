const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', ()=> {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', ()=> {
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', ()=> {
    wrapper.classList.remove('active-popup');
});

/* ------------------------------------------------ */

// Search 

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