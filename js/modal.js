document.addEventListener('DOMContentLoaded', () => {
    const modalElement = document.getElementById('myModal');
    if (!modalElement) return;

    // Initialize Bootstrap 5 Modal
    const myModal = new bootstrap.Modal(modalElement, {
        keyboard: false
    });

    // Check cookies
    function checkCookie() {
        let cookie = document.cookie;
        if (cookie.includes("display=false")) {
            // Do not show
        } else {
            myModal.show();
        }
    }
    checkCookie();

    // Handle "Don't show again" checkbox
    const checkbox = document.querySelector("input.dont");
    if (checkbox) {
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                document.cookie = "display=false; path=/; max-age=" + (60 * 60 * 24 * 365); // 1 year
            } else {
                document.cookie = "display=true; path=/; max-age=" + (60 * 60 * 24 * 365);
            }
        });
    }

    // Centering is handled by Bootstrap 5 CSS (modal-dialog-centered class)
    // We will add this class in the HTML migration step.
});
