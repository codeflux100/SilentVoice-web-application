const input_bar = document.querySelector('.input_bar')
const search_button = document.querySelector('.search_button')

input_bar.addEventListener("keydown",async (e) => {
    if(e.key === "Enter"){
        search_function()
    }
})
search_button.addEventListener('click',() => {search_function()})

const search_function= () => {
    const input_bar_text = input_bar.value.trim()
    fetch('/api/signs')
    .then(response => response.json())
    .then(data => {
        const word_found = data.find(word => word.name.toLowerCase() === input_bar_text);
        if(word_found){
            window.location.href = `/sign_name/${word_found.name}`;
        }
        else{
            alert('Word Not Found !!');
        }
    })
    .catch(error => console.error('Error fetching data:', error));
}
