document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.container');
    const dropdownContent = document.querySelector('.dropdown-content');

    container.addEventListener('mouseenter', function () {
        dropdownContent.style.display = 'block';
    });

    container.addEventListener('mouseleave', function () {
        dropdownContent.style.display = 'none';
    });
});