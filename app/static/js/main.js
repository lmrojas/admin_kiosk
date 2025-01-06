// Toggle sidebar on mobile
document.querySelector('.toggle-sidebar').addEventListener('click', function() {
    document.querySelector('.sidebar').classList.toggle('show');
});

// Show notifications
function showNotification(type, message) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.querySelector('.main-content').insertAdjacentElement('afterbegin', alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 5000);
} 