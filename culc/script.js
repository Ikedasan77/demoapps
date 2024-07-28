const quizData = [
    {
        question: "3+2-5=",
        a: "6",
        b: "-2",
        c: "0",
        d: "-6",
        correct: "c"
    },
    {
        question: "3-6-5+4=",
        a: "-4",
        b: "-2",
        c: "2",
        d: "3",
        correct: "a"
    },
    {
        question: "75-325+375-25=",
        a: "100",
        b: "150",
        c: "200",
        d: "250",
        correct: "a"
    },
    {
        question: "(4-6)+7-3=",
        a: "2",
        b: "6",
        c: "8",
        d: "10",
        correct: "c"
    },
    {
        question: "13-(2-4)-5=",
        a: "7",
        b: "8",
        c: "9",
        d: "10",
        correct: "d"
    }
];

const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const submitButton = document.getElementById('submit');

function buildQuiz() {
    const output = [];

    quizData.forEach((currentQuestion, questionNumber) => {
        const answers = [];

        for (let letter in currentQuestion) {
            if (letter !== 'question' && letter !== 'correct') {
                answers.push(
                    `<label>
                        <input type="radio" name="question${questionNumber}" value="${letter}">
                        ${letter} :
                        ${currentQuestion[letter]}
                    </label>`
                );
            }
        }

        output.push(
            `<div class="question">${currentQuestion.question}</div>
            <div class="answers">${answers.join('')}</div>`
        );
    });

    quizContainer.innerHTML = output.join('');
}

function showResults() {
    const answerContainers = quizContainer.querySelectorAll('.answers');
    let numCorrect = 0;

    quizData.forEach((currentQuestion, questionNumber) => {
        const answerContainer = answerContainers[questionNumber];
        const selector = `input[name=question${questionNumber}]:checked`;
        const userAnswer = (answerContainer.querySelector(selector) || {}).value;

        if (userAnswer === currentQuestion.correct) {
            numCorrect++;
            answerContainers[questionNumber].style.color = 'green';
        } else {
            answerContainers[questionNumber].style.color = 'red';
        }
    });

    resultsContainer.innerHTML = `${quizData.length} 問中 ${numCorrect} 問正解しました。`;
}

buildQuiz();

submitButton.addEventListener('click', showResults);
