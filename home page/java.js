document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const menuItems = document.getElementById('menu-items');

    menuToggle.addEventListener('click', () => {
        menuItems.classList.toggle('active');
    });
});
