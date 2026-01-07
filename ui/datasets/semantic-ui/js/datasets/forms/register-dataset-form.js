(function () {
    function attachFormSubmitSpinner() {
        const form = document.getElementById('register-dataset-form');
        const submitButton = form?.querySelector('button[type="submit"]');
        
        if (!form || !submitButton) return;
        
        submitButton.classList.remove("loading", "disabled");

        form.addEventListener("submit", () => {
            submitButton.classList.add("loading", "disabled");
        });
    };

    window.addEventListener("pageshow", (e) => {
        if (e.persisted) {
            // Page was fetched from BFCache (navigated back to it) 
            // Reset the form state as if it was loaded for the first time
            attachFormSubmitSpinner()
        }
    });

    // Attach on DOM ready
    document.addEventListener("DOMContentLoaded", () => {
        attachFormSubmitSpinner();
    });
})();
