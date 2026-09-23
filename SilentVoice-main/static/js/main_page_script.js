document.addEventListener('DOMContentLoaded', () => {
    // Authentic Sign Language gesture data using clean transparent character assets
    const islSignsData = [
        {
            name: "Hello",
            desc: "In Indian Sign Language (ISL), raise your open hand beside your head, palm facing forward, and wave gently to greet someone warmly.",
            difficulty: "Beginner",
            image: "../static/images/isl_hello_character.png"
        },
        {
            name: "I Love You",
            desc: "Extend your thumb, index finger, and pinky finger while folding your middle two fingers down to express 'I Love You'.",
            difficulty: "Beginner",
            image: "../static/images/isl_love_character.png"
        },
        {
            name: "Thank You",
            desc: "In Indian Sign Language (ISL), place your fingertips at your chin or forehead and move your flat hand forward toward the person you are thanking.",
            difficulty: "Beginner",
            image: "../static/images/isl_thankyou_character.png"
        },
        {
            name: "Please",
            desc: "In Indian Sign Language (ISL), place your flat palm gently over your heart/chest and move your hand in a soft circular motion.",
            difficulty: "Intermediate",
            image: "../static/images/image_three.png"
        }
    ];

    let currentSignIndex = 0;

    const signNameEl = document.getElementById('showcase-sign-name');
    const signDescEl = document.getElementById('showcase-sign-desc');
    const characterImgEl = document.getElementById('isl-character-img');
    const signTagEl = document.getElementById('showcase-tag');
    const detectedTextEl = document.getElementById('detected-text');

    const btnPrev = document.getElementById('btn-prev-sign');
    const btnNext = document.getElementById('btn-next-sign');

    function updateShowcase(index) {
        const sign = islSignsData[index];
        if (!sign) return;

        if (signNameEl) signNameEl.innerText = sign.name;
        if (signDescEl) signDescEl.innerText = sign.desc;
        if (characterImgEl) characterImgEl.src = sign.image;
        if (signTagEl) signTagEl.innerText = `ISL Gesture: ${sign.name.toUpperCase()}`;
        if (detectedTextEl) {
            detectedTextEl.innerText = `${sign.name.toUpperCase()} (ISL)`;
        }
    }

    // Initialize default sign (Hello)
    updateShowcase(0);

    if (btnPrev && btnNext) {
        btnPrev.addEventListener('click', () => {
            currentSignIndex = (currentSignIndex - 1 + islSignsData.length) % islSignsData.length;
            updateShowcase(currentSignIndex);
        });

        btnNext.addEventListener('click', () => {
            currentSignIndex = (currentSignIndex + 1) % islSignsData.length;
            updateShowcase(currentSignIndex);
        });
    }

    // Hero Vocab Chips interaction
    const chips = document.querySelectorAll('.vocab-chips .chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.remove('chip-active'));
            chip.classList.add('chip-active');
            
            const signText = chip.getAttribute('data-sign');

            // Find matching ISL sign
            const foundIndex = islSignsData.findIndex(s => s.name.toUpperCase() === signText);
            if (foundIndex !== -1) {
                currentSignIndex = foundIndex;
                updateShowcase(currentSignIndex);
            }
        });
    });
});
