document.addEventListener('DOMContentLoaded', () => {
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('a[rel=citation]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        const popover = new bootstrap.Popover(popoverTriggerEl, {
            placement: 'top'
        });

        popoverTriggerEl.addEventListener('click', function (e) {
            e.preventDefault();
            setTimeout(() => {
                popover.hide();
            }, 4000);
        });

        return popover;
    });
});
