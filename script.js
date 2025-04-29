document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll(".anim-appear");
    elements.forEach((el, index) => {
        el.style.opacity = "0";
        el.style.transform = "translateY(20px)";
        el.dataset.delay = index * 300; // Retraso progresivo entre elementos
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.transition = "opacity 0.3s ease, transform 0.3s ease";
                    entry.target.style.opacity = "1";
                    entry.target.style.transform = "translateY(0)";
                }, entry.target.dataset.delay);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    elements.forEach((el) => observer.observe(el));
});

const elements = document.querySelectorAll(".logo-appear");
elements.forEach((el, index) => {
    el.style.opacity = "0";
    el.style.transform = "translateX(-50px)";
    el.dataset.delay = index * 150; // Retraso progresivo entre elementos
});

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.transition = "opacity 0.3s ease, transform 0.3s ease";
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
            }, entry.target.dataset.delay);
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.2 });

elements.forEach((el) => observer.observe(el));

document.addEventListener("DOMContentLoaded", () => {
    const logos = document.querySelectorAll(".logos img");
    let counter = 0;

    function showLogo() {
        if (counter < logos.length) {
            logos[counter].classList.add("aparece");
            counter++;
            setTimeout(showLogo, 200); // Retraso para mostrar uno a uno
        }
    }

    showLogo();
});