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
const nextButton = document.getElementById('next');

let currentQuizData = [];
let currentIndex = 0;
const questionsPerSet = 5;

function getNextQuestions() {
    return quizData.slice(currentIndex, currentIndex + questionsPerSet);
}

function buildQuiz() {
    const output = [];
    currentQuizData = getNextQuestions();

    currentQuizData.forEach((currentQuestion, questionNumber) => {
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

    currentQuizData.forEach((currentQuestion, questionNumber) => {
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

    resultsContainer.innerHTML = `${currentQuizData.length} 問中 ${numCorrect} 問正解しました。`;
}

function nextQuiz() {
    currentIndex += questionsPerSet;
    if (currentIndex >= quizData.length) {
        currentIndex = 0;  // リストの終わりに達したら最初に戻る
    }
    buildQuiz();
    resultsContainer.innerHTML = '';  // 前回の結果をクリア
}

buildQuiz();

submitButton.addEventListener('click', showResults);
nextButton.addEventListener('click', nextQuiz);
