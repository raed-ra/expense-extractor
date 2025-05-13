document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("sidebar-toggle");
    const sidebar = document.getElementById("sidebar-links");

    toggleBtn?.addEventListener("click", function () {
      sidebar?.classList.toggle("hidden");
    });
  });