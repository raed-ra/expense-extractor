/**
 * Logout page functionality - prevent access to previously protected pages using the browser back button
 */

// Prevent access to previously protected pages using the browser back button
function preventBackNavigation() {
  window.history.pushState(null, "", window.location.href);
  window.onpopstate = function () {
    window.history.pushState(null, "", window.location.href);
  };
}

// Clear browser history cache
function clearBrowserHistoryCache() {
  if (
    window.performance &&
    window.performance.navigation.type ===
      window.performance.navigation.TYPE_BACK_FORWARD
  ) {
    redirectToLogin();
  }
}

// Redirect to login page
function redirectToLogin() {
  // Get login URL (passed from template)
  const loginUrl = document
    .getElementById("login-url")
    .getAttribute("data-url");
  window.location.href = loginUrl;
}

// Delayed redirect
function setupDelayedRedirect() {
  // Redirect to login page after 2 seconds
  setTimeout(redirectToLogin, 2000);
}

// Initialize all logout functionality
function initLogout() {
  preventBackNavigation();
  document.addEventListener("DOMContentLoaded", setupDelayedRedirect);
  window.onload = clearBrowserHistoryCache;
}

// Automatically initialize
initLogout();
