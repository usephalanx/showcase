document.addEventListener('DOMContentLoaded', function initApp() {
    document.body.classList.add('loaded');
    console.log('Yellow World app initialized');
});

function getGreeting() {
    return 'Yellow World';
}
