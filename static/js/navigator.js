// static/js/navigator.js

document.addEventListener('DOMContentLoaded', function () {
  // 🍔 Toggle mobile nav
  const mobileToggle = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }

  // 👤 Toggle user dropdown
  const userAvatar = document.querySelector('.user-avatar');
  const dropdown = document.querySelector('.user-dropdown-content');

  if (userAvatar && dropdown) {
    userAvatar.addEventListener('click', (e) => {
      e.stopPropagation(); // Prevent bubbling up to document click
      dropdown.classList.toggle('hidden');
    });

    // 🧼 Hide dropdown when clicking outside
    document.addEventListener('click', function (e) {
      if (!dropdown.classList.contains('hidden') && !dropdown.contains(e.target) && !userAvatar.contains(e.target)) {
        dropdown.classList.add('hidden');
      }
    });
  }
});
