const dictionary = document.getElementById("two");
const contact = document.getElementById("three");
const blur_screen = document.getElementById('blur_screen');
const footer_base = document.getElementById('footer_base');
const dictionary_box = document.getElementById('dictionary_box');
const contact_box = document.getElementById('contact_box');
const close = document.getElementById('close_logo');

function hideAllBoxes() {
    dictionary_box.style.display = "none";
    contact_box.style.display = "none";
}

function openFooter() {
    blur_screen.classList.add('active');
    footer_base.classList.add('active');
}

function closeFooter() {
    blur_screen.classList.remove('active');
    footer_base.classList.remove('active');
    hideAllBoxes();
}

dictionary.addEventListener('click', () => {
    hideAllBoxes();
    openFooter();
    dictionary_box.style.display = "block";
});

contact.addEventListener('click', () => {
    hideAllBoxes();
    openFooter();
    contact_box.style.display = "block";
});

close.addEventListener('click', () => {
    closeFooter();
});
