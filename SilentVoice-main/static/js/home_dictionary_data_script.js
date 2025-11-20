    fetch('/api/signs')
    .then(response => response.json())
    .then(data => {
        const dictionary_box = document.querySelector('.dictionary_box')
        const sign = document.querySelector('.signs');
        dictionary_box.appendChild(sign);
        const dict_navigation = document.querySelector('.dictionary_navigation')
        data.forEach(word => {
            const word_link = document.createElement('a')
            word_link.classList.add('word_link')
            word_link.href = `#sign_starting-${word.id}`

            const search = document.createElement('div')
            search.classList.add('search')
            search.textContent = `${word.id}`

            const sign_starting = document.createElement('div');
            sign_starting.classList.add('sign_starting')
            sign_starting.textContent =`${word.id}`;
            sign_starting.id = `sign_starting-${word.id}`;

            const sign_word = document.createElement('div');
            sign_word.classList.add('sign_word')
            sign_word.textContent = `${word.name}`

            const link = document.createElement('a');
            link.classList.add("word_link")
            link.href = `/sign_name/${word.name}`;

            dict_navigation.appendChild(word_link)
            word_link.appendChild(search)
            link.appendChild(sign_word)
            sign_starting.appendChild(link)
            sign.appendChild(sign_starting)
        }) 
    })
    .catch(error => console.error('Error fetching data:', error));
