const quizData = [
    {
        question: "日本の首都はどこですか？",
        a: "大阪",
        b: "名古屋",
        c: "京都",
        d: "東京",
        correct: "d"
    },
    {
        question: "ピカソの有名な絵はどれですか？",
        a: "モナ・リザ",
        b: "ゲルニカ",
        c: "最後の晩餐",
        d: "ひまわり",
        correct: "b"
    },
    {
        question: "地球の周囲はどれくらいですか？",
        a: "約20,000km",
        b: "約30,000km",
        c: "約40,000km",
        d: "約50,000km",
        correct: "c"
    }
];

const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const submitButton = document.getElementById('submit');

function buildQuiz() {
    const output = [];

    quizData.forEach((currentQuestion, questionNumber) => {
        const answers = [];

        for (letter in currentQuestion) {
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
