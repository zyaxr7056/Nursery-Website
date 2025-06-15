document.addEventListener('DOMContentLoaded', function() {
    // Hide overlay when Razorpay modal is closed
    window.addEventListener('popstate', function() {
        const overlay = document.querySelector('.payment-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    });
});
