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
    },
    {
        question: "(+1)+(-7)-(+4)-(-9)=",
        a: "-1",
        b: "-2",
        c: "-3",
        d: "-4",
        correct: "a"
    },
    {
        question: "18-7+3=",
        a: "14",
        b: "13",
        c: "12",
        d: "15",
        correct: "d"
    },
    {
        question: "9-5+2=",
        a: "7",
        b: "6",
        c: "5",
        d: "4",
        correct: "b"
    },
    {
        question: "20-10+5-15=",
        a: "0",
        b: "5",
        c: "-5",
        d: "-10",
        correct: "c"
    },
    {
        question: "50-25+30-10=",
        a: "55",
        b: "45",
        c: "35",
        d: "40",
        correct: "b"
    }
];

// クイズの表示と結果の表示に使用されるHTML要素を取得
const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const submitButton = document.getElementById('submit');
const nextButton = document.getElementById('next');

let currentQuizData = []; // 現在表示されているクイズのデータ
let currentIndex = 0; // 現在のクイズのインデックス
const questionsPerSet = 5; // 一度に表示する問題の数

// 次の問題セットを取得する関数
function getNextQuestions() {
    return quizData.slice(currentIndex, currentIndex + questionsPerSet);
}

// クイズを構築して表示する関数
function buildQuiz() {
    const output = [];
    currentQuizData = getNextQuestions();

    currentQuizData.forEach((currentQuestion, questionNumber) => {
        const answers = [];

        // 現在の質問の選択肢を生成
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

        // 質問とその選択肢をoutputに追加
        output.push(
            `<div class="question">${currentQuestion.question}</div>
            <div class="answers">${answers.join('')}</div>`
        );
    });

    // クイズをHTMLに表示
    quizContainer.innerHTML = output.join('');
}

// 結果を表示する関数
function showResults() {
    const answerContainers = quizContainer.querySelectorAll('.answers');
    let numCorrect = 0;

    // 各質問の回答をチェック
    currentQuizData.forEach((currentQuestion, questionNumber) => {
        const answerContainer = answerContainers[questionNumber];
        const selector = `input[name=question${questionNumber}]:checked`;
        const userAnswer = (answerContainer.querySelector(selector) || {}).value;

        // 正解の場合、緑色に、不正解の場合、赤色にする
        if (userAnswer === currentQuestion.correct) {
            numCorrect++;
            answerContainers[questionNumber].style.color = 'green';
        } else {
            answerContainers[questionNumber].style.color = 'red';
        }
    });

    // 結果をHTMLに表示
    resultsContainer.innerHTML = `${currentQuizData.length} 問中 ${numCorrect} 問正解しました。`;
}

// 次のクイズセットを表示する関数
function nextQuiz() {
    currentIndex += questionsPerSet;
    if (currentIndex >= quizData.length) {
        currentIndex = 0;  // リストの終わりに達したら最初に戻る
    }
    buildQuiz();
    resultsContainer.innerHTML = '';  // 前回の結果をクリア
}

// 初期クイズの表示
buildQuiz();

// ボタンにイベントリスナーを追加
submitButton.addEventListener('click', showResults);
nextButton.addEventListener('click', nextQuiz);
