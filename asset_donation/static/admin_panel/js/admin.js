document.addEventListener('DOMContentLoaded', () => {
    // Highlight current active link
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.sidebar nav a');
    links.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
