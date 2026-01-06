(function () {
    function attachFormSubmitSpinner(formId, buttonId) {
        const form = document.getElementById('register-dataset-form');
        const submitButton = form?.querySelector('button[type="submit"]');

        if (!form || !submitButton) return;

        form.addEventListener("submit", () => {
            submitButton.classList.add("loading", "disabled");
        });
    };

    // Attach on DOM ready
    document.addEventListener("DOMContentLoaded", () => {
        attachFormSubmitSpinner("my-form", "submit-btn");
    });
})();
