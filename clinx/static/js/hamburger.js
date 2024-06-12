document.querySelector('.hamburger-menu').addEventListener('click', function() {
    document.querySelector('.mobile-menu').classList.toggle('active');
    console.log('Hamburger menu clicked');
  });

  // Function to close mobile menu when screen size is large enough
function closeMobileMenuOnResize() {
  const menuToggle = document.querySelector('.menu-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');

  // Listen for window resize event
  window.addEventListener('resize', function() {
    // Check if screen size is larger than specified width
    if (window.innerWidth > 768) { // Adjust 768 as needed
      // Remove 'active' class from mobile menu to hide it
      mobileMenu.classList.remove('active');
      // Uncheck the menu toggle checkbox
      menuToggle.checked = false;
    }
  });
}


// Call the function to close mobile menu on window resize
closeMobileMenuOnResize();