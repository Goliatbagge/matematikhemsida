// Smooth scrolling för länkar
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Stäng dropdown när användaren klickar utanför
window.addEventListener('click', function(e) {
    if (!e.target.matches('.dropbtn')) {
        const dropdowns = document.querySelectorAll('.dropdown-content');
        dropdowns.forEach(dropdown => {
            if (dropdown.style.display === 'block') {
                dropdown.style.display = 'none';
            }
        });
    }
});

// Highlight aktiv sektion vid scrollning
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('.content-section');
    const navLinks = document.querySelectorAll('.dropdown-content a');

    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= (sectionTop - 150)) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) {
            link.classList.add('active');
        }
    });
});

// Lägg till active class styling
const style = document.createElement('style');
style.textContent = `
    .dropdown-content a.active {
        background: #667eea;
        color: white !important;
        font-weight: bold;
    }
`;
document.head.appendChild(style);

// Console log för att visa att scriptet är laddat
console.log('Matematik 3c hemsida laddad!');
