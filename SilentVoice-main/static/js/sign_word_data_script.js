const path = window.location.pathname;
const name = path.split("/").pop();
console.log("Name from URL:", name);
 
fetch('/api/signs')
.then(response => response.json())
.then(data => {
    const image_box = document.querySelector('.image_box')
    const image = document.querySelector('.image')
    const description_text = document.querySelector('.txt');
    data.forEach(word => {
        if ( word.name === name){
            description_text.textContent = `${word.description}`;
            image.src= `/static/images/${word.image}.png`;
        }
        image_box.appendChild(image)
    }) 
})
.catch(error => console.error('Error fetching data:', error));