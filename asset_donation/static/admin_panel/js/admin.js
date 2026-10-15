document.addEventListener('DOMContentLoaded', () => {
    // Accordion Toggle for Category & Nav Groups
    const groupHeaders = document.querySelectorAll('.nav-group-header');
    groupHeaders.forEach(header => {
        header.addEventListener('click', (e) => {
            e.preventDefault();
            const group = header.closest('.nav-group');
            if (group) {
                group.classList.toggle('open');
            }
        });
    });

    // Highlight current active link
    const currentUrl = window.location.pathname + window.location.search;
    const currentPath = window.location.pathname;

    const links = document.querySelectorAll('.sidebar nav a');
    let matched = false;

    // Check exact match first
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentUrl) {
            link.classList.add('active');
            const parentGroup = link.closest('.nav-group');
            if (parentGroup) {
                parentGroup.classList.add('open');
            }
            matched = true;
        }
    });

    // Fallback to path match if query param is not matched
    if (!matched) {
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.split('?')[0] === currentPath && !link.classList.contains('tree-item')) {
                link.classList.add('active');
                const parentGroup = link.closest('.nav-group');
                if (parentGroup) {
                    parentGroup.classList.add('open');
                }
            }
        });
    }
});

