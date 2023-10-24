document.addEventListener('mousemove', e => {
    const menuSection = document.getElementById('home');

    // Проверяем, происходит ли событие внутри секции меню
    if (menuSection && e.target.closest('#home')) {
        Object.assign(document.documentElement, {
            style: `
            --move-x: ${(e.clientX - window.innerWidth / 2) * -0.005}deg;
            --move-y: ${(e.clientY - window.innerHeight / 2) * 0.01}deg;
            `
        });
    } else {
        Object.assign(document.documentElement, {
            style: `
            --move-x: 0deg;
            --move-y: 0deg;
            `
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const userMenu = document.querySelector('.user-menu');
    const submenu = document.querySelector('.submenu');

    if (userNickname) {
        userNickname.addEventListener('mouseenter', () => {
            userMenu.style.display = 'block';
        });
    }

    if (userNickname) {
        userNickname.addEventListener('mouseleave', () => {
            userMenu.style.display = 'none';
        });
    }

});

const smoothLinks = document.querySelectorAll('a[href^="#"]');
for (let smoothLink of smoothLinks) {
    smoothLink.addEventListener('click', function (e) {
        e.preventDefault();
        const id = smoothLink.getAttribute('href');

        document.querySelector(id).scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
};
