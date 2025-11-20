let questions = [];
let currentIndex = 0;
let score = 0;

const questionImg = document.querySelector('.question_image');
const options = document.querySelectorAll('.option');
const scoreEl = document.querySelector('.correct_score');
const totalEl = document.querySelector('.total_score');
const nextBtn = document.querySelector('.next');
const prevBtn = document.querySelector('.previous');

fetch('/api/quiz')
  .then(res => res.json())
  .then(data => {
    questions = data;
    totalEl.textContent = questions.length;
    loadQuestion();
  })
  .catch(err => console.error("Error fetching quiz data:", err));

function loadQuestion() {
  const q = questions[currentIndex];

  resetOptions();

  questionImg.src = `/static/images/${q.image_name}`;

  document.querySelector('.txt_one').textContent = q.option_1;
  document.querySelector('.txt_two').textContent = q.option_2;
  document.querySelector('.txt_three').textContent = q.option_3;
  document.querySelector('.txt_four').textContent = q.option_4;
}

options.forEach(opt => {
  opt.addEventListener('click', () => {
    const q = questions[currentIndex];
    const selectedText = opt.querySelector('p').textContent;

    options.forEach(o => o.style.pointerEvents = 'none');

    if (selectedText === q.correct_answer) {
      opt.style.backgroundColor = 'green';
      score++;
      scoreEl.textContent = score;
    } else {
      opt.style.backgroundColor = 'red';

      options.forEach(o => {
        const txt = o.querySelector('p').textContent;
        if (txt === q.correct_answer) {
          o.style.backgroundColor = 'green';
        }
      });
    }
  });
});


function resetOptions() {
  options.forEach(opt => {
    opt.style.backgroundColor = '';
    opt.style.pointerEvents = 'auto';
  });
}

nextBtn.addEventListener('click', () => {
  if (currentIndex < questions.length - 1) {
    currentIndex++;
    loadQuestion();
  }
});

prevBtn.addEventListener('click', () => {
  if (currentIndex > 0) {
    currentIndex--;
    loadQuestion();
  }
});
