/**
 * Home page search redirection handler
 *
 * This script handles the "Find or Register Dataset" button behavior on the frontpage.
 * When clicked:
 * - If the search input contains a URL (starts with https://),
 *   it submits the search form to redirect to the search page
 * - Otherwise, it navigates to the dataset registration page
 */

(function () {
  function initializeFrontpageSearch() {
    const registerButton = document.getElementById("frontpage-register-button");
    const searchInput = document.getElementById("frontpage-search-input");
    const searchForm = document.getElementById("frontpage-search-form");

    if (!registerButton || !searchInput || !searchForm) {
      return;
    }

    /**
     * Handle the action when the register button is activated
     */
    function handleAction() {
      const query = searchInput.value.trim();

      if (query.startsWith("https://")) {
        searchForm.submit();
      } else {
        const registerUrl = registerButton.getAttribute("data-register-url");
        if (registerUrl) {
          window.location.href = registerUrl;
        }
      }
    }

    registerButton.addEventListener("click", handleAction);
    registerButton.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        handleAction();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeFrontpageSearch);
  } else {
    initializeFrontpageSearch();
  }
})();
